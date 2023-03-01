import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
import os

memory = "his name is chatbot"

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="you")

client = aclient()
        
@client.event
async def on_ready():
    await client.tree.sync()

@client.tree.command(name="chat", description="Talk with ChatGPT.")
async def chat(interaction: discord.Interaction, *, message: str):
    global memory
    await interaction.response.send_message("Thinking...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": memory},
            {"role": "user", "content": message}
        ]
    )
    response = response['choices'][0]['message']['content']
    memory += message + "\n"
    user = interaction.user.mention
    await interaction.channel.send(user + ": " + message + "\n\n" + response)
    return
    

if __name__ == '__main__':
    load_dotenv()
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client.run(discord_token)