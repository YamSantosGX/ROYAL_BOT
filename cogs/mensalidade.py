import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta

class MensalidadeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Substitua pelo ID real do seu cargo
        self.CARGO_MENSALIDADE_ID = 1478286792930230353

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Separa as listas de cargos que acabaram de ser adicionados ou removidos
        cargos_adicionados = [cargo for cargo in after.roles if cargo not in before.roles]
        cargos_removidos = [cargo for cargo in before.roles if cargo not in after.roles]

        # --- LÓGICA 1: QUANDO O CARGO É ADICIONADO ---
        for cargo in cargos_adicionados:
            if cargo.id == self.CARGO_MENSALIDADE_ID:
                data_futura = datetime.now() + relativedelta(months=1)
                data_formatada = data_futura.strftime("%d/%m")
                nome_atual = after.display_name
                
                if data_formatada not in nome_atual:
                    novo_nome = f"{nome_atual} {data_formatada}"
                    
                    if len(novo_nome) > 32:
                        novo_nome = novo_nome[:32]
                    
                    try:
                        await after.edit(nick=novo_nome)
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para alterar o nick de {after.name}.')
                    except Exception as e:
                        print(f'[Erro] Falha ao alterar nick de adição: {e}')
                break 

        # --- LÓGICA 2: QUANDO O CARGO É REMOVIDO ---
        for cargo in cargos_removidos:
            if cargo.id == self.CARGO_MENSALIDADE_ID:
                nome_atual = after.display_name
                
                # Procura um espaço seguido de 2 números, barra e 2 números no final do nome (Ex: " 26/01") e apaga
                novo_nome = re.sub(r'\s\d{2}/\d{2}$', '', nome_atual)
                
                if novo_nome != nome_atual:
                    try:
                        # Se o novo apelido for idêntico ao nome de usuário original (sem o discriminador), 
                        # passar None reseta o apelido para o padrão do Discord.
                        if novo_nome == after.name:
                            await after.edit(nick=None)
                        else:
                            await after.edit(nick=novo_nome)
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para resetar o nick de {after.name}.')
                    except Exception as e:
                        print(f'[Erro] Falha ao resetar nick na remoção: {e}')
                break 
    
    @commands.command(name="sincronizar_mensalidades", help="Sincroniza os apelidos com as datas de mensalidade.")
    @commands.has_permissions(administrator=True) # Apenas administradores podem usar
    async def sincronizar_mensalidades(self, ctx):
        await ctx.send("⏳ Iniciando varredura de membros... Isso pode levar alguns segundos.")
        
        adicionados = 0
        removidos = 0
        
        # Busca o objeto do cargo no servidor atual
        cargo_mensalidade = ctx.guild.get_role(self.CARGO_MENSALIDADE_ID)
        
        if not cargo_mensalidade:
            return await ctx.send("❌ Erro: Cargo não encontrado. Verifique o ID.")

        # Percorre todos os membros do servidor
        for member in ctx.guild.members:
            nome_atual = member.display_name
            
            # --- CENÁRIO 1: O membro TEM o cargo, mas NÃO TEM a data ---
            if cargo_mensalidade in member.roles:
                # Verifica se NÃO existe uma data no final do nome (ex: " 26/01")
                if not re.search(r'\s\d{2}/\d{2}$', nome_atual):
                    # Como não sabemos o dia exato que ele ganhou o cargo no passado, 
                    # adicionamos 1 mês a partir de hoje por padrão.
                    data_futura = datetime.now() + relativedelta(months=1)
                    data_formatada = data_futura.strftime("%d/%m")
                    
                    novo_nome = f"{nome_atual} {data_formatada}"
                    if len(novo_nome) > 32:
                        novo_nome = novo_nome[:32]
                    
                    try:
                        await member.edit(nick=novo_nome)
                        adicionados += 1
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para alterar: {member.name}')
                    except Exception:
                        pass
                        
            # --- CENÁRIO 2: O membro NÃO TEM o cargo, mas TEM a data presa no nome ---
            else:
                if re.search(r'\s\d{2}/\d{2}$', nome_atual):
                    novo_nome = re.sub(r'\s\d{2}/\d{2}$', '', nome_atual)
                    try:
                        if novo_nome == member.name:
                            await member.edit(nick=None)
                        else:
                            await member.edit(nick=novo_nome)
                        removidos += 1
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para alterar: {member.name}')
                    except Exception:
                        pass

        # Envia o resumo final no chat
        await ctx.send(
            f"✅ **Sincronização concluída!**\n"
            f"🔹 Datas adicionadas: `{adicionados}`\n"
            f"🔻 Datas removidas: `{removidos}`"
        )

    # Comando de Sincronização (Slash)
    @app_commands.command(name="sincronizar_mensalidades", description="Sincroniza os apelidos com as datas de mensalidade.")
    @app_commands.checks.has_permissions(administrator=True) # Apenas administradores podem usar
    async def sincronizar_mensalidades_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message("⏳ Iniciando varredura de membros... Isso pode levar alguns segundos.", ephemeral=True)
        
        adicionados = 0
        removidos = 0
        
        cargo_mensalidade = interaction.guild.get_role(self.CARGO_MENSALIDADE_ID)
        
        if not cargo_mensalidade:
            return await interaction.followup.send("❌ Erro: Cargo não encontrado. Verifique o ID.", ephemeral=True)

        for member in interaction.guild.members:
            nome_atual = member.display_name
            
            if cargo_mensalidade in member.roles:
                if not re.search(r'\s\d{2}/\d{2}$', nome_atual):
                    data_futura = datetime.now() + relativedelta(months=1)
                    data_formatada = data_futura.strftime("%d/%m")
                    
                    novo_nome = f"{nome_atual} {data_formatada}"
                    if len(novo_nome) > 32:
                        novo_nome = novo_nome[:32]
                    
                    try:
                        await member.edit(nick=novo_nome)
                        adicionados += 1
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para alterar: {member.name}')
                    except Exception:
                        pass
                        
            else:
                if re.search(r'\s\d{2}/\d{2}$', nome_atual):
                    novo_nome = re.sub(r'\s\d{2}/\d{2}$', '', nome_atual)
                    try:
                        if novo_nome == member.name:
                            await member.edit(nick=None)
                        else:
                            await member.edit(nick=novo_nome)
                        removidos += 1
                    except discord.Forbidden:
                        print(f'[Aviso] Sem permissão para alterar: {member.name}')
                    except Exception:
                        pass

        await interaction.followup.send(
            f"✅ **Sincronização concluída!**\n"
            f"🔹 Datas adicionadas: `{adicionados}`\n"
            f"🔻 Datas removidas: `{removidos}`",
            ephemeral=True
        )


# Função de setup obrigatória para carregar a Cog no main.py
async def setup(bot):
    await bot.add_cog(MensalidadeCog(bot))