import discord
import os
from discord import app_commands
from discord.ext import commands

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel_id = int(os.getenv("ID_CANAL_LOGS", 0))

    @commands.command(name="registrar")
    async def registrar(self, ctx, *, dados: str):
        partes = dados.split(";")

        if len(partes) < 4:
            return await ctx.send(f"{ctx.author.mention}, por favor forneça os dados no formato: `!registrar Nome;Idade;Email;Telefone`")
        
        nome = partes[0].strip()
        idade_str = partes[1].strip()
        email = partes[2].strip()
        telefone = partes[3].strip()

        # --- Validação simples para idade ---
        try:
            idade = int(idade_str)
        except ValueError:
            return await ctx.send(f"{ctx.author.mention}, a idade deve ser um número inteiro.")
        
        # --- Validação simples para email ---
        if "@" not in email or "." not in email:
            return await ctx.send(
                f"❌ {ctx.author.mention}, o e-mail informado (`{email}`) parece ser inválido. "
                f"Certifique-se de incluir o '@' e o domínio (ex: .com, .com.br)."
            )
        
        # --- Validação simples para telefone ---
        numeros_telefone = ''.join(filter(str.isdigit, telefone))
        if len(numeros_telefone) < 10:
            return await ctx.send(f"{ctx.author.mention}, o telefone informado parece ser inválido. Certifique-se de incluir o DDD e o número (ex: (11) 99999-9999).")

        canal_logs = self.bot.get_channel(self.logchannel_id)
        
        if canal_logs:
            dados_csv = f"{nome};{idade};{email};{telefone}"
            
            embed = discord.Embed(title="Novo Registro Realizado", color=discord.Color.green())
            embed.add_field(name="Usuário", value=ctx.author.mention, inline=False)
            embed.add_field(name="Dados (Formato Planilha)", value=f"```csv\n{dados_csv}\n```", inline=False)
            embed.set_footer(text="Copie a linha acima para o Excel (separador: ponto e vírgula)")
            
            await canal_logs.send(embed=embed)
            await ctx.send(f"{ctx.author.mention}, seu registro foi enviado com sucesso!")
        else:
            await ctx.send("Erro: Canal de logs não encontrado.")

    # Comando de barra (Slash)

    @app_commands.command(name="registrar", description="Realiza o registro de informações")
    async def registrar(self, interaction: discord.Interaction, nome: str, idade: int, email: str, telefone: str):

        try:
            idade = int(idade)        
        except ValueError:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}, a idade informada (`{idade}`) parece ser inválida. "
                f"Certifique-se de incluir um número inteiro.",
                ephemeral=True
            )
            return

        if "@" not in email or "." not in email:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}, o e-mail informado (`{email}`) parece ser inválido. "
                f"Certifique-se de incluir o '@' e o domínio (ex: .com, .com.br).",
                ephemeral=True
            )
            return
        
        if len(''.join(filter(str.isdigit, telefone))) < 10:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}, o telefone informado parece ser inválido. "
                f"Certifique-se de incluir o DDD e o número (ex: (11) 99999-9999).",
                ephemeral=True
            )
            return

        canal_logs = self.bot.get_channel(self.logchannel_id)
        
        if not canal_logs:
            await interaction.response.send_message("Erro: Canal de logs não configurado corretamente.", ephemeral=True)
            return

        # Formato para CSV
        dados_csv = f"{nome} \n{idade}\n \n{email}\n \n{telefone}\n"
        
        embed_log = discord.Embed(title="📝 Novo Registro", color=discord.Color.gold())
        embed_log.add_field(name="Autor", value=interaction.user.mention, inline=True)
        embed_log.add_field(name="Dados CSV", value=f"```csv\n{dados_csv}\n```", inline=False)
        
        await canal_logs.send(embed=embed_log)
        await interaction.response.send_message(f"Obrigado {nome}, seu registro foi processado!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Registro(bot))
