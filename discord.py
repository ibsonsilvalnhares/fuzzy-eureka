# boot.py
import discord
from discord.ext import commands
import json
import os
from datetime import datetime

# Configurações
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Arquivo para salvar o catálogo
DATA_FILE = "catalogo_vendas.json"

# Carregar catálogo
def load_catalog():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"produtos": []}

# Salvar catálogo
def save_catalog(catalog):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=4)

catalog = load_catalog()

# ====================== COMANDOS DE ADMIN ======================

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    print(f"📦 Catálogo carregado com {len(catalog['produtos'])} produtos.")

# Adicionar produto
@bot.command(name="addprod")
@commands.has_permissions(administrator=True)
async def add_produto(ctx, nome: str, preco: float, estoque: int, *, descricao: str = "Sem descrição"):
    produto = {
        "id": len(catalog["produtos"]) + 1,
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
        "descricao": descricao,
        "adicionado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    catalog["produtos"].append(produto)
    save_catalog(catalog)
    
    embed = discord.Embed(title="✅ Produto Adicionado", color=0x00ff00)
    embed.add_field(name="ID", value=produto["id"], inline=True)
    embed.add_field(name="Produto", value=nome, inline=True)
    embed.add_field(name="Preço", value=f"R$ {preco:.2f}", inline=True)
    embed.add_field(name="Estoque", value=estoque, inline=True)
    embed.add_field(name="Descrição", value=descricao, inline=False)
    
    await ctx.send(embed=embed)

# Ver catálogo
@bot.command(name="catalogo")
async def ver_catalogo(ctx):
    if not catalog["produtos"]:
        return await ctx.send("📭 Catálogo vazio no momento.")
    
    embed = discord.Embed(title="🛒 Catálogo de Vendas", color=0x1e90ff)
    for p in catalog["produtos"]:
        embed.add_field(
            name=f"#{p['id']} - {p['nome']}",
            value=f"**Preço:** R$ {p['preco']:.2f}\n"
                  f"**Estoque:** {p['estoque']}\n"
                  f"**Desc:** {p['descricao'][:100]}...",
            inline=False
        )
    await ctx.send(embed=embed)

# Remover produto
@bot.command(name="delprod")
@commands.has_permissions(administrator=True)
async def remover_produto(ctx, id_produto: int):
    for i, p in enumerate(catalog["produtos"]):
        if p["id"] == id_produto:
            removido = catalog["produtos"].pop(i)
            save_catalog(catalog)
            await ctx.send(f"🗑️ Produto **{removido['nome']}** (ID: {id_produto}) removido com sucesso!")
            return
    await ctx.send("❌ Produto não encontrado.")

# Editar produto
@bot.command(name="editprod")
@commands.has_permissions(administrator=True)
async def editar_produto(ctx, id_produto: int, campo: str, *, valor):
    campos_validos = ["nome", "preco", "estoque", "descricao"]
    
    if campo not in campos_validos:
        return await ctx.send(f"❌ Campo inválido. Use: {', '.join(campos_validos)}")
    
    for p in catalog["produtos"]:
        if p["id"] == id_produto:
            if campo == "preco":
                p[campo] = float(valor)
            elif campo == "estoque":
                p[campo] = int(valor)
            else:
                p[campo] = valor
                
            save_catalog(catalog)
            await ctx.send(f"✏️ Produto **{p['nome']}** atualizado! `{campo}` = `{valor}`")
            return
    
    await ctx.send("❌ Produto não encontrado.")

# ====================== ERRO DE PERMISSÃO ======================
@add_produto.error
@remover_produto.error
@editar_produto.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 Apenas **Administradores** podem usar este comando.")

# ====================== RODAR O BOT ======================
if __name__ == "__main__":
    TOKEN = "SEU_TOKEN_AQUI"  # ← Coloque seu token aqui
    bot.run(TOKEN)
