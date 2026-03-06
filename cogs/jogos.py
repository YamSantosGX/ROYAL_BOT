import discord
import random
from discord import app_commands
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jogo_atual = "Nenhum jogo definido"

    @commands.command(name='definirjogo')
    @commands.has_permissions(administrator=True) # Apenas ADMs podem mudar
    async def setgame_prefix(self, ctx, *, nome_do_jogo: str):
        self.jogo_atual = nome_do_jogo
        if not nome_do_jogo:
            await ctx.send("Por favor, forneça o nome do jogo. Uso: `!definirjogo <nome do jogo>`")
            return
        await self.bot.change_presence(activity=discord.Game(name=nome_do_jogo))
        await ctx.send(f"🎮 O jogo definido: **{nome_do_jogo}**")

    @commands.command(name='jogo')
    async def getgame_prefix(self, ctx):
        
        if isinstance(self.jogo_atual, str):
            await ctx.send(f"🎮 O jogo atual é: **{self.jogo_atual}**")
        else:
            await ctx.send("🎮 No momento não temos nenhum jogo específico.")

    # Comando de Jogo (Slash)
    
    @app_commands.command(name="definirjogo", description="Define o jogo que está rolando")
    @app_commands.describe(nome="Nome do jogo que será definido")
    async def definirjogo(self, interaction: discord.Interaction, nome: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
            return
        self.jogo_atual = nome
        await self.bot.change_presence(activity=discord.Game(name=nome))
        await interaction.response.send_message(f"🎮 O jogo definido: **{nome}**!")
    
    @app_commands.command(name="jogo", description="Mostra qual o jogo está rolando no palco")
    async def jogo(self, interaction: discord.Interaction):
        if self.jogo_atual != "Nenhum jogo definido":
            await interaction.response.send_message(f"🎮 O jogo atual é: **{self.jogo_atual}**")
        else:
            await interaction.response.send_message("🎮 No momento não temos nenhum jogo específico.")


async def setup(bot):
    await bot.add_cog(Games(bot))