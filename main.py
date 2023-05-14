#all imports
#--------------------
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
#--------------------
#load the bot token
#--------------------
load_dotenv()
bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())
#--------------------
#sends a message to the log when the bot is ready
#--------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
#--------------------
#the commands
#--------------------
class counter(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.money = {}

    @discord.ui.button(label='+1', style=discord.ButtonStyle.blurple)
    async def plusOne(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id not in self.money.keys():
            self.money[interaction.user.id] = 0
        self.money[interaction.user.id] += 1
        embed = interaction.message.embeds[0]
        if not any(field.name == interaction.user.name for field in embed.fields):
            embed.add_field(name=interaction.user.name, value=self.money[interaction.user.id])
        else:
            index = next(i for i, field in enumerate(embed.fields) if field.name == interaction.user.name)
            embed.set_field_at(index, name=interaction.user.name, value=self.money[interaction.user.id])
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(f"Je hebt nu {self.money[interaction.user.id]} euro", ephemeral=True)

@bot.command()
async def geld(ctx: commands.Context):
    embed = discord.Embed(title="Leaderboard", description="Hier is de leaderboard van de mensen die het meeste geld hebben", color=discord.Color.blurple())
    await ctx.send(f"klik op knop voor geld", embed=embed, view=counter())
#--------------------
#runs the bot using the token loaded previously
#--------------------
bot.run(os.getenv("BOT_TOKEN"))
#--------------------