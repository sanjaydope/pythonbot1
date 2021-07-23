import asyncio

import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)





client = commands.Bot(command_prefix='')

status = ['with mani and anand!', 'reels!', 'in JMK meeting!']

@client.event
async def on_ready():
    change_status.start()
    print('Bot is online!')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}! வாங்க நண்பரே எப்படி இருக்கீங்க!')



@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**எனக்கு ஓரும் மயிரும் தெரியாதுலே ** கேர்த்து சொல்றேன்  Latency: {round(client.latency * 1000)}ms')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['என்ன வேணும்லே சும்மா சும்மா கூப்பிட்டு சாவடிகாராலே ', 'வணக்கம் நண்பரோ !',  'Hi','என்னலே லெட்டர் படிக்க போனும் என்ன  வெணும்லேய் உனக்கு ']
    await ctx.send(choice(responses))

@client.command(name='bye', help='This command returns a random welcome message')
async def bye(ctx):
    responses = ['bye da settapayale ', 'bye நண்பரோ !',  'ponumnaa poley settapayale','poitu vanga நண்பரோ !']
    await ctx.send(choice(responses))



@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['போலே நாரா பயலே ', 'நீ சவுலே ']
    await ctx.send(choice(responses))

@client.command(name='credits', help='This command returns the credits')
async def credits(ctx):
    await ctx.send('made by 11.De meme BOI')
    await ctx.send('GP MUTHU')

@client.command(name='settapayale', help='This command returns the TRUE credits')
async def settapayale(ctx):
    await ctx.send('**அது என் dialogue பெடில போனவன்னெ**')

@client.command(name='play', help='This command plays music')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()



@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


client.run("ODY3MjgyNjkyNzg1OTYzMDYy.YPe18w.NFy81v2f2_PEbThU2NiB7Pp2HTA")



