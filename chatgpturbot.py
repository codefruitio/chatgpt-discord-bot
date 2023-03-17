import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
import requests
import os


# initialize memory
chat_history = "his name is chatbot"
def update_memory():
    path_to_notes = "notes"
    # Load all the Markdown files and combine their content
    context_notes = ""
    for root, _, files in os.walk(path_to_notes):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as md_file:
                    context_notes += md_file.read() + "\n\n\n\n"
    return context_notes


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
    context_notes = update_memory()
    await interaction.response.send_message("Thinking...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. The context you receive will be a series of Markdown notes from the user that you will need to answer questions about. You will also receive a history of the conversation so far."},           
            {"role": "assistant", "content": context_notes},
            {"role": "user", "content": chat_history}
            {"role": "user", "content": message}
        ]
        
    )
    response = response['choices'][0]['message']['content']
    memory += message + "\n"
    user = interaction.user.mention
    await interaction.channel.send(user + ": " + message + "\n\n" + response)
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