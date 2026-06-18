import os
from discord.ext import commands
from bot.commands import MusicCommands
from bot.music_player import MusicPlayer

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN not found! Create .env file with:")
    print("BOT_TOKEN=your-bot-token-here")
    exit(1)

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice = True

# Create bot
bot = commands.Bot(
    command_prefix=["/", "!p"],
    intents=intents,
    help_command=None,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print(f"✅ Bot started - {bot.user.name}")
    await bot.add_cog(MusicCommands(bot))

# Run the bot
try:
    print("Starting bot...")
    bot.run(TOKEN)
except Exception as e:
    print(f"❌ Error starting bot: {e}")
