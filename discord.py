import discord
from discord.ext import commands
import os
from datetime import datetime

# Configurações de Intents (necessário para o bot funcionar)
intents = discord.Intents.default()
intents.message_content = True  # Permite ler o conteúdo das mensagens
intents.members = True          # Opcional: para ver membros

# Cria o bot com prefixo "!"
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Evento: Quando o bot ficar online
@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    print(f"Servidores conectados: {len(bot.guilds)}")
    
    # Status personalizado
    await bot.change_presence(
        activity=discord.Game(name="!help | Bot feito por Ibson")
    )

# Comando simples: Olá
@bot.command(name="ola", aliases=["olá", "hello"])
async def ola(ctx):
    await ctx.send(f"👋 Olá, {ctx.author.mention}! Tudo bem?")

# Comando: Ping
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! `{latency}ms`")

# Comando: Info do servidor
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Membros", value=guild.member_count, inline=True)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    
    await ctx.send(embed=embed)

# Comando de ajuda personalizado
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📜 Comandos do Bot",
        description="Aqui estão os comandos disponíveis:",
        color=discord.Color.purple()
    )
    embed.add_field(name="!ola", value="Diz olá para você", inline=False)
    embed.add_field(name="!ping", value="Mostra a latência do bot", inline=False)
    embed.add_field(name="!serverinfo", value="Mostra informações do servidor", inline=False)
    
    await ctx.send(embed=embed)

# ========================
# RODAR O BOT
# ========================

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")  # Melhor usar variável de ambiente
    
    if not TOKEN:
        TOKEN = input("🔑 Cole seu Token do Bot aqui: ")
    
    bot.run(TOKEN)
