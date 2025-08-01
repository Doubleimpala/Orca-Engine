import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def decompile_binary(message, attachment):
    name = attachment.filename
    root, extension = os.path.splitext(name)
    if extension != ".dll"  and extension != ".exe" and extension != ".so" and extension != ".bin":
        print("invalid")
        return ""
    return discord.File()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$decompile'):
        if not message.attachments:
            embed_var = discord.Embed(
                title="Please attach a file.",
                description="`.exe`, `.bin`, `.dll`, and `.so` files are supported.",
                color=discord.Color.purple()
            )
            await message.channel.send(embed=embed_var)
        else:
            attachment = message.attachments[0]
            embed_var = discord.Embed(
                title="Analyzing...",
                color=discord.Color.purple()
            )
            await message.channel.send(embed=embed_var)
            file = decompile_binary(message=message,attachment=attachment)
            if file != "":
                await message.channel.send(content="Here is the deassembled code in `.asm` format.",file=file)
            else:
                embed_var = discord.Embed(
                    title="Invalid Input.",
                    description="`.exe`, `.bin`, `.dll`, and `.so` files are supported.",
                    color=discord.Color.purple()
                )
                await message.channel.send(embed=embed_var)

@tree.command(
    name="decompile",
    description="Decompiles a binary file into C code."
)
async def command(interaction):
    await interaction.response.send_message("Please run $decompile. Slash commands do not support file attachments.")

# @tree.command(
#     name="pentest"
# )


load_dotenv()
client.run(os.getenv("SECRET"))


#@discord.Client.tree.command()
