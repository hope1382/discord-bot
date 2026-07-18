import os
import requests
import discord
from discord.ext import commands

# 1. Configuration & Security
# These variables pull directly from the "Environment Variables" or "Variables" tab of your cloud host panel.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("MYMC_API_KEY")
SERVER_ID = os.getenv("MYMC_SERVER_ID")  # Add your server ID to your host variables as well

BASE_URL = f"https://info.my-mc.link/api/client/servers/{SERVER_ID}/power"

# 2. Bot Setup
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to process commands from chat messages
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Helper Function for API Calls
def send_power_signal(action: str) -> tuple[bool, str]:
    """
    Sends a POST request to the my-mc.link panel to start or stop the server.
    Returns a tuple: (success_boolean, status_message)
    """
    if not API_KEY or not SERVER_ID:
        return False, "Missing API configuration keys on the host panel."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"signal": action}

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        # Pterodactyl panels usually return 204 No Content for successful power actions
        if response.status_code in [200, 204]:
            return True, f"Successfully sent the **{action}** command to the server."
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
        print("Error: DISCORD_TOKEN environment variable is missing.")
    else:
        bot.run(DISCORD_TOKEN)