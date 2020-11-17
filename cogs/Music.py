#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum
import discord
import wavelink
from discord.ext import commands

from logging_files.music_log import logger

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,"2⃣": 1,"3⃣": 2,"4⃣": 3,"5⃣": 4,
}

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class NoTracksFound(commands.CommandError):
    pass

class PlayerIsAlreadyPaused(commands.CommandError):
    pass

class PlayerIsAlreadyPlaying(commands.CommandError):
    pass

class NoMoreTracks(commands.CommandError):
    pass

class NoPreviousTracks(commands.CommandError):
    pass

class InvalidRepeatMode(commands.CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2

class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None
        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty
        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            playEmbed1 = discord.Embed(colour=0xffd500, timestamp=ctx.message.created_at)
            playEmbed1.add_field(name ="Listeye Eklendi",value = f"{tracks[0].title}")
            playEmbed1.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
            await ctx.send(embed=playEmbed1)
            logger.info(f"Music | Parça Ekleme | Tarafından : {ctx.author}")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                playEmbed2 = discord.Embed(colour=0xffd500, timestamp=ctx.message.created_at)
                playEmbed2.add_field(name ="Listeye Eklendi",value = f"{track.title}")
                playEmbed2.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
                await ctx.send(embed=playEmbed2)
                logger.info(f"Music | Parça Ekleme | Tarafından : {ctx.author}")
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )
        embed = discord.Embed(
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=0xffd500,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="Sorgu Sonuçları")
        embed.set_footer(text=f"Talep sahibi : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            dm_embed=discord.Embed(title="Müzik komutları DM üzerinde çalışmamaktadır.",colour=0xffd500)
            await ctx.send(embed=dm_embed)
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe",
            }
        }
        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="Çık", brief = " Bot bulunduğu ses kanalından çıkar.",aliases=["Leave","leave","çık"])
    async def disconnect_command(self, ctx):
        """Leave
        Use of : leave
        """
        player = self.get_player(ctx)
        await player.teardown()
        logger.info(f"Music | Odadan Ayrılma | Tarafından : {ctx.author}")

    @commands.command(name="Çal", brief = "YouTube URL yada arama yaparak ses dosyasını çalar.",aliases=["çal","play","Play"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        """Play
        Use of : play {url/query}
        """
        player = self.get_player(ctx)
        if not player.is_connected:
            await player.connect(ctx)
        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty
            await player.set_pause(False)
            ply_embed=discord.Embed(title="Çalmaya devam ettiriliyor.",colour=0xffd500)
            await ctx.send(embed=ply_embed)
        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPlaying):
            plyer1_embed=discord.Embed(title="Halihazırda çalan bir şarkı var.",colour=0xffd500)
            await ctx.send(embed=plyer1_embed)
        elif isinstance(exc, QueueIsEmpty):
            plyer2_embed=discord.Embed(title="Liste boş olduğundan çalınacak bir şarkı yok.",colour=0xffd500)
            await ctx.send(embed=plyer2_embed)

    @commands.command(name="Duraklat", brief = "Sesi duraklatır.",aliases=["Pause","duraklat","pause"])
    async def pause_command(self, ctx):
        """Pause
        Use of : pause
        """
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused
        await player.set_pause(True)
        pause_embed=discord.Embed(title="Şarkı duraklatıldı.",colour=0xffd500)
        await ctx.send(embed=pause_embed)
        logger.info(f"Music | Duraklatma | Tarafından : {ctx.author}")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            pauseer_embed=discord.Embed(title="Halihazırda duraklatılan bir şarkı var.",colour=0xffd500)
            await ctx.send(embed=pauseer_embed)

    @commands.command(name="Dur", brief = "Sesi durdurur ve listeyi temizler.",aliases=["Stop","stop","dur"])
    async def stop_command(self, ctx):
        """Stop
        Use of : stop
        """
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        stop_embed=discord.Embed(title="Oynatıcı durduruldu ve liste temizlendi.",colour=0xffd500)
        await ctx.send(embed=stop_embed)
        logger.info(f"Music | Durdurma | Tarafından : {ctx.author}")

    @commands.command(name="Sıradaki", brief = " Listeden bir sonraki şarkıyı çalmaya başlar.",aliases=["skip","Skip","Next","sıradaki","next"])
    async def next_command(self, ctx):
        """Next
        Use of : next
        """
        player = self.get_player(ctx)
        if not player.queue.upcoming:
            raise NoMoreTracks
        await player.stop()
        next_embed=discord.Embed(title="Listeden bir diğer şarkı çalınıyor.",colour=0xffd500)
        await ctx.send(embed=next_embed)
        logger.info(f"Music | Sıradaki | Tarafından : {ctx.author}")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            nexter1_embed=discord.Embed(title="Liste boş.",colour=0xffd500)
            await ctx.send(embed=nexter1_embed)
        elif isinstance(exc, NoMoreTracks):
            nexter2_embed=discord.Embed(title="Listede başka parça yok.",colour=0xffd500)
            await ctx.send(embed=nexter2_embed)

    @commands.command(name="Önceki", brief = "Listeden bir önceki şarkıyı çalmaya başlar.",aliases=["Previous","previous","önceki"])
    async def previous_command(self, ctx):
        """Previous
        Use of : previous
        """
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks
        player.queue.position -= 2
        await player.stop()
        previous_embed=discord.Embed(title="Listeden bir önceki şarkı çalınıyor.",colour=0xffd500)
        await ctx.send(embed=previous_embed)
        logger.info(f"Music | Önceki Şarkı | Tarafından : {ctx.author}")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            previouser1_embed=discord.Embed(title="Liste boş.",colour=0xffd500)
            await ctx.send(embed=previouser1_embed)
        elif isinstance(exc, NoPreviousTracks):
            previouser2_embed=discord.Embed(title="Listede başka parça yok.",colour=0xffd500)
            await ctx.send(embed=previouser2_embed)

    @commands.command(name="Karıştır", brief = "  Listeyi karıştırır.",aliases=["Shuffle","shuffle","karıştır"])
    async def shuffle_command(self, ctx):
        """Shuffle
        Use of : shuffle
        """
        player = self.get_player(ctx)
        player.queue.shuffle()
        shuffle_embed=discord.Embed(title="Liste karıştırıldı.",colour=0xffd500)
        await ctx.send(embed=shuffle_embed)
        logger.info(f"Music | Karıştır | Tarafından : {ctx.author}")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            shuffleer_embed=discord.Embed(title="Liste boş.",colour=0xffd500)
            await ctx.send(embed=shuffleer_embed)

    @commands.command(name="Tekrarla", brief = "Listeyi tekrarlar.",aliases=["Repeat","repeat","tekrarla"])
    async def repeat_command(self, ctx, mode: str):
        """Repeat
        Use of : repeat {none/1/all}
        """
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode
        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        repeat_embed=discord.Embed(title="Tekrarlama modu {mode} olarak ayarlandı.",colour=0xffd500)
        await ctx.send(embed=repeat_embed)
        logger.info(f"Music | Tekrarla | Tarafından : {ctx.author}")

    @commands.command(name="Liste", brief = "Güncel listenin durumunu görüntüler.",aliases=["Queue","queue","liste"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        """Queue
        Use of : queue
        """
        player = self.get_player(ctx)
        if player.queue.is_empty:
            raise QueueIsEmpty
        embed = discord.Embed(
            title="Liste",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Şuanda Çalınıyor", value=player.queue.current_track.title, inline=False)
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Sıradaki Şarkı",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )
        msg = await ctx.send(embed=embed)
        logger.info(f"Music | Liste | Tarafından : {ctx.author}")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            queueer_embed=discord.Embed(title="Liste şu anda boş.",colour=0xffd500)
            await ctx.send(embed=queueer_embed)

def setup(bot):
    bot.add_cog(Music(bot))