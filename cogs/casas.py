import discord
from discord.ext import commands
from discord import app_commands

class Casas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listarcasas")
    async def casas_prefix(self, ctx):
        embed = discord.Embed(
            title="🏠 Casas Disponíveis",
            description="Aqui estão as casas que você pode escolher:",
            color=discord.Color.gold())
        embed.add_field(name="BetVip", value="[Acesse aqui](https://betvip.bet.br/)", inline=False)
        embed.add_field(name="R7 Bet", value="[Acesse aqui](https://r7.bet.br/pb/)", inline=False)
        embed.add_field(name="7Games", value="[Acesse aqui](https://7games.bet.br/pb/)", inline=False)
        embed.add_field(name="BetMGM", value="[Acesse aqui](https://betmgm.bet.br/)", inline=False)
        embed.add_field(name="Donos da Bola", value="[Acesse aqui](https://donosdabola.bet.br/)", inline=False)
        embed.add_field(name="Lance de Sorte", value="[Acesse aqui](https://lancedesorte.bet.br/)", inline=False)
        embed.add_field(name="Aposta Ganha", value="[Acesse aqui](https://apostaganha.bet.br/)", inline=False)
        embed.add_field(name="KTO", value="[Acesse aqui](https://kto.bet.br/)", inline=False)
        embed.add_field(name="Sportingbet", value="[Acesse aqui](https://sportingbet.bet.br/)", inline=False)
        embed.add_field(name="Betsson", value="[Acesse aqui](https://betsson.bet.br/)", inline=False)
        embed.add_field(name="BetWarrior", value="[Acesse aqui](https://betwarrior.bet.br/)", inline=False)
        embed.add_field(name="Vera", value="[Acesse aqui](https://vera.bet.br/)", inline=False)
        embed.add_field(name="Luva", value="[Acesse aqui](https://luva.bet.br/)", inline=False)
        embed.add_field(name="Betano", value="[Acesse aqui](https://betano.bet.br/)", inline=False)
        embed.add_field(name="Superbet", value="[Acesse aqui](https://superbet.bet.br/)", inline=False)
        embed.add_field(name="BetEsporte", value="[Acesse aqui](https://betesporte.bet.br/)", inline=False)
        embed.add_field(name="Betfair", value="[Acesse aqui](https://www.betfair.bet.br/)", inline=False)

        await ctx.send(embed=embed)

    # Comando de Casas (Slash)

    @app_commands.command(name="listarcasas", description="Mostra as casas disponíveis para apostar")
    async def casas(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏠 Casas Disponíveis",
            description="Aqui estão as casas que você pode escolher:",
            color=discord.Color.gold()
        )
        embed.add_field(name="BetVip", value="[Acesse aqui](https://betvip.bet.br/)", inline=False)
        embed.add_field(name="R7 Bet", value="[Acesse aqui](https://r7.bet.br/pb/)", inline=False)
        embed.add_field(name="7Games", value="[Acesse aqui](https://7games.bet.br/pb/)", inline=False)
        embed.add_field(name="BetMGM", value="[Acesse aqui](https://betmgm.bet.br/)", inline=False)
        embed.add_field(name="Donos da Bola", value="[Acesse aqui](https://donosdabola.bet.br/)", inline=False)
        embed.add_field(name="Lance de Sorte", value="[Acesse aqui](https://lancedesorte.bet.br/)", inline=False)
        embed.add_field(name="Aposta Ganha", value="[Acesse aqui](https://apostaganha.bet.br/)", inline=False)
        embed.add_field(name="KTO", value="[Acesse aqui](https://kto.bet.br/)", inline=False)
        embed.add_field(name="Sportingbet", value="[Acesse aqui](https://sportingbet.bet.br/)", inline=False)
        embed.add_field(name="Betsson", value="[Acesse aqui](https://betsson.bet.br/)", inline=False)
        embed.add_field(name="BetWarrior", value="[Acesse aqui](https://betwarrior.bet.br/)", inline=False)
        embed.add_field(name="Vera", value="[Acesse aqui](https://vera.bet.br/)", inline=False)
        embed.add_field(name="Luva", value="[Acesse aqui](https://luva.bet.br/)", inline=False)
        embed.add_field(name="Betano", value="[Acesse aqui](https://betano.bet.br/)", inline=False)
        embed.add_field(name="Superbet", value="[Acesse aqui](https://superbet.bet.br/)", inline=False)
        embed.add_field(name="BetEsporte", value="[Acesse aqui](https://betesporte.bet.br/)", inline=False)
        embed.add_field(name="Betfair", value="[Acesse aqui](https://www.betfair.bet.br/)", inline=False)
        
        await interaction.response.send_message(embed=embed) 

async def setup(bot):
    await bot.add_cog(Casas(bot))