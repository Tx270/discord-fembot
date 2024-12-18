import discord
from discord.ext import commands
from dotenv import load_dotenv
import praw
import json
import re
import os
import random
import requests

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="Fembot/1.0"
)

with open("custom.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
    
allCommands = ["add", "all", "remove", "story", "selfie", "insult", "joke"]


def chatbot(prompt, max_tokens):
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": "Bearer " + os.getenv('HUGGINGFACE_TOKEN')}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_tokens,
            "temperature": 0.8,
            "top_p": 0.9
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]['generated_text']
        else:
            return "Brak odpowiedzi w liście"
    else:
        return f"Błąd: {response.status_code} - {response.text}"
    
    
def get_random_image(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.new(limit=50))

    random.shuffle(posts)
    for post in posts:
        if hasattr(post, "url") and (post.url.endswith(".jpg") or post.url.endswith(".png")):
            return post.url

    return "https://i.redd.it/nq2ztptwnh7e1.jpeg"


@bot.event
async def on_ready():
    for command, response in data.items():
        exec(f"""async def {command}(ctx): await ctx.send("{response}")""")
        bot.command(name=command)(locals()[command])
    print(f'Zalogowano jako {bot.user}')
    
    
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
    await ctx.send('Oto wszystkie komendy funkcjonalne:\n' + ', '.join(allCommands) + "\nA to wszystkie polecenia dodane oddolnie:\n" + ', '.join(data.keys()))
    
@bot.command()
async def story(ctx, *args):
    await ctx.send(chatbot(" ".join(args), 50)[:1500])

@bot.command()
async def insult(ctx, *args):
    await ctx.send(requests.get("https://insult.mattbas.org/api/insult", params={ 'who': " ".join(args) }).text)
    
@bot.command()
async def joke(ctx, *args):
    await ctx.send(requests.get("https://v2.jokeapi.dev/joke/Dark?type=single").json()["joke"])

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

    found = []
    for key, value in data.items():
        if key.lower() in message.content.lower():
            found.append(value)
    if found:
        await message.channel.send(random.choice(found))
    await bot.process_commands(message)
    
@bot.command()
async def selfie(ctx):
    path = get_random_image("femboy");
    await ctx.send(content="Oto jedno z moich zdjęć z kolekcji:", embed=discord.Embed().set_image(url=path))    

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