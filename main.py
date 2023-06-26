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
import asyncio
import json
#--------------------
#all variables
#--------------------
dcc = docker.from_env()

CONTAINER_NAME = "Paarse_Ballen_server"

bot = commands.Bot(
    command_prefix='!', intents = discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
)

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

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.mute and not after.mute:
        if member == muted_user:
            await member.edit(mute=True)
#--------------------
#the zoo game
#--------------------
#all buttons
#--------------------
class counter(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.money = {}

    @discord.ui.button(label='+1', style=discord.ButtonStyle.blurple)
    async def plusOne(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id not in self.money.keys():
            self.money[interaction.user.id] = 0
        self.money[interaction.user.id] += (1 + (len(animal_count[interaction.user.id]) if interaction.user.id in animal_count.keys() else 0))
        embed = interaction.message.embeds[0]
        if not any(field.name == interaction.user.name for field in embed.fields):
            embed.add_field(name=interaction.user.name, value=self.money[interaction.user.id])
        else:
            index = next(i for i, field in enumerate(embed.fields) if field.name == interaction.user.name)
            embed.set_field_at(index, name=interaction.user.name, value=self.money[interaction.user.id])
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(f"you now have {self.money[interaction.user.id]} money", ephemeral=True)

class zoozoo(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.zoo = {}
        self.animals = ("monkey", "horse", "dog", "cat", "bird", "fish", "snake", "lion", "tiger", "elephant", "bear", "panda", "penguin", "cow", "pig", "chicken", "sheep", "goat", "duck", "rabbit", "big penis")

    @discord.ui.button(label='zoo button', style=discord.ButtonStyle.blurple)
    async def plusZoo(self, button: discord.ui.Button, interaction: discord.Interaction):
        already_chosen = False
        if interaction.user.id not in self.zoo.keys():
            self.zoo[interaction.user.id] = []
        choice = random.choice(self.animals)
        if choice not in self.zoo[interaction.user.id]:
            bestond = open("data/zoo.json", mode="w", encoding="utf-8")
            jeeson = json.load(bestond)
            if not jeeson[interaction.user.id].choices:
                jeeson[interaction.user.id].choices = []
            jeeson[interaction.user.id].choices.append(choice)
            bestond.write(json.dumps(jeeson))
            bestond.close()
            self.zoo[interaction.user.id].append(choice)
        else:
            already_chosen = True
        global animal_count
        animal_count = self.zoo
        embed = interaction.message.embeds[0]
        if not any(field.name == interaction.user.name for field in embed.fields):
            embed.add_field(name=interaction.user.name, value=", ".join(self.zoo[interaction.user.id]))
        else:
            index = next(i for i, field in enumerate(embed.fields) if field.name == interaction.user.name)
            embed.set_field_at(index, name=interaction.user.name, value=", ".join(self.zoo[interaction.user.id]))
        if not already_chosen:
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(f"You now have a {choice}!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already have a {choice}!", ephemeral=True)
#--------------------
#all commands using the buttons
#--------------------
@bot.command()
async def money(ctx: commands.Context):
    embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with the most money", color=discord.Color.blurple())
    await ctx.send(f"Click on button for money", embed=embed, view=counter())

@bot.command()
async def zoo(ctx):
    embed = discord.Embed(title="Leaderboard", description="Here is the leaderboard of the people with their animals", color=discord.Color.blurple())
    await ctx.send(f"Click on the button for zoo", embed=embed, view=zoozoo())
#--------------------
#the minecraft server start, stop and restart commands
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
    if current_status == "exited" or current_status == "created":
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
    Stop the Minecraft server
    """
    container: Container = dcc.containers.get(CONTAINER_NAME)
    current_status = container.status
    user = interaction.user
    if user.id == 643009066557243402:
        if current_status == "exited" or current_status == "created":
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
    Restart the Minecraft server
    """
    container: Container = dcc.containers.get(CONTAINER_NAME)
    current_status = container.status
    user = interaction.user
    if user.id == 643009066557243402:
        if current_status == "exited" or current_status == "created":
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
#mute command
#--------------------
@bot.slash_command(name="mute")
async def mute(interaction: discord.Interaction, user: discord.Member):
    """
    Mute a user
    """
    if interaction.user.id == 643009066557243402:
        global muted_user
        muted_user = user
        await user.edit(mute=True)
        await interaction.response.send_message(f"{user} has been muted!")
    else:
        await interaction.response.send_message("You don't have permission to do this!")
@bot.slash_command(name="unmute")
async def unmute(interaction: discord.Interaction, user: discord.Member):
    """
    Unmute a user
    """
    if interaction.user.id == 643009066557243402:
        global muted_user
        muted_user = None
        await user.edit(mute=False)
        await interaction.response.send_message(f"{user} has been unmuted!")
    else:
        await interaction.response.send_message("You don't have permission to do this!")
#--------------------
#runs the bot using the token loaded previously
#--------------------
bot.run(os.getenv("BOT_TOKEN"))
#--------------------