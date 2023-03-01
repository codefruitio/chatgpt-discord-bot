# ChatGPT Discord Bot

# chatgpturbot

You'll need a Discord bot to get started. Here is a reference for how to set one up

[https://discord.com/developers/docs/getting-started](https://discord.com/developers/docs/getting-started)

You'll also need to grab your API key from your OpenAI profile.

## run

```
# create container and run
sudo docker run -d --name chatgpturbot --env DISCORD_BOT_TOKEN="discord-bot-api-key" --env OPENAI_API_KEY="openai-api-key" tylerplesetz/chatgpturbot:latest
```
