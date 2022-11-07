from discord.ext import commands
import discord, aiohttp
from utils import *

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="!insult @<user>")
    async def insult(self, ctx, member: discord.Member = None):
        add_to_db(member.id, current_count, 1, "Memes")
        insult = await get_mom_joke()
        await ctx.send(f"{member.display_name} {insult}")


    @commands.command(brief="!quote sends a beer quote with image")
    async def quote(self, ctx):
        add_to_db(member.id, current_count, 1, "Memes")
        quote = await open_file("beer.json", "beer")
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://picsum.photos/1000/1000") as r:
                    embed = discord.Embed(title=quote)
                    embed.set_image(url=r._real_url)
                    await ctx.send(embed=embed)

                    
    @commands.command(brief="!whoyou Stepbot se présente")
    async def whoyou(self, ctx):
        await ctx.send(embed=discord.Embed(title="What are you doing stepbot?? UwU",
                                                    description=
                                                    "Feet adorer, womanizer, Short longsword, can do the drapeau, gets stuck in washing machine and windows(I use Arch btw). Nemesis: Nick Gingras.",
                                                    color=0xeeafe6))

def setup(bot):
    bot.add_cog(Memes(bot))