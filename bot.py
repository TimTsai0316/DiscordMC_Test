import discord
from discord.ext import commands, pages
import datetime
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = ',', intents=intents)

mc_server_ip = "whatisthis.myddns.me"

class MyView(discord.ui.View):
    @discord.ui.button(label="重新整理", style=discord.ButtonStyle.primary, emoji="🔁")
    async def button_callback(self, button, interaction):
        r = requests.get("https://sr-api.sfirew.com/server/" + mc_server_ip)
        doc = json.loads(r.text)
        embed=discord.Embed(title="Server Status", color=0x00ff00, timestamp=datetime.datetime.now())
        embed.set_author(name=mc_server_ip)

        if r.status_code == requests.codes.ok:
            if doc['online']:
                embed.add_field(name="上線狀態", value="🟢 上線中", inline=True)

                playerCount = doc['players']['online']
                playersList = []
                playersCount = 0
                playersStr = ""
                for i in doc['players']['sample']:
                    playersList.append(doc['players']['sample'][playersCount]['name'])
                    playersCount = playersCount + 1

                embed.add_field(name="上線人數", value=str(playersCount), inline=True)
                playersList.sort()
                for j in playersList:
                    playersStr = playersStr + j + "\n"

                embed.add_field(name="上線中玩家", value=playersStr, inline=False)
            else:
                embed.add_field(name="上線狀態", value="🔴 離線中", inline=False)
                embed.color = 0xff0000

            await interaction.message.edit(embed=embed, view = MyView())

        else:
            reply = "伺服器無法存取資料，請稍後再試。"
            await interaction.message.edit(reply, view = MyView())
        await interaction.response.defer()
        

        

@bot.event  # 上線中提示
async def on_ready():
    print(f"<<< {bot.user} 已成功連線至 Discord >>>")

@bot.slash_command(name="mc_server_status", description="更新 Minecraft 伺服器狀態")
async def mc_server_status(ctx):
    channel = ctx.channel
    r = requests.get("https://sr-api.sfirew.com/server/" + mc_server_ip)
    doc = json.loads(r.text)
    embed=discord.Embed(title="Server Status", color=0x00ff00, timestamp=datetime.datetime.now())
    embed.set_author(name=mc_server_ip)

    if r.status_code == requests.codes.ok:
        if doc['online']:
            embed.add_field(name="上線狀態", value="🟢 上線中", inline=True)

            playerCount = doc['players']['online']
            playersList = []
            playersCount = 0
            playersStr = ""
            for i in doc['players']['sample']:
                playersList.append(doc['players']['sample'][playersCount]['name'])
                playersCount = playersCount + 1

            embed.add_field(name="上線人數", value=str(playersCount), inline=True)
            playersList.sort()
            for j in playersList:
                playersStr = playersStr + j + "\n"

            embed.add_field(name="上線中玩家", value=playersStr, inline=False)
        else:
            embed.add_field(name="上線狀態", value="🔴 離線中", inline=False)
            embed.color = 0xff0000

        await channel.send(embed=embed, view = MyView())

    else:
        reply = "伺服器無法存取資料，請稍後再試。"
        await channel.send(reply, view = MyView())

    await ctx.respond("已新增狀態訊息。", ephemeral = True)

bot.run(os.getenv('TOKEN'))