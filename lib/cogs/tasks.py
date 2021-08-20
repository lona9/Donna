from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from discord.utils import get
from discord import Embed
from..db import db

class Tasks(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command("help")

  @command(aliases=["help"])
  async def ayuda(self, ctx):
      embed = Embed()

      fields = [("Hola!", "Soy Donna, la bot asistente de este server. Estos son los comandos que puedes utilizar para acceder a mis funciones:", False),
      ("Para tareas realizadas", "**$t:**: usa este comando para agregar una tarea realizada a tu lista.\n**$hoy:** usa este comando para ver tus tareas realizadas durante el día.\n**$semana:** usa este comando para ver tus tareas realizadas durante la semana.\nEn ambos comandos de resumen, puedes reaccionar con :x: para eliminarlos de tu lista.", False),
      ("Para recordatorios", "**$r:** usa este comando para programar recordatorios. El input toma la cantidad de tiempo, la unidad de tiempo en segundos (s), minutos (m), horas (h) o días (d), y el texto recordatorio. Por ejemplo: *$r 30m sacar ropa de la lavadora*.", False)]

      for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)

      embed.set_author(name='Donna', icon_url="https://cdn.discordapp.com/attachments/804477811574308864/878116460478730270/Captura_de_Pantalla_2021-08-19_a_las_22.49.19.png")

      await ctx.channel.send(embed=embed)

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
                taskmsg = await ctx.send(task)
                await taskmsg.add_reaction("❌")

  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
      if payload.member.bot:
          pass
      else:
          if payload.emoji.name == "❌":
              try:
                  channel = self.bot.get_channel(payload.channel_id)
                  message = await channel.fetch_message(payload.message_id)
                  content = message.content

                  db.execute("DELETE FROM tasks WHERE TaskText = ?", content)
                  db.commit()

              except:
                  pass

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
                taskmsg = await ctx.send(task)
                await taskmsg.add_reaction("❌")

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tasks")

def setup(bot):
  bot.add_cog(Tasks(bot))
