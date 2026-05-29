**✅ Aqui está um código completo e atualizado para criar um Bot de Discord em Python (discord.py)**

### 1. Primeiro, instale as dependências:

```bash
pip install discord.py
```

---

### 2. Código do Bot (bot.py)

```python
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
```

---

### 3. Como criar o Bot no Discord

1. Acesse: [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em **New Application**
3. Vá em **Bot** → **Add Bot**
4. Copie o **Token** (guarde com segurança!)
5. Ative as **Privileged Gateway Intents**:
   - `PRESENCE INTENT`
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`

---

### 4. Como rodar o bot

```bash
python bot.py
```

---

### Dicas extras:

- **Usar .env** (mais seguro):
  ```bash
  pip install python-dotenv
  ```

  Crie um arquivo `.env`:
  ```env
  DISCORD_TOKEN=seu_token_aqui
  ```

- Quer que eu adicione alguma funcionalidade específica?
  - Sistema de níveis
  - Moderação (ban, kick, mute)
  - Música
  - Economia (carteira)
  - Tickets
  - Slash Commands (moderna)

É só falar o que você quer que eu melhore ou adicione no bot! 🚀
