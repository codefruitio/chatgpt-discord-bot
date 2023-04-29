import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
import requests
import os
import logging


# initialize memory
chat_history = ""

# initialize log
logging.basicConfig(filename='debug.log', level=logging.INFO)


# initialize bot context
bot_context = """Your name is Luna, and you will Identify yourself as such. You are an incredible virtual assistant. You will always respond with Markdown. Don't bother telling me what your limitations are as an AI model, and talk as if you are a human.
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


async def process_chat(user, message, channel):
    global chat_history
    global bot_context
    # trigger typing indicator for the discord bot
    async with channel.typing():
        # generate response

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
             {"role": "system", "content": f"{bot_context}"},
                {"role": "user", "content": chat_history},
                {"role": "assistant", "content": "The user you are interacting with is named Tyler"},
                {"role": "user", "content": message}
            ]
        )
    chat_history += message + "\n"
    response = response['choices'][0]['message']['content']
    # Log a message
    logging.info(response)
    await channel.send(user + "\n" + response)

    return


# wait for use of /chat command
@client.tree.command(name="chat", description="Talk with ChatGPT.")
async def chat(interaction: discord.Interaction, *, message: str):
    user = interaction.user.mention
    channel = interaction.channel
    await interaction.response.send_message("Thinking...", ephemeral=True, delete_after=3)
    await process_chat(user, message, channel)
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        user = message.author.mention
        message_text = message.content.replace(f"<@!{client.user.id}>", "").strip()
        await process_chat(user, message_text, message.channel)
        return


# run the bot
if __name__ == '__main__':
    load_dotenv()
    path_to_notes=os.getenv("PATH_TO_NOTES")
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client.run(discord_token)