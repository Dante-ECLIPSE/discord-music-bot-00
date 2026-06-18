import discord
from discord.ext import commands
from typing import Dict, List, Optional
import asyncio
import random
import os

class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.voice_client = None
        self.queue = []
        self.now_playing = None
        self.is_paused = False
        self.volume = 0.5
        self.loop_mode = "off"  # off, track, queue
        
    async def connect(self):
        if self.voice_client is None:
            self.voice_client = await self.ctx.author.voice.channel.connect()
            return True
        return False
    
    async def disconnect(self):
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
            return True
        return False
    
    async def play(self, source):
        if self.voice_client is None:
            await self.connect()
        
        if self.voice_client.is_playing():
            self.queue.append(source)
            return False
        
        self.now_playing = source
        self.is_paused = False
        self.voice_client.play(source, after=lambda e: self._play_next())
        return True
    
    def _play_next(self):
        if self.is_paused or not self.queue:
            return
        
        if self.loop_mode == "track":
            self.now_playing.seek(0)
            return
        
        self.now_playing = self.queue.pop(0)
        self.voice_client.play(self.now_playing, after=lambda e: self._play_next())
    
    async def pause(self):
        if self.voice_client is not None and self.voice_client.is_playing():
            self.is_paused = True
            self.voice_client.pause()
            return True
        return False
    
    async def resume(self):
        if self.voice_client is not None and self.voice_client.is_paused():
            self.is_paused = False
            self.voice_client.resume()
            return True
        return False
    
    async def skip(self):
        if self.voice_client is not None and self.queue:
            self.now_playing.stop()
            self.now_playing = self.queue.pop(0)
            return True
        return False
    
    async def shuffle(self):
        random.shuffle(self.queue)
        return True
    
    async def set_volume(self, volume: float):
        self.volume = max(0, min(1, volume))
        if self.voice_client is not None:
            self.voice_client.source.volume = self.volume
        return self.volume
    
    async def loop(self, mode: str):
        valid_modes = ["off", "track", "queue"]
        if mode not in valid_modes:
            return False
        
        self.loop_mode = mode
        return True
    
    @property
    def queue_length(self):
        return len(self.queue)
