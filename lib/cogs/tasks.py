from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from discord.utils import get
from..db import db

class Tasks(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["t"])
  async def set_task(self, ctx, *args):

      tasktext = str(" ".join(args))

      taskid = str(ctx.author) + "-" + datetime.now().strftime("%d/%m %H:%M:%S")

      taskday = datetime.now().strftime("%d/%m")

      taskweek = datetime.now().strftime("%Y/W%V")

      taskmention = ctx.message.author.mention

      db.execute("INSERT OR IGNORE INTO tasks (TaskID, TaskDay, TaskWeek, TaskText, TaskMention) VALUES (?, ?, ?, ?, ?)", taskid, taskday, taskweek, tasktext,taskmention)

      db.commit()

      await ctx.channel.send("Agregado!")


  @command(aliases=["hoy"])
  async def today(self, ctx):
      author = ctx.message.author.mention

      today = datetime.now().strftime("%d/%m")

      tasks = db.column("SELECT TaskText FROM tasks WHERE TaskMention = ? and TaskDay = ?", author, today)

      if tasks == []:
          await ctx.send("No hay tareas realizadas hoy.")

      else:
          await ctx.send(f"{author}, **esto es lo que has hecho hoy:**")

          for task in tasks:
                await ctx.send(task)

  @command(aliases=["semana"])
  async def week(self, ctx):
      author = ctx.message.author.mention

      week = datetime.now().strftime("%Y/W%V")

      tasks = db.column("SELECT TaskText FROM tasks WHERE TaskMention = ? and TaskWeek = ?", author, week)

      if tasks == []:
          await ctx.send("No hay tareas realizadas esta semana.")

      else:
          await ctx.send(f"{author}, **esto es lo que has hecho esta semana:**")

          for task in tasks:
                await ctx.send(task)

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tasks")

def setup(bot):
  bot.add_cog(Tasks(bot))
