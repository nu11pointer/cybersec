import discord
import os
import platform
import pathlib
from discord.ext import commands
import src.log as log
import src.virustotal as virustotal
import src.encoding as encoding
import src.nvd as nvd
import src.cmd_admin as admin
import src.cmd as cmd
import src.writeups as writeups
from src.args import parse
from src.version import __version__

TOKEN = os.getenv("TOKEN")
PATH = str(pathlib.Path(__file__).parent.absolute())
    
def main():
    argv = parse(__version__)
    bot = commands.Bot(command_prefix=argv.prefix, case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    if (not os.path.exists(PATH + "/logs")):
        os.mkdir(PATH + "/logs")

    @bot.command()
    async def hello(ctx):
        await ctx.send(cmd.hello(ctx.message.author))
        
    @bot.command()
    async def whoami(ctx):
        await ctx.send(cmd.whoami(bot.user.name))

    @bot.command()
    async def id(ctx):
        await ctx.send(cmd.id(bot.user.name.lower(), ctx.author.name))

    @bot.command()
    async def ping(ctx):
        await ctx.send(cmd.ping(bot.latency))
    
    @bot.command()
    @commands.has_role(argv.management_role)
    async def env(ctx):
        print(ctx.message.content)
        if (argv.management_channel and not ctx.channel.name == argv.management_channel):
            await ctx.send("Unauthorized! This action will be logged.")
            log.unauthorized(ctx.author, ctx.channel.name, cmd=ctx.command)
            return
        await ctx.send(admin.env())
    
    @bot.command()
    @commands.has_role(argv.management_role)
    async def set(ctx, var=None, value=None):
        if (argv.management_channel and not ctx.channel.name == argv.management_channel):
            await ctx.send("Unauthorized! This action will be logged.")
            log.unauthorized(ctx.author, ctx.channel.name, cmd=ctx.command)
            return
        await ctx.send(admin.set(bot, var, value))
        
    @bot.command()
    async def cve(ctx, value):
        if (not os.getenv("NVD_API_KEY")):
            await ctx.send("Please set the `NVD_API_KEY` token!")
            return

        out, components = nvd.cve(value)
        await ctx.send(out, components=components)
        
    @bot.command()
    async def search(ctx, *, vars):
        if(not vars):
            await ctx.send(f"Missing a required argument. Use {bot.command_prefix}help.")
            return
        if (not os.getenv("GOOGLE_API_KEY")):
            await ctx.send(f"Please set the `GOOGLE_API_KEY` token!")
            return

        query = f"site:ctftime.org inurl:writeup {vars}"

        response, components = writeups.search(query)

        await ctx.send(response, components=components)

    @bot.command(category="Search", help="Search for a given hash on VirusTotal")
    async def vt(ctx, hash):
        if (not os.getenv("VIRUSTOTAL_API_KEY")):
            await ctx.send("Please set the `VIRUSTOTAL_API_KEY` token!")
            return

        out, components = virustotal.submit(hash)
        await ctx.send(out, components=components)
    
    @bot.command()
    async def decode(ctx, type, *, data):
        decoded = encoding.decoder(type, data)
        await ctx.send(decoded)

    @bot.command()
    async def encode(ctx, type, *, data):
        encoded = encoding.encoder(type, data)
        await ctx.send(encoded)
            
    @bot.event
    async def on_ready():
        print(f"{bot.user.name} {__version__}")
        print(f"Discord {discord.__version__}")
        print(f"Python {platform.python_version()}")
        print(f"\nConnected as {bot.user}")
        print("-------------------------------")
        await bot.change_presence(activity=discord.Activity(status=discord.Status.online, type=discord.ActivityType.listening, state="Online", details=f"Version {__version__}", name=f"{bot.command_prefix}help"))

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Unknown command! Use {bot.command_prefix}help.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing a required argument. Do {bot.command_prefix}help.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the appropriate permissions to run this command.")
        if isinstance(error, commands.MissingRole):
            await ctx.send("Unauthorized! This action will be logged.")
            log.unauthorized(ctx.author, ctx.channel.name, cmd=ctx.command)
        else:
            log.error(ctx.message.content, error)

    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Unauthorized: Improper token has beed passed!")
    except RuntimeError:
        print("Aborting...")

if __name__ == "__main__":
    main()