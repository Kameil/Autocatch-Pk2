import discord, time, re, asyncio, random, requests, sys, os
from discord.ext import commands
from unidecode import unidecode
from threading import Thread



sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # isso ai e pra tentar resolver os b.o

Arquivos = {
    'main.py': 'https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/main.py', 'bot.py': 'https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/bot.py', 'data/pokemon': 'https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/data/pokemon', 'data/legendary': 'https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/data/legendary', 'data/mythical': 'https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/data/mythical'
    }


# bota os CATCH ID AI TA LIGADO PQ OREA SECA E DESENROLADO

catch_ids = []

from config import *

for catch_id in [catch_id, catch_id2, catch_id3, catch_id4, catch_id5, catch_id6]:
    catch_ids.append(catch_id)

catch_ids = [catch_id for catch_id in catch_ids if catch_id != '']

pokemon_file = os.path.join(os.path.dirname(__file__), "data/pokemon")
with open(pokemon_file, 'r', encoding='utf8') as file:
    pokemon_list = file.read()

def CarregarPokemons():
    global pokemon_list
    print('Carregando lista dos Pokemons..')
    try:
        # vai ate a url dos pikomon e ver os pokemon q ta la ta ligado
        url = Arquivos['data/pokemon']
        pokemons = requests.get(url)
        if pokemons.status_code == 200:
            # os.path.join(os.path.dirname(__file__), "data/pokemon") e pra ser o patch onde o data/pokemon esta
            with open(os.path.join(os.path.dirname(__file__), "data/pokemon"), 'w', encoding='utf8') as PokemonList:
                PokemonList.write(pokemons.text)
                print('lista dos pokemons atualizada.')
        else:
            print('nao foi possivel atualizar a lista dos pokemons.')
    except:
        pass
    with open(os.path.join(os.path.dirname(__file__), "data/pokemon"), 'r', encoding='utf8') as file:
        pokemon_list = file.read()

Thread(target=CarregarPokemons).start()




def decidirtimesleep():
    return 0

mitico = os.path.join(os.path.dirname(__file__), "data/mythical")
tolevel = os.path.join(os.path.dirname(__file__), "data/level")       # os path ai de cria
legend = os.path.join(os.path.dirname(__file__), "data/legendary")

with open(legend, 'r') as file:
    legendary_list = file.read()
with open(mitico, 'r') as file:
    mythical_list = file.read()
with open(tolevel, 'r') as file:
    to_level = file.readline()

# 3 kilo de variavel inutil para remover talvez em outra versao

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0
captcha_content = None
captcha = False
poketwo = 716390085896962058
Mpoketwo = "<@" + str(poketwo) + ">"


# CLIENT TA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
client = commands.Bot(command_prefix=[f"{prefix} ", f"{prefix}"], help_command=None)



def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^' + hint_replaced + '$', pokemon_list, re.MULTILINE)
    return solution

async def Infolatest(message: discord.Message):
    async with message.channel.typing():
        await asyncio.sleep(random.uniform(0.5, 1.3))
        await message.channel.send(f"{Mpoketwo} i l")
paused = False

@client.event
async def on_ready():
    print((f'Autocatch em execuçao em : {client.user.name}', 'black', 'on_white'))
    try:
        channel = client.get_channel(int(catch_ids[0]))
        if channel:
            await asyncio.sleep(2)
            pro = ["autocatch online.", "ac online", "ac on", "autocatch on"]
            await channel.send(random.choice(pro))
        else:
            print((f"Nao foi possivel obter o canal: {catch_id}!", "red"))
    except Exception as e:
        print((f"Ocorreu um erro: {e}", "red")) 
    
def limpar_texto(texto: str): 
    texto_sem_emojis = texto.replace('♀️', '').replace('♂️', '') 
    texto_limpo = unidecode(texto_sem_emojis)
    return texto_limpo

@client.event
async def on_message(message : discord.Message):
    global paused, captcha_content, captcha
    if str(message.channel.id) in catch_ids:
        if message.author.id == poketwo:
            if not paused:
                if message.embeds:
                    embed_title = message.embeds[0].title
                    if 'wild pokémon has appeared!' in embed_title:
                        async with message.channel.typing():
                            await asyncio.sleep(random.randint(1, 5))
                            await message.channel.send(f'{Mpoketwo} h')
                else:
                    content = message.content
                    if 'The pokémon is ' in content:
                        if not len(solve(content)):
                            print('Pokemon not found.')
                        else:
                            for i in solve(content):
                                async with message.channel.typing():
                                    timesleep = random.uniform(0.8, 2.3)
                                    pokemon_name = limpar_texto(i.lower())
                                    await asyncio.sleep(timesleep)
                                    await message.channel.send(f'{Mpoketwo} c {pokemon_name}')
                    elif 'Congratulations' in content:
                        global num_pokemon
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!', '')
                        pokemon = pokemon.split("<")[0]
                        print(f'Numero de Pokemons Pegos/Ultimo Pego: {num_pokemon} :{pokemon}')
                        if random.randint(1, 10) == 10 and not paused:
                            await Infolatest(message)
                    elif 'human' in content:
                        paused, captcha = True, True
                        captcha_content = message.content
                        async with message.channel.typing():
                            await asyncio.sleep(random.uniform(0.5,3.5))
                            await message.channel.send(f'<@{ping}> Captcha Detectado! Bot pausado.')
                        
    if not message.author.bot:
        await client.process_commands(message)
  
"""
Comando desativado
@client.command()
async def say(ctx, *, args):
    if str(ctx.channel.id) in str(catch_ids):
        await ctx.send(args)
"""

@client.command()
async def p(ctx, method: str = None, arg1: str = None):
    methods = ["tri", "quad", "iv"]
    if method is None:
        return await ctx.send(f"{Mpoketwo}p")
    if method in methods and arg1 is not None:
        if method == "tri":
            await ctx.send(f"{Mpoketwo}p --{method} {arg1}")
        if method == "quad":
            await ctx.send(f"{Mpoketwo}p --{method} {arg1}")
        if method == "iv":
            if arg1 == "menor" or arg1 == "<":
                await ctx.send(f"{Mpoketwo}p --iv < 10")
            if arg1 == "maior" or arg1 == ">":
                await ctx.send(f"{Mpoketwo}p --iv > 90")
    else:
        await ctx.send("Metodo nao encontrado")


@client.command()
async def i(ctx, num = None):
    if num is not None:
        await ctx.send(f"{Mpoketwo}i {num}")
    await ctx.send(f"{Mpoketwo} i l")

@client.command()
async def start(ctx):
    global paused
    async with ctx.typing():
        if str(ctx.channel.id) in catch_ids:
            await asyncio.sleep(random.uniform(0.5, 0.9))
            if not paused:
                await ctx.send('Bot ja esta em Execuçao.')
            else:
                paused = False
                await ctx.send('Bot Iniciado.')

@client.command()
async def stop(ctx):
    global paused
    async with ctx.typing():
        if str(ctx.channel.id) in catch_ids:
            await asyncio.sleep(random.uniform(0.5, 0.9))
            if not paused:
                paused = True
                await ctx.send('Bot Pausado.')
            else:
                await ctx.send('Bot Ja esta pausado.')
      


version = '3.1'      

def Alerts():
    time.sleep(1)
    print(f"Poketwo Autocatcher V{version}") 

    

def ProcurarAtualizaçoes():
    requisicoes = 1
    time.sleep(60)
    while True:
        for file, url in Arquivos.items():
            requisicoes += 1
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(os.path.dirname(__file__), file), 'w', encoding="utf-8") as arch:
                    arch.write(response.text)
        time.sleep(600)


Thread(target=Alerts).start()
Thread(target=ProcurarAtualizaçoes).start()
try:
    client.run(f"{user_token}")
except discord.HTTPException as e:
    if e.status == 429:
        print(('Discord Recusou a Conexao com o Codigo De status: 429 too many requests.\n', 'red'), str(e))
        """
        FlasK.terminate()
        """
