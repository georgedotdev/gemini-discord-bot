import discord
from discord.ext import commands, tasks

from youtube_dl import YoutubeDL


class MusicAgent(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self,ctx):
            if len(self.music_queue) > 0:
                self.is_playing = True
                m_url = self.music_queue[0][0]['source']

                if self.vc == None or not self.vc.is_connected():
                    self.vc = await self.music_queue[0][1].connect()

                    if self.vc == None:
                        await ctx.send("Could not connect to the voice channel")
                else:
                    await self.vc.move_to(self.music_queue[0][1])
                self.music_queue.pop(0) 

                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())   

            else:
                self.is_playing = False
        

    @commands.command(name = "play",aliases = ["p","playing"], help = "Plays a selected song from youtube")
    async def play(self,ctx,*args):
        query = "  ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Connect to a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. The song might be too long.")
            else:
                await ctx.send("Song addes to the queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)
    @commands.command(name = "pause", help = "Pauses the current song")
    async def pause(self,ctx,*args):
        if self.vc and self.vc.is_playing():
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            
            await ctx.send("Paused")
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("I am currently paused")

    @commands.command(name = "resume", help = "Resumes the current song")
    async def resume(self,ctx,*args):
        if self.vc and self.vc.is_paused():
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            await ctx.send("Resumed")
        else:
            await ctx.send("I am not paused")
    @commands.command(name = "skip", help = "Skips the current song")
    async def skip(self,ctx,*args):
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await self.play_music(ctx)
            await ctx.send("Skipped")

    @commands.command(name = "queue", help = "Shows the current queue")

    async def queue(self,ctx):
        retval = ""

        for i in range(0,len(self.music_queue)):
            if i>5:break
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
    
    @commands.command(name = "clear", help = "Clears the current queue")
    async def clear(self,ctx,*args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Queue cleared")
    
    @commands.command(name = "disconnect", help = "Disconnects the bot from the voice channel")
    async def disconnect(self,ctx):

        self.is_playing = False
        self.is_paused= False
        await self.vc.disconnect()

