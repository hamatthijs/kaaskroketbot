import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()
money = 0
bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')

class InviteButtons(discord.ui.View):
    def __init__(self, inv: str):
        global money
        super().__init__()
        self.inv = inv

    @discord.ui.button(label='Invite Btn', style=discord.ButtonStyle.blurple)
    async def inviteBtn(self, button: discord.ui.Button, interaction: discord.Interaction):
        global money
        money = money + 1
        await interaction.response.send_message(f"je hebt nu {money} euro", ephemeral=True)

@bot.command()
async def invite(ctx: commands.Context):
    inv = await ctx.channel.create_invite()
    await ctx.send(f"je hebt {money} euro stoopid. Klik deze knop voor meer", view=InviteButtons(str(inv)))

bot.run(os.getenv("BOT_TOKEN"))