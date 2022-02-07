from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import random
from..db import db
from discord import Embed

class Actas(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["actas"])
  async def acta(self, ctx):
      if ctx.channel.id == 878058128032288829 or ctx.channel.id == 877959989409501185:
          lowest_count = db.record("SELECT MIN(PersonaCount) FROM actas")[0]
          person_list = db.column("SELECT PersonaMention FROM actas WHERE PersonaCount = ?", lowest_count)

          chosen_person = random.choice(person_list)
          person_mention = f"<@{chosen_person}>"
          await ctx.send("La persona elegida para el acta es...")
          await ctx.send("...")
          await ctx.send("...")
          await ctx.send("...")
          await ctx.send(f"{person_mention}!!!")

          db.execute("UPDATE actas SET PersonaCount = PersonaCount + 1 WHERE PersonaMention = ?", chosen_person)
          db.commit()

          log_channel = self.bot.get_channel(877959989409501185)
          await log_channel.send(f"{ctx.message.author.mention} acaba de usar el comando de actas.")

  @command()
  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("actas")

def setup(bot):
  bot.add_cog(Actas(bot))
