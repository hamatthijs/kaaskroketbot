#all imports
#--------------------
import docker
from docker.models.containers import Container
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from time import localtime
import json
import bisect
#--------------------
#all variables
#--------------------
dcc = docker.from_env()

CONTAINER_NAME = "Paarse_Ballen_server"

bot = commands.Bot(
    command_prefix='!', intents = discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
)

dataOpened = False

muted_user = None
#--------------------
#load the bot token
#--------------------
load_dotenv()
#--------------------
#sends a message to the log when the bot is ready
#--------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
#--------------------
#the help command
#--------------------
bot.remove_command("help")
@bot.slash_command(name="help")
async def _help(interaction: discord.Interaction):
    """
    Get help with the bot
    """
    user = interaction.user
    embed = discord.Embed(title="Help", description="Here is a list of all the commands", color=discord.Color.blurple())
    embed.add_field(name="/help", value="Get help with the bot", inline=False)
    embed.add_field(name="/start", value="Start the Minecraft server", inline=False)
    embed.add_field(name="/stop", value="Stop the Minecraft server", inline=False)
    embed.add_field(name="/restart", value="Restart the Minecraft server", inline=False)
    embed.add_field(name="!money", value="Get money", inline=False)
    embed.add_field(name="!zoo", value="Get zoo", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
#--------------------
#the ping command
#--------------------
@bot.slash_command()
async def ping(interaction: discord.Interaction):
    """
    Get the bot's ping
    """
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")
#--------------------
#the commands command
#--------------------
@bot.slash_command(name="commands")
async def _commands(interaction: discord.Interaction):
    """
    Get the commands
    """
    embed = discord.Embed(title="Commands", description="Here is a list of all the commands", color=discord.Color.blurple())
    embed.add_field(name="/help", value="Get help with the bot", inline=False)
    embed.add_field(name="/start", value="Start the Minecraft server", inline=False)
    embed.add_field(name="/stop", value="Stop the Minecraft server", inline=False)
    embed.add_field(name="/restart", value="Restart the Minecraft server", inline=False)
    embed.add_field(name="!money", value="Get money", inline=False)
    embed.add_field(name="!zoo", value="Get zoo", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
#--------------------
#admin commands command
#--------------------
@bot.slash_command()
async def admin(interaction: discord.Interaction):
    """
    Get the admin commands
    """
    embed = discord.Embed(title="Admin commands", description="Here is a list of all the admin commands", color=discord.Color.blurple())
    embed.add_field(name="/mute", value="Mute a user", inline=False)
    embed.add_field(name="/unmute", value="Unmute a user", inline=False)
    embed.add_field(name="/ban", value="Ban a user", inline=False)
    embed.add_field(name="/unban", value="Unban a user", inline=False)
    embed.add_field(name="/kick", value="Kick a user", inline=False)
    embed.add_field(name="/giverole", value="Give a user a role", inline=False)
    embed.add_field(name="/removeotherrole", value="Remove a role from a user", inline=False)
    embed.add_field(name="/stop", value="Stop the Minecraft server", inline=False)
    embed.add_field(name="/restart", value="Restart the Minecraft server", inline=False)
    embed.add_field(name="/spongebob", value="Create channels", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
#--------------------
#give a role when user joines
#--------------------
@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id == 11217139618013593926: #sever balaap
        role = member.guild.get_role(1121714519102738483) 
        await member.add_roles(role)
    elif member.guild.id == 1072785326168346706: #server downtown
        role = member.guild.get_role(1072785468569169930)
        await member.add_roles(role)
#--------------------
#give yourself a role command
#--------------------
@bot.slash_command()
async def role(interaction: discord.Interaction, role: discord.Role):
    """
    Give a role
    """
    if role in interaction.user.roles:
        await interaction.response.send_message("You already have that role!", ephemeral=True)
    if role.id in [1072785468569169930, 1072786364279566396]:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{interaction.user.name} now has the role {role.name}")
#--------------------
#give others a role command (admin only)
#--------------------
@bot.slash_command()
async def giverole(interaction: discord.Interaction, role: discord.Role, user: discord.Member):
    """
    Give a role to someone 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        if role in user.roles:
            await interaction.response.send_message("They already have that role!", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"{user.name} just got the role {role.name}")
    else:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
#--------------------
#remove your own role command
#--------------------
@bot.slash_command()
async def removerole(interaction: discord.Interaction, role: discord.Role):
    """
    Remove a role
    """
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"{interaction.user.name} no longer has the role {role.name}")
    else:
        await interaction.response.send_message("You don't have that role!", ephemeral=True)
#--------------------
#remove others role command (admin only)
#--------------------
@bot.slash_command()
async def removeotherrole(interaction: discord.Interaction, role: discord.Role, user: discord.Member):
    """
    Remove a role from someone 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"{user.name} no longer has the role {role.name}")
        else:
            await interaction.response.send_message("They don't have that role!", ephemeral=True)
    else:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
#--------------------
#ban command (admin only)
#--------------------
@bot.slash_command()
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str):
    """
    Ban someone 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"{user.name} has been banned for {reason}")
    else:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
#--------------------
#unban command (admin only)
#--------------------
@bot.slash_command()
async def unban(interaction: discord.Interaction, user: discord.User, reason: str):
    """
    Unban someone 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        await user.unban(reason=reason)
        await interaction.response.send_message(f"{user.name} has been unbanned for {reason}")
    else:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
#--------------------
#kick command (admin only)
#--------------------
@bot.slash_command()
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str):
    """
    Kick someone 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"{user.name} has been kicked for {reason}")
    else:
        await interaction.response.send_message("You don't have permission to do that!", ephemeral=True)
#--------------------
#the zoo game
#--------------------
#all buttons
#--------------------
class money_button(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label='+1', style=discord.ButtonStyle.blurple)
    async def plusOne(self, button: discord.ui.Button, interaction: discord.Interaction):
        global dataOpened
        if dataOpened:
            await interaction.response.send_message("hold the fuck up", ephemeral=True, delete_after=1)
            return
        id = str(interaction.user.id)
        with open("./data/data.json", mode="r+", encoding="utf-8") as file:
            dataOpened = True
            data = json.loads(file.read())
            
            # Initialize with empty arrays if user has no data
            if not data.get(id):
                data[id] = {"money": 0, "animals": []}

            data[id]["money"] += 1 + len(data[id]["animals"])
            
            embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with the most money", color=discord.Color.blurple())
            for id, udata in data.items():
                embed.add_field(name=interaction.guild.get_member(int(id)).name, value=udata["money"])
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(f"You now have {data[id]['money']} money!", ephemeral=True, delete_after=0.0000001)
            
            file.seek(0)
            file.write(json.dumps(data))
        dataOpened = False

class zoo_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.animals = ("monkey", "horse", "dog", "cat", "bird", "fish", "snake", "lion", "tiger", "elephant", "bear", "panda", "penguin", "cow", "pig", "chicken", "sheep", "goat", "duck", "rabbit", "big penis")

    @discord.ui.button(label='zoo button', style=discord.ButtonStyle.blurple)
    async def plusZoo(self, button: discord.ui.Button, interaction: discord.Interaction):
        global dataOpened
        if dataOpened:
            await interaction.response.send_message("hold the fuck up", ephemeral=True, delete_after=1)
            return
        id = str(interaction.user.id)
        choice = random.choice(self.animals)
        with open("./data/data.json", mode="r+", encoding="utf-8") as file:
            dataOpened = True
            data = json.loads(file.read())
            
            # Initialize with empty arrays if user has no data
            if not data.get(id):
                data[id] = {"money": 0, "animals": []}

            if choice not in data[id]["animals"]:
                data[id]["animals"].append(choice)

                embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with their animals", color=discord.Color.blurple())
                for id, udata in data.items():
                    embed.add_field(name=interaction.guild.get_member(int(id)).name, value=", ".join(udata["animals"]))
                await interaction.message.edit(embed=embed)
                await interaction.response.send_message(f"You now have a {choice}!", ephemeral=True, delete_after=5)
            else:
                await interaction.response.send_message(f"You got a {choice}, but you already have it!", ephemeral=True, delete_after=5)

            file.seek(0)
            file.write(json.dumps(data))
        dataOpened = False

def check_level(xp):
    levels = {"1": 100, "2": 200, "3": 300, "4": 400, "5": 500, "6": 600, "7": 700, "8": 800, "9": 900, "10": 1000, "11": 1100, "12": 1200, "13": 1300, "14": 1400, "15": 1500, "16": 1600, "17": 1700, "18": 1800, "19": 1900, "20": 2000, "21": 2100, "22": 2200, "23": 2300, "24": 2400, "25": 2500, "26": 2600, "27": 2700, "28": 2800, "29": 2900, "30": 3000, "31": 3100, "32": 3200, "33": 3300, "34": 3400, "35": 3500, "36": 3600, "37": 3700, "38": 3800, "39": 3900, "40": 4000, "41": 4100, "42": 4200, "43": 4300, "44": 4400, "45": 4500, "46": 4600, "47": 4700, "48": 4800, "49": 4900, "50": 5000, "51": 5100, "52": 5200, "53": 5300, "54": 5400, "55": 5500, "56": 5600, "57": 5700, "58": 5800, "59": 5900, "60": 6000, "61": 6100, "62": 6200, "63": 6300, "64": 6400, "65": 6500, "66": 6600, "67": 6700, "68": 6800, "69": 6900, "70": 7000, "71": 7100, "72": 7200, "73": 7300,}
    xp_thresholds = list(levels.values())
    levels = list(levels.keys())
    
    index = bisect.bisect(xp_thresholds, xp)
    

#--------------------
#all commands using the buttons
#--------------------
@bot.command()
async def money(ctx: commands.Context):
    embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with the most money", color=discord.Color.blurple())
    with open("data/data.json", mode="r+", encoding="utf-8") as file:
        data = json.loads(file.read())
        for id, udata in data.items():
            if udata["money"] == 0 or not int(id) in [member.id for member in ctx.guild.members]:
                continue
            embed.add_field(name=ctx.guild.get_member(int(id)).name, value=udata["money"])
    await ctx.send("Click on button for money", embed=embed, view=money_button())

@bot.command()
async def zoo(ctx: commands.Context):
    embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with their animals", color=discord.Color.blurple())
    with open("data/data.json", mode="r+", encoding="utf-8") as file:
        data = json.loads(file.read())
        for id, udata in data.items():
            if len(udata["animals"]) == 0 or not int(id) in [member.id for member in ctx.guild.members]:
                continue
            embed.add_field(name=ctx.guild.get_member(int(id)).name, value=", ".join(udata["animals"]))
    await ctx.send("Click on the button for zoo", embed=embed, view=zoo_button())
#--------------------
#the level system
#--------------------
@bot.command()
async def level(ctx: commands.Context):
    embed = discord.Embed(title="Leaderboard", description="Here is everyones level", color=discord.Color.blurple())
    with open("data/levels.json", mode="r+", encoding="utf-8") as file:
        data = json.loads(file.read())
        for id, udata in data.items():
            if udata["level"] == 0 or not int(id) in [member.id for member in ctx.guild.members]:
                continue
            embed.add_field(name=ctx.guild.get_member(int(id)).name, value=udata["level"])
#--------------------
#the minecraft server start, stop and restart commands
#stop and restart are admin only
#--------------------
@bot.slash_command(name="start")
async def start(interaction: discord.Interaction):
    """
    Start the Minecraft server
    """
    user = interaction.user
    if interaction.guild.id not in (1072785326168346706, 1121713961801359392):
        await interaction.response.send_message("You can't use this command here!")
        return
    if user.id != 643009066557243402:
        if localtime().tm_hour < 6:
            await interaction.response.send_message(
                "You can't start the server at this time!"
            )
            return
    container: Container = dcc.containers.get(CONTAINER_NAME)
    current_status = container.status
    if current_status in ["exited", "created"]:
        await interaction.response.send_message("Starting server...")
        container.start()
    elif current_status == "running":
        await interaction.response.send_message("Server is already running!")
    elif current_status == "paused":
        await interaction.response.send_message("Server is paused!")
    elif current_status == "restarting":
        await interaction.response.send_message("Server is restarting!")
    elif current_status == "dead":
        await interaction.response.send_message("Server is dead!")

@bot.slash_command(name="stop")
async def stop(interaction: discord.Interaction):
    """
    Stop the Minecraft server 🛑ADMIN ONLY🛑
    """
    container: Container = dcc.containers.get(CONTAINER_NAME)
    user = interaction.user
    if user.id == 643009066557243402:
        current_status = container.status
        if current_status in ["exited", "created"]:
            await interaction.response.send_message("Server is not running!")
        elif current_status == "running":
            await interaction.response.send_message("Stopping server...")
            container.stop()
        elif current_status == "paused":
            await interaction.response.send_message("Server is paused!")
        elif current_status == "restarting":
            await interaction.response.send_message("Server is restarting!")
        elif current_status == "dead":
            await interaction.response.send_message("Server is dead!")
    else:
        await interaction.response.send_message("You don't have permission to do this!")

@bot.slash_command(name="restart")
async def restart(interaction: discord.Interaction):
    """
    Restart the Minecraft server 🛑ADMIN ONLY🛑
    """
    container: Container = dcc.containers.get(CONTAINER_NAME)
    user = interaction.user
    if user.id == 643009066557243402:
        current_status = container.status
        if current_status in ["exited", "created"]:
            await interaction.response.send_message("Server is not running!")
        elif current_status == "running":
            await interaction.response.send_message("Restarting server...")
            container.restart()
        elif current_status == "paused":
            await interaction.response.send_message("Server is paused!")
        elif current_status == "restarting":
            await interaction.response.send_message("Server is restarting!")
        elif current_status == "dead":
            await interaction.response.send_message("Server is dead!")
    else:

        await interaction.response.send_message("You don't have permission to do this!")
#--------------------
#mute and unmute command (admin only)
#--------------------
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.mute and not after.mute:
        if member == muted_user:
            if muted == True:
                await member.edit(mute=True)
@bot.slash_command(name="mute")
async def mute(interaction: discord.Interaction, user: discord.Member):
    """
    Mute a user 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        global muted_user
        muted_user = user
        await user.edit(mute=True)
        global muted
        muted = True
        await interaction.response.send_message(f"{user} has been muted!")
    else:
        await interaction.response.send_message("You don't have permission to do this!")
@bot.slash_command(name="unmute")
async def unmute(interaction: discord.Interaction, user: discord.Member):
    """
    Unmute a user 🛑ADMIN ONLY🛑
    """
    if interaction.user.id == 643009066557243402:
        global muted_user
        muted_user = None
        await user.edit(mute=False)
        global muted
        muted = False
        await interaction.response.send_message(f"{user} has been unmuted!")
    else:
        await interaction.response.send_message("You don't have permission to do this!")
#--------------------
#create channels command
#--------------------
@bot.slash_command(name="spongebob")
async def spam(interaction: discord.Interaction, amount: int, server: discord.Guild):
    print("penis")
    if interaction.user.id == 643009066557243402:
        invalidtime = ""
        if amount > 10:
            invalidtime = "You can't create more than 10 channels per command!\nReverting to 10."
            amount = 10
        elif amount < 0:
            await interaction.response.send_message("You can't create less than zero channels!", ephemeral=True)
            return
        await interaction.response.send_message(
            f"{invalidtime}\nCreating channels in '{server}' {amount} times!",
            ephemeral=True,
        )
        for _ in range(amount):
            await server.create_text_channel("spongebob")
    else:
        await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
@spam.error
async def spam_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.GuildNotFound):
        await ctx.respond("I am not in that server!", ephemeral=True)
    else:
        raise error
#--------------------
#runs the bot using the token loaded previously
#--------------------
bot.run(os.getenv("BOT_TOKEN"))
#--------------------
