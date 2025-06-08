import os
import discord
import requests
import json

# --- Load configuration from environment variables ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
HA_WEBHOOK_URL = os.getenv('HA_WEBHOOK_URL')

# --- Basic checks to ensure configuration is present ---
if not BOT_TOKEN:
    print("FATAL ERROR: BOT_TOKEN environment variable not set.")
    exit(1)

if not HA_WEBHOOK_URL:
    print("FATAL ERROR: HA_WEBHOOK_URL environment variable not set.")
    exit(1)

# --- Define the necessary Discord Intents ---
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Prints a confirmation message when the bot logs in successfully."""
    print(f'Logged in as {client.user}')
    print('Ready to forward DMs, Mentions, and Slash Commands to Home Assistant.')
    print('-----------------------------------------')

@client.event
async def on_message(message):
    """This function handles DMs and @mentions."""
    if message.author == client.user:
        return

    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mention = client.user in message.mentions

    if is_dm or is_mention:
        content_cleaned = message.clean_content.replace(f'@{client.user.name}', '', 1).strip() if is_mention else message.content
        print(f"Triggered by message from '{message.author.name}'.")

        payload = {
            'type': 'message', # NEW: Identify the event type
            'author_name': message.author.name,
            'author_id': str(message.author.id),
            'content': content_cleaned,
            'is_dm': is_dm,
            'guild_name': message.guild.name if message.guild else None,
            'channel_name': message.channel.name if hasattr(message.channel, 'name') else None
        }
        send_to_ha(payload)

# --- NEW: Event handler for slash commands and other interactions ---
@client.event
async def on_interaction(interaction):
    """This function handles slash commands."""
    # We only care about slash commands for now
    if interaction.type == discord.InteractionType.application_command:
        
        # This is CRITICAL. It tells Discord "I got the command" so it doesn't time out.
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        print(f"Triggered by slash command from '{interaction.user.name}'.")

        # Convert the options into a simple dictionary
        options_dict = {opt['name']: opt['value'] for opt in interaction.data.get('options', [])}

        payload = {
            'type': 'slash_command', # NEW: Identify the event type
            'author_name': interaction.user.name,
            'author_id': str(interaction.user.id),
            'command_name': interaction.data['name'],
            'options': options_dict, # Pass along the command options
            'guild_name': interaction.guild.name if interaction.guild else None,
            'channel_name': interaction.channel.name if hasattr(interaction.channel, 'name') else None
        }
        send_to_ha(payload)

def send_to_ha(payload):
    """A helper function to send data to the Home Assistant Webhook."""
    try:
        response = requests.post(
            HA_WEBHOOK_URL,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        print(f"Successfully forwarded event to Home Assistant (Type: {payload['type']})")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to forward event to Home Assistant: {e}")

# --- Run the bot ---
client.run(BOT_TOKEN)