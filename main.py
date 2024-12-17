import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import re
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

with open("custom.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

allCommands = ["add", "all", "remove"];


def add_commands():
    for command, response in data.items():
        exec(f"""async def {command}(ctx): await ctx.send("{response}")""")
        bot.command(name=command)(locals()[command])


@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')
    add_commands()
    
    
@bot.command()
async def add(ctx, command: str, *args):
    response = " ".join(args)
    
    if not re.match(r'^[a-z0-9ąćęłńóśżź]+$', command) or len(response) == 0:
        await ctx.send('Komenda może mieć tylko małe litery i liczby i nie może być pusta')
        return
        
    data.update({command: response})
    
    with open("custom.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    await ctx.send('Dodano lub zaktualizowano komendę ' + command )

@bot.command()
async def all(ctx, *args):
    await ctx.send('Oto wszystkie dostępne komendy:\n' + ', '.data.keys())
    

@bot.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, command, *args):
    if command in data:
        del data[command]
        with open("custom.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        await ctx.send("Usunięto komendę " + command)
    else:
        await ctx.send("Nie ma takiej komendy w bazie")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for key, value in data.items():
        if key.lower() in message.content.lower():
            await message.channel.send(value)
            break
    await bot.process_commands(message)
        
        
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Brakuje wymaganych argumentów")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Nie ma takiej komendy")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Błąd argumentu: {error}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Musisz mieć odpowiednie uprawnienia, aby wykonać tę komendę")
    else:
        await ctx.send(f"Wystąpił błąd: {error}")




bot.run(os.getenv('DISCORD_TOKEN'))