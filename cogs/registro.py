import discord
import os
from discord import app_commands
from discord.ext import commands

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel_id = int(os.getenv("ID_CANAL_LOGS", 0))

    @commands.command(name="registrar")
    async def registrar(self, ctx, nome: str, idade: int, email: str, telefone: str):
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

    @app_commands.command(name="ajuda", description="Mostra como usar os comandos do bot")
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Guia de Comandos",
            description="Aqui estão as instruções para utilizar as funções do bot:",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="/registrar", 
            value="Inicia seu cadastro.\n**Uso:** `/registrar nome: João idade: 25 email: joao@email.com telefone: (11) 99999-9999`", 
            inline=False
        )
        embed.add_field(
            name="/definirjogo", 
            value="Escolhe um jogo aleatório entre as opções enviadas.\n**Uso:** `/definirjogo opcoes: LoL, CS, Valorant`", 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

    # Comando de Registro (Slash)
    @app_commands.command(name="registrar", description="Realiza o registro de informações")
    async def registrar(self, interaction: discord.Interaction, nome: str, idade: int, email: str, telefone: str):
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