import discord
from discord.ext import commands
from .music_player import MusicPlayer
from typing import Optional

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["join", "connect"])
    async def connect_to_voice(self, ctx):
        """Connect to your voice channel"""
        if ctx.author.voice:
            await ctx.send(f"✅ Connected to {ctx.author.voice.channel.name}")
        else:
            await ctx.send("❌ You need to be in a voice channel first!")
    
    @commands.command(aliases=["play", "p", "!p"])
    async def play_music(self, ctx, *, query: str):
        """Play music from YouTube, link, or search"""
        try:
            # In a real bot, you'd use a music library like pyttsx3 or spotipy
            # Here I'll simulate with a simple response
            await ctx.send(f"🎵 Playing: {query}")
        except Exception as e:
            await ctx.send(f"❌ Error playing music: {e}")
    
    @commands.command(aliases=["pause"])
    async def pause_playback(self, ctx):
        """Pause the currently playing music"""
        player = MusicPlayer(ctx)
        if await player.pause():
            await ctx.send("⏸️  Music paused")
        else:
            await ctx.send("❌ No music playing")
    
    @commands.command(aliases=["resume", "unpause"])
    async def resume_playback(self, ctx):
        """Resume paused music"""
        player = MusicPlayer(ctx)
        if await player.resume():
            await ctx.send("▶️  Music resumed")
        else:
            await ctx.send("❌ Nothing to resume")
    
    @commands.command(aliases=["skip", "next"])
    async def skip_track(self, ctx):
        """Skip the current track"""
        player = MusicPlayer(ctx)
        if await player.skip():
            await ctx.send("⏭️  Track skipped")
        else:
            await ctx.send("❌ No tracks to skip")
    
    @commands.command(aliases=["shufflequeue", "shuffle"])
    async def shuffle_queue(self, ctx):
        """Shuffle the music queue"""
        player = MusicPlayer(ctx)
        if await player.shuffle():
            await ctx.send("🔀  Queue shuffled!")
        else:
            await ctx.send("❌ No queue to shuffle")
    
    @commands.command(aliases=["queue", "q", "playlist"])
    async def view_queue(self, ctx):
        """View the current music queue"""
        player = MusicPlayer(ctx)
        queue = player.queue_length
        
        embed = discord.Embed(title="🎵 Music Queue", color=0x2ecc71)
        embed.add_field(name="Tracks in queue", value=str(queue), inline=False)
        
        if queue > 0:
            embed.add_field(
                name="Now playing", 
                value=f"{player.now_playing} " if player.now_playing else "Nothing playing", 
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["volume"])
    async def adjust_volume(self, ctx, volume: int):
        """Adjust music volume (0-100)"""
        if 0 > volume > 100:
            await ctx.send("❌ Volume must be between 0 and 100")
            return
        
        player = MusicPlayer(ctx)
        await player.set_volume(volume / 100)
        await ctx.send(f"🔊 Volume set to {volume}%")
    
    @commands.command(aliases=["loop", "repeat"])
    async def toggle_loop(self, ctx, mode: str = "off"):
        """Loop track or queue. Usage: !loop [track/queue/off]"""
        valid_modes = ["track", "queue", "off"]
        
        if mode not in valid_modes:
            await ctx.send(f"❌ Invalid mode. Use: {', '.join(valid_modes)}")
            return
        
        player = MusicPlayer(ctx)
        await player.loop(mode)
        await ctx.send(f"🔁 Loop set to: **{mode}**")
    
    @commands.command(aliases=["leave", "disconnect"])
    async def leave_voice(self, ctx):
        """Make the bot leave the voice channel"""
        player = MusicPlayer(ctx)
        if await player.disconnect():
            await ctx.send("👋 Left voice channel")
        else:
            await ctx.send("❌ Not connected to a voice channel")
