import discord
from discord.ext import commands
from discord import app_commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando de Prefixo (!ajuda)
    @commands.command(name="ajuda")
    async def ajuda_prefixo(self, ctx):
        embed = discord.Embed(
            title="📚 Guia de Comandos",
            description="Aqui estão as instruções para utilizar as funções do bot:",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="/registrar ou !registrar", 
            value="Inicia seu cadastro.\n**Uso:** `/registrar nome: João idade: 25 email: joao@email.com telefone: (11) 99999-9999`", 
            inline=False
        )
        embed.add_field(
            name="/definirjogo ou !definirjogo", 
            value="Escolhe um jogo aleatório entre as opções enviadas.\n**Uso:** `/definirjogo opcoes: Fla x Flu` ou `!definirjogo Pal x Cor`", 
            inline=False
        )
        embed.add_field(
            name="/listarcasas ou !listarcasas", 
            value="Mostra as casas de apostas disponíveis.\n**Uso:** `/listarcasas` ou `!listarcasas`", 
            inline=False
        )
        embed.set_footer(text="Use os comandos com barra (/) para uma experiência otimizada!")
        
        await ctx.send(embed=embed)

    # Comando de Barra (/ajuda)
    @app_commands.command(name="ajuda", description="Mostra como usar os comandos do bot")
    async def ajuda_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Guia de Comandos",
            description="Aqui estão as instruções para utilizar as funções do bot:",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="/registrar ou !registrar", 
            value="Inicia seu cadastro.\n**Uso:** `/registrar nome: João idade: 25 email: joao@email.com telefone: (11) 99999-9999`", 
            inline=False
        )
        embed.add_field(
            name="/definirjogo ou !definirjogo", 
            value="Escolhe um jogo aleatório entre as opções enviadas.\n**Uso:** `/definirjogo opcoes: Fla x Flu, Palmeiras x Corinthians` ou `!definirjogo Fla x Flu`", 
            inline=False
        )
        embed.add_field(
            name="/listarcasas ou !listarcasas", 
            value="Mostra as casas de apostas disponíveis.\n**Uso:** `/listarcasas` ou `!listarcasas`", 
            inline=False
        )
        embed.set_footer(text="Use os comandos com barra (/) para uma experiência otimizada!")
        
        await interaction.response.send_message(embed=embed)

# Função obrigatória para carregar a Cog
async def setup(bot):
    await bot.add_cog(Ajuda(bot))