import json, os, random
from pymongo import MongoClient
from settings import *



def db_connection():
    connect = MongoClient(CONN_STRING)
    collection = connect.discord.wallet
    return collection


def get_cash(member_id):
    collection = db_connection()
    current_cash = collection.find_one({'_id': member_id})['Nanane']
    return current_cash


def lose_money(member_id, current_cash, win):
    collection = db_connection()
    collection.update_one({'_id': member_id},{'$set': {'Nanane': current_cash - win}}, upsert=False)


def win_money(member_id, current_cash, loss):
    collection = db_connection()
    collection.update_one({'_id': member_id},{'$set': {'Nanane': current_cash + loss}}, upsert=False)


async def create_text_channel(guild, channel_name):
    await guild.create_text_channel(channel_name)
    channel = get_channel_by_name(guild, channel_name)
    return channel


async def create_voice_channel(guild, channel_name, user_limit=1):
    await guild.create_voice_channel(channel_name, user_limit=user_limit)
    channel = get_channel_by_name(guild, channel_name)
    return channel

def get_card_dealer(cards, dealer_hand):
    dealer_hand = pop_card(cards, dealer_hand)

    if len(dealer_hand) < 2:
        for c in range(len(dealer_hand)):
            tprint(dealer_hand[c],font="block",chr_ignore=True)
            tprint(".",font="block",chr_ignore=True)
    else:
        for c in range(len(dealer_hand)):
            tprint(dealer_hand[c],font="block",chr_ignore=True)
    return dealer_hand


def get_card(cards, hand):
    if len(hand) < 2:
        for i in range(2):
            hand = pop_card(cards, hand)
    else:
        hand = pop_card(cards, hand)

    for c in range(len(hand)):
        tprint(hand[c],font="block",chr_ignore=True)
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

async def get_channel_by_name(guild, channel_name):
    channel = None
    for c in guild.channels:
        if c.name == channel_name.lower():
            channel = c
            break
        return channel


async def open_file(file, category):
    with open(os.path.join(WORDBANK_DIR, file)) as f:
        jokes = json.load(f)
    opening = random.choice(list(jokes[category]))
    return opening


async def get_mom_joke():
    with open(os.path.join(WORDBANK_DIR, "mama.json")) as f:
        jokes = json.load(f)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult
