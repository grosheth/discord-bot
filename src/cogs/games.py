import asyncio
from discord.ext import commands
from random import randint
from utils import *

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="!coinflip <pile> <face>")
    async def coinflip(self, ctx, arg):
        arg = arg.lower()
        if arg != "pile" and arg != "face":
            await ctx.send(f"{arg} n'est pas un choix à Pile ou face. Monsieur soleil")
            return
        
        guesses = {
            1:"pile",
            2:"face"
        }
        guess = randint(1,2)
        await asyncio.sleep(1)
        await ctx.send("...La tension monte...")
        await asyncio.sleep(2)
        
        if ctx.author.id == int(FILOU):
            await ctx.send("...pas comme la molle a Filou...")
        await ctx.send(guesses[guess])

        if guesses[guess] == arg:
            await asyncio.sleep(1)
            await ctx.send("Bravo, Pussi Conqueror")
        else:
            await asyncio.sleep(1)
            await ctx.send("CACHING MUFAKA")


    @commands.command(brief="!rr Russian roulette")
    async def rr(self, ctx):
        await ctx.send("Tu gagne 1000 Nanane si tu meur pas. Tu perd 5000 Nanane si tu tfa shot.")
        
        if ctx.author.voice is None:
            await ctx.send("T po dans l'channel, Tu decide po.")
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        await ctx.send("Roulette Russe")
        await asyncio.sleep(1)
        for member in voice_channel.members:

            current_cash = get_cash(member.id)
            shot = randint(1,6)

            await ctx.send(f'{member.name} {await open_file("russianroulette.json","opening")}')
            await asyncio.sleep(1)
            if shot == 1:
                lose_money(member.id, current_cash, 5000)
                await ctx.send(f'{member.name} {await open_file("russianroulette.json","dead")}')
                await ctx.send(f'{member.name} Ta pardu tes Nanane sti de laid')
                await asyncio.sleep(1)
                await member.move_to(None)
                return
            else:
                if member.id == int(FILOU):
                    lose_money(member.id, current_cash, 500)            
                else:
                    win_money(member.id, current_cash, 1000)
                await ctx.send(f"click...")
                await asyncio.sleep(1)
                await ctx.send(f'{await open_file("russianroulette.json","alive")}')

        await asyncio.sleep(1)
        await ctx.send(f"Parsonne est mort")
        return


    @commands.command(brief="!blackjack")
    async def blackjack(self, ctx):

        points = 0
        dealer_points = 0
        hand = []
        dealer_hand = []
        cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        x = 0
        for value in cards:
            if x < 39:
                cards.append(value)
            else:
                break
            x += 1

        await create_text_channel(ctx.author.guild, f"{ctx.author.name}-blackjack")
        
        await ctx.send("Here is the dealer's first card:")
        get_card_dealer(cards, dealer_hand)
        await ctx.send("-------------------------------------")
        await ctx.send("Here is your hand:")
        get_card(cards, hand)
        points = convert(hand, points)
        dealer_points = convert(dealer_hand, dealer_points)
        while True:
            await ctx.send(f"you currently have {points}")
            await ctx.send(f"The dealer has {dealer_points}")
            await ctx.send("1. Call.")
            await ctx.send("2. Stay.")
            answer = input()

            if answer == "1":
                await ctx.send("Here is your hand:")
                get_card(cards, hand)
                points = convert(hand, points)
                if points > 21:
                    await ctx.send("you have more than 21!")
                    await ctx.send("YOU LOST")
                    # delete channel await create_text_channel(ctx.author.guild, f"{ctx.author.name}-blackjack")
                    await asyncio.sleep(1)
                    
            elif answer == "2":
                    await ctx.send("Here is the dealer's hand")
                    get_card_dealer(cards, dealer_hand)
                    await ctx.send("-------------------------------------")
                    dealer_points = convert(dealer_hand, dealer_points)
                    await asyncio.sleep(1)

                    while True:
                        
                        if dealer_points > 21:
                            await ctx.send("You Won the dealer has more than 21")
                            await ctx.send("YOU WON")
                            # delete channel await create_text_channel(ctx.author.guild, f"{ctx.author.name}-blackjack")

                        if dealer_points <= 16:
                            get_card_dealer(cards, dealer_hand)
                            dealer_points = convert(dealer_hand, dealer_points)
                            await asyncio.sleep(1)
                        else:
                            win = decision(points, dealer_points)

                            if win:
                                await ctx.send(f"You won with {points} against the dealer's {dealer_points}")
                                await ctx.send("YOU WON")
                                # delete channel await create_text_channel(ctx.author.guild, f"{ctx.author.name}-blackjack")
                            else:
                                await ctx.send(f"You lost with {points} against the dealer's {dealer_points}")
                                await ctx.send("YOU LOST")
                                # delete channel await create_text_channel(ctx.author.guild, f"{ctx.author.name}-blackjack")
            else:
                await ctx.send("invalid answer")
        
        
        def get_card_dealer(cards, dealer_hand):
            dealer_hand = pop_card(cards, dealer_hand)

            if len(dealer_hand) < 2:
                for c in range(len(dealer_hand)):
                    await ctx.send(dealer_hand[c])
            else:
                for c in range(len(dealer_hand)):
                    await ctx.send(dealer_hand[c])
            return dealer_hand


        def get_card(cards, hand):
            if len(hand) < 2:
                for i in range(2):
                    hand = pop_card(cards, hand)
            else:
                hand = pop_card(cards, hand)

            for c in range(len(hand)):
                await ctx.send(hand[c],font="block",chr_ignore=True)
            return hand


        def pop_card(cards, hand):
            position = randint(0,len(cards))
            card = cards[position]
            cards.pop(position)
            hand.append(card)
            return hand


        def convert(hand, points):
            if points > 0:
                if hand[-1].isdigit():
                    c = int(hand[-1])
                else:
                    if hand[-1] != "A":
                        c = 10
                    elif points < 21:
                        c = 11
                    else:
                        c = 1
                points += c
            else:
                for c in hand:
                    if c.isdigit():
                        c = int(c)
                    else:
                        if c != "A":
                            c = 10
                        elif points < 21:
                            c = 11
                        else:
                            c = 1
                    points += c
            return points


        def decision(points, dealer_points):
            if points == 21:
                win = True   
            elif points > dealer_points:
                win = True
                return win
            else:
                win = False
                return win            
                
def setup(bot):
    bot.add_cog(Games(bot))