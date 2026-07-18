import os
import requests
import discord
from discord.ext import commands

# 1. Configuration & Security
# Change ONLY the DISCORD_TOKEN string if Discord has deactivated your old one.
DISCORD_TOKEN = "token"
API_KEY = "api"
SERVER_ID = "id" 

# Base API URL matching your provider's custom endpoints
BASE_URL = "https://api.my-mc.link"

# 2. Bot Setup
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to process commands from chat messages
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Helper Function for API Calls
def send_power_signal(action: str) -> tuple[bool, str]:
    """
    Sends a GET request to the my-mc.link panel to start or stop the server.
    Returns a tuple: (success_boolean, status_message)
    """
    if not API_KEY:
        return False, "Missing API authorization key."

    # Custom headers required by my-mc.link documentation
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-my-mc-auth": API_KEY
    }
    
    # Constructs either https://api.my-mc.link/start or https://api.my-mc.link/stop
    url = f"{BASE_URL}/{action}"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") is True:
                return True, f"Successfully sent the **{action}** command to the server."
            else:
                return False, f"Panel rejected command: `{data.get('message', 'Unknown error')}`"
        else:
            return False, f"Panel returned error code {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Failed to connect to the panel API: {str(e)}"

# 4. Bot Events & Commands
@bot.event
async def on_ready():
    """Triggers when the bot boots up and connects to Discord successfully."""
    print(f"Bot backend active. Logged in as: {bot.user.name}")
    print("Awaiting commands...")

@bot.command(name="start")
async def start_server(ctx):
    """Command to turn on the Minecraft server."""
    await ctx.send("⏳ Attempting to start the Minecraft server...")
    
    # Run the API call
    success, message = send_power_signal("start")
    await ctx.send(message)

@bot.command(name="stop")
async def stop_server(ctx):
    """Command to turn off the Minecraft server."""
    await ctx.send("⏳ Attempting to shut down the Minecraft server...")
    
    # Run the API call
    success, message = send_power_signal("stop")
    await ctx.send(message)

# 5. Start the Application
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN is missing.")
    else:
        bot.run(DISCORD_TOKEN)
