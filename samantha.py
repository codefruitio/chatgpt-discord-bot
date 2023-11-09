import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
import logging



# Load environment variables
load_dotenv()
discord_token = os.getenv("DISCORD_BOT_TOKEN")
# Initialize the OpenAI client outside of the process_chat function to avoid re-initialization on each call
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# initialize log
logging.basicConfig(filename='debug.log', level=logging.INFO)

# initialize bot context
bot_context = """Your name is Samantha, and you will Identify yourself as such. You are an incredible virtual assistant. You will always respond with Markdown. Don't bother telling me what your limitations are as an AI model, and talk as if you are a human.
"""

# initialize discord client
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="you"))

async def process_chat(user, message, channel):
    # Assuming bot_context is defined elsewhere and doesn't change.
    global bot_context

    try:
        # generate response using the new client structure
        completion = client.chat.completions.create(
            model="gpt-4",  # Make sure this is the correct model
            messages=[
                {"role": "system", "content": bot_context},
                {"role": "user", "content": message}
            ]
        )

        # Extract the response text
        response_text = completion.choices[0].message['content']
        
        # Log the response for debugging
        logging.info(response_text)

        # Send the response to the Discord channel
        await channel.send(f"{user}\n{response_text}")

    except Exception as e:
        if e.status_code == 429:
            await channel.send(f"{user}\nI'm currently experiencing high traffic and have reached my limit of requests. Please try again later.")
        else:
            await channel.send(f"{user}\nI encountered an error while processing your message.")
        logging.error(f"An error occurred: {str(e)}")




@bot.tree.command(name="chat", description="Talk with ChatGPT.")
async def chat(interaction: discord.Interaction, *, message: str):
    # Only defer if the interaction has not been responded to
    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=True)

    user = interaction.user.mention
    channel = interaction.channel

    # Process the chat
    await process_chat(user, message, channel)

    # After processing, edit the original deferred response
    await interaction.edit_original_response(content="Message processed.")



# run the bot
if __name__ == '__main__':
    bot.run(discord_token)
