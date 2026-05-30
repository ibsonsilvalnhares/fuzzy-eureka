import discord
from discord.ext import commands

TOKEN = "SEU_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# CATÁLOGO
catalogo = {
    "Netflix": "R$ 15",
    "Spotify": "R$ 10",
    "Disney+": "R$ 12"
}

@bot.command()
async def catalogo(ctx):
    texto = "**📦 Catálogo da Loja**\n\n"

    for produto, preco in catalogo.items():
        texto += f"• {produto} - {preco}\n"

    await ctx.send(texto)

@bot.command()
async def comprar(ctx, *, produto):
    await ctx.send(
        f"✅ Pedido de **{produto}** registrado por {ctx.author.mention}"
    )

# COMANDOS ADM

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Sem motivo"):
    await membro.ban(reason=motivo)
    await ctx.send(f"🔨 {membro} foi banido.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo="Sem motivo"):
    await membro.kick(reason=motivo)
    await ctx.send(f"👢 {membro} foi expulso.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(
        f"🧹 {quantidade} mensagens removidas.",
        delete_after=5
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def anunciar(ctx, *, mensagem):
    await ctx.send(f"📢 {mensagem}")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

bot.run(TOKEN)
