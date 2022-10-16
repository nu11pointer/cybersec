#!/usr/bin/env python3

from datetime import datetime
from sqlite3 import Timestamp
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
    bot = commands.Bot(command_prefix=argv.prefix, case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False), help_command=None)
    if (not os.path.exists(PATH + "/logs")):
        os.mkdir(PATH + "/logs")
    
    @bot.command()
    async def help(ctx):
        admin = False
        for role in ctx.author.roles:
            if (argv.management_role == role.name):
                if (argv.management_channel and argv.management_channel == ctx.channel.name):
                    admin = True

        desc = cmd.__help__ if not admin else cmd.__helpadmin__
        embed = discord.Embed(title="\t*Help Page*", colour=discord.Colour.green(), type="article", description=desc)
        embed.set_author(name="CYBERSEC", url="https://github.com/fssecur3/cybersec")
        embed.set_footer(text="> Developed by Francisco Spínola (fssecur3)")
        embed.set_thumbnail(url="https://en.gravatar.com/userimage/224659032/c4b7169b35d5b85855a209c844f03543.png?size=200")
        await ctx.send(embed=embed)

    @bot.command(help="be nice and greet me!")
    async def hello(ctx):
        await ctx.send(cmd.hello(ctx.message.author))
        
    @bot.command(help="who am I?")
    async def whoami(ctx):
        await ctx.send(cmd.whoami(bot.user.name))

    @bot.command(help="why not?")
    async def id(ctx):
        await ctx.send(cmd.id(bot.user.name.lower(), ctx.author.name))

    @bot.command(help="check the bot latency")
    async def ping(ctx):
        await ctx.send(cmd.ping(bot.latency))
    
    @bot.command(help="display the current API keys")
    @commands.has_role(argv.management_role)
    async def env(ctx):
        if (argv.management_channel and not ctx.channel.name == argv.management_channel):
            await ctx.send("Unauthorized! This action will be logged.")
            log.unauthorized(ctx.author, ctx.channel.name, cmd=ctx.command)
            return
        await ctx.send(admin.env())
    
    @bot.command(help="modify or add a value to a variable")
    @commands.has_role(argv.management_role)
    async def set(ctx, variable=None, value=None):
        if (argv.management_channel and not ctx.channel.name == argv.management_channel):
            await ctx.send("Unauthorized! This action will be logged.")
            log.unauthorized(ctx.author, ctx.channel.name, cmd=ctx.command)
            return
        await ctx.send(admin.set(bot, variable, value))
    
    @bot.command(help="search for public exploits on Exploit DB")
    async def exploit(ctx, *, keywords):
        out, components = cmd.exploit(keywords)
        await ctx.send(out, components=components)
        
    @bot.command(help="get details from a CVE")
    async def cve(ctx, value):
        if (not os.getenv("NVD_API_KEY")):
            await ctx.send("Please set the `NVD_API_KEY` token!")
            return

        out, components = nvd.cve(value)
        await ctx.send(out, components=components)
        
    @bot.command(help="search for CTFtime writeups related to the provided keywords")
    async def writeup(ctx, *, vars):
        if(not vars):
            await ctx.send(f"Missing a required argument. Use {bot.command_prefix}help.")
            return
        if (not os.getenv("GOOGLE_API_KEY")):
            await ctx.send(f"Please set the `GOOGLE_API_KEY` token!")
            return

        query = f"site:ctftime.org inurl:writeup {vars}"

        response, components = writeups.search(query)

        await ctx.send(response, components=components)

    @bot.command(help="search for a given hash on VirusTotal")
    async def vt(ctx, hash):
        if (not os.getenv("VIRUSTOTAL_API_KEY")):
            await ctx.send("Please set the `VIRUSTOTAL_API_KEY` token!")
            return

        out, components = virustotal.submit(hash)
        await ctx.send(out, components=components)
    
    @bot.command(help="decode a given string")
    async def decode(ctx, type, *, data):
        decoded = encoding.decoder(type, data)
        await ctx.send(decoded)

    @bot.command(help="encode a given string")
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
        print("Unauthorized: Improper token provided!")
    except RuntimeError:
        print("Aborting...")

if __name__ == "__main__":
    main()