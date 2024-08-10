#!/usr/bin/env python3

import discord
import os
import platform
import pathlib
import aiohttp
from discord.ext import commands
import src.exploit as searchsploit
import src.log as log
import src.virustotal as virustotal
import src.encoding as encoding
import src.nvd as nvd
import src.command_admin as admin
import src.command as command
import src.writeups as writeups
import src.hashes as hashes
import src.listen as listen
import src.reverseshell as reverseshell
import src.shellc0de as shellc0de
import src.help as hlp
import src.shodan as sd
from src.help import SUBS
from src.args import parse
from src.version import __version__

TOKEN = os.getenv("TOKEN")
PATH = str(pathlib.Path(__file__).parent.absolute())
    
def main():
    argv = parse(__version__)
    bot = commands.Bot(command_prefix=argv.prefix, case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False), help_command=None)
    if (not os.path.exists(os.path.join(PATH, "logs"))):
        os.mkdir(os.path.join(PATH, "logs"))
    
    @bot.command()
    async def help(ctx, sub=""):
        global SUBS
        desc = ""
        admin = False
        for role in ctx.author.roles:
            if (argv.management_role == role.name):
                if (argv.management_channel and argv.management_channel == ctx.channel.name):
                    admin = True
        if (sub == ""):
            desc = hlp.help() if not admin else hlp.help_admin()
        elif (sub not in SUBS):
            await ctx.send(f"Command '{sub}' does not exist! Use {bot.command_prefix}help.")
            return
        else:
            if (sub == "crack"):
                desc = hlp.help_crack(bot.command_prefix)
            elif (sub == "env"):
                desc = hlp.help_env(bot.command_prefix)
            elif (sub == "cve"):
                desc = hlp.help_cve(bot.command_prefix)
            elif (sub == "encode"):
                desc = hlp.help_encode(bot.command_prefix)
            elif (sub == "decode"):
                desc = hlp.help_decode(bot.command_prefix)
            elif (sub == "exploit"):
                desc = hlp.help_exploit(bot.command_prefix)
            elif (sub == "hashid"):
                desc = hlp.help_hashid(bot.command_prefix)
            elif (sub == "hello"):
                desc = hlp.help_hello(bot.command_prefix)
            elif (sub == "help"):
                desc = hlp.help_help(bot.command_prefix)
            elif (sub == "listener"):
                desc = hlp.help_listener(bot.command_prefix)
            elif (sub == "ping"):
                desc = hlp.help_ping(bot.command_prefix)
            elif (sub == "revshell"):
                desc = hlp.help_revshell(bot.command_prefix)
            elif (sub == "set"):
                desc = hlp.help_set(bot.command_prefix)
            elif (sub == "shellcode"):
                desc = hlp.help_shellcode(bot.command_prefix)
            elif (sub == "shodan"):
                desc = hlp.help_shodan(bot.command_prefix)
            elif (sub == "vt"):
                desc = hlp.help_vt(bot.command_prefix)
            elif (sub == "writeup"):
                desc = hlp.help_writeup(bot.command_prefix)
        
        embed = discord.Embed(title="\t*Help Page*", colour=discord.Colour.green(), type="article", description=desc)
        embed.set_author(name="CYBERSEC", url="https://github.com/nu11pointer/cybersec")
        embed.set_footer(text="> Developed by nu11pointer")
        embed.set_thumbnail(url="https://en.gravatar.com/userimage/224659032/c4b7169b35d5b85855a209c844f03543.png?size=200")
        await ctx.send(embed=embed)

    @bot.command(help="be nice and greet me!")
    async def hello(ctx):
        await ctx.send(command.hello(ctx.message.author))

    @bot.command(help="check the bot latency")
    async def ping(ctx):
        await ctx.send(command.ping(bot.latency))
    
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
        out, components = searchsploit.exploit(keywords)
        await ctx.send(out, components=components)
    
    @bot.command(help="search on shodan")
    async def shodan(ctx, *, keywords):
        out = sd.search(keywords)
        await ctx.send(out)
    
    @bot.command(help="identify hashes")
    async def hashid(ctx, hash):
        out = hashes.hash_id(hash)
        await ctx.send(out)

    @bot.command(help="get details from a CVE")
    async def cve(ctx, value):
        if (not os.getenv("NVD_API_KEY")):
            await ctx.send("Please set the `NVD_API_KEY` token!")
            return

        out, components = nvd.cve(value)
        await ctx.send(out, components=components)
    
    @bot.command(help="listener generator")
    async def listener(ctx, type="", port="9001"):
        if (type.isnumeric()):
            port = type
            type = ""
        out = listen.listener(type, port)
        await ctx.send(out)
    
    @bot.command(help="revshell generator")
    async def revshell(ctx, type, host, port, bash="/bin/sh"):
        out = reverseshell.create(type, host, port, bash)
        await ctx.send(out)
        
    @bot.command(help="search for CTFtime writeups related to the provided keywords")
    async def writeup(ctx, *, vars):
        query = f"site:ctftime.org inurl:writeup {vars}"

        response, components = writeups.search(query)
        await ctx.send(response, components=components)
    
    @bot.command(help="search for shellcode")
    async def shellcode(ctx, *, query):
        response = shellc0de.shellcode(query)
        await ctx.send(response)

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
    
    @bot.command(help="crack a hash")
    async def crack(ctx, alg, hash):
        ret = hashes.crack(hash, alg)
        await ctx.send(ret)
            
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
            await ctx.send(f"Missing a required argument. Do {bot.command_prefix}help {ctx.command}.")
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
    except aiohttp.client_exceptions.ClientConnectorError:
        print("Could not connect to discord servers!")

if __name__ == "__main__":
    main()
