# discord-message-forwarder
The discord-message-forwarder sends dms and mentions of the bot to a specified text channel. 

Image: nzspongebob/discord-message-forwarder:latest https://hub.docker.com/r/nzspongebob/discord-message-forwarder

Forwards Discord messages

A lightweight, containerized Discord bot that forwards Direct Messages (DMs) and @mentions to a designated Discord channel for logging, moderation, or personal notifications.

This bot is designed to be a simple, "set it and forget it" service that runs 24/7. It's configured entirely with environment variables, requiring no code changes to deploy.

FEATURES
Forwards all received Direct Messages (DMs).
Listens for @mentions in any channel the bot is in.
Forwards these messages to a specific channel for logging or moderation.
Configured entirely with environment variables.
Lightweight and designed for 24/7 operation.
USAGE
To run this bot, you will need a bot token from the Discord Developer Portal and the ID of the channel you want messages to be forwarded to.

Use the following docker run command to start the container. You should copy this command and replace the placeholder values.

docker run -d --name discord-forwarder --restart always -e BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN" -e FORWARD_CHANNEL_ID="YOUR_DESTINATION_CHANNEL_ID" your-dockerhub-username/discord-message-forwarder:latest

ENVIRONMENT VARIABLES
The container is configured using the following environment variables passed at runtime.

BOT_TOKEN
Required: Yes
Description: The secret token for your Discord bot from the Discord Developer Portal.

FORWARD_CHANNEL_ID
Required: Yes
Description: The ID of the Discord text channel where all DMs and mentions will be forwarded.

BOT PREREQUISITES
Before running the container, ensure you have set up your bot correctly in the Discord Developer Portal:

Create an Application and add a Bot to it.
Under the "Bot" tab, enable the following Privileged Gateway Intents: SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT.
Invite the bot to any servers you want it to monitor for mentions using the OAuth2 URL Generator. It needs the 'bot' scope.
