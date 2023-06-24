#all imports
#--------------------
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
#--------------------
#all variables
#--------------------
animal_count = {}
#--------------------
#load the bot token
#--------------------
load_dotenv()
bot = commands.Bot(
    command_prefix='!', intents = discord.Intents.all(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="/start"),
)
#--------------------
#sends a message to the log when the bot is ready
#--------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
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
#runs the bot using the token loaded previously
#--------------------
bot.run(os.getenv("BOT_TOKEN"))
#--------------------