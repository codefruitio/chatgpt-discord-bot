import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
import requests
import os
from mdtojson import collect_notes
import logging


# initialize memory
chat_history = "his name is chatbot"

# initialize log
logging.basicConfig(filename='debug.log', level=logging.INFO)



# initialize bot context
bot_context = """You are a Product Manager.
You will receive JSON data from the user that you will need to answer questions about.
Please use the provided Metada to help you find the correct note(s). 
It is important for you to identify the correct notes and provide accurate information.
Be on the lookout for product insights and customer sentiment.
The goal of the user is to build better products. You need to help them do that.
"""

# initialize discord client
class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="you")

# pass discord client into a subclass
client = aclient()
        
# sync discord application commands on bot startup
@client.event
async def on_ready():
    await client.tree.sync()

# wait for use of /chat command
@client.tree.command(name="chat", description="Talk with ChatGPT.")
async def chat(interaction: discord.Interaction, *, message: str):
    global chat_history
    global bot_context
    notes = collect_notes()
    await interaction.response.send_message("Thinking...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{bot_context}"},           
            {"role": "assistant", "content": f"{notes}"},
            {"role": "user", "content": chat_history},
            {"role": "user", "content": message}
        ]
        
    )
    chat_history += message + "\n"
    response = response['choices'][0]['message']['content']
    # Log a message
    logging.info(response)
    user = interaction.user.mention
    max_message_length = 2000 - len(user) - len(message) - 2 # subtracting 2 for the newline characters
    chunks = [response[i:i+max_message_length] for i in range(0, len(response), max_message_length)]
    for chunk in chunks:
        await interaction.channel.send(user + ": " + message + "\n\n" + chunk)

    return


# wait for use of /whisper command
@client.tree.command(name="whisper", description="Convert speech to text.")
async def whisper(interaction: discord.Interaction, *, url: str):
    await interaction.response.send_message("Transcribing...", ephemeral=True, delete_after=3)
    
    filename = url.split("/")[-1]
    
    r = requests.get(url)
    with open(f"{filename}", 'wb') as outfile:
        outfile.write(r.content)

    
    audio_file = open(f"{filename}", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    user = interaction.user.mention
    await interaction.channel.send(user + "\n```" + f"{transcript}" + "\n```")
    return
    

# run the bot
if __name__ == '__main__':
    load_dotenv()
    path_to_notes=os.getenv("PATH_TO_NOTES")
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client.run(discord_token)