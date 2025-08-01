import discord

class Client(discord.Client()):
    async def on_ready(self):
        print(f"Logged in as {self.user}.")
    
    @discord.Client.tree.command()
    async def on_message(self,message):
        pass