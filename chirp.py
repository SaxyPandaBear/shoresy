import discord
import asyncio
from auths import discord_token
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout = logging.StreamHandler()
fileHandler = logging.FileHandler('chirp-log.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stdout.setFormatter(formatter)
fileHandler.setFormatter(formatter)
logger.addHandler(stdout)
logger.addHandler(fileHandler)

client = discord.Client()

CHIRPS_FILE = 'chirps.txt'

try:
    f = open(CHIRPS_FILE)
    f.close()
except:
    raise FileNotFoundError('Need {} file to operate'.format(CHIRPS_FILE))


@client.event
async def on_ready():
    logger.info('Username: {0}\nID: {1}'.format(client.user.name, client.user.id))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content is None or not message.content.startswith('!shoresy'):
        return
    
    # don't need to parse message. just send a chirp back to message sender
    await client.send_message(message.channel, __format_chirp__(message.author, __get_random_chirp__(CHIRPS_FILE)))

# format is "@user, 'chirp'"
def __format_chirp__(user, chirp):
    return "{} : {}".format(user.mention, chirp)

# reads from chirps.txt and picks a random chirp from the file
def __get_random_chirp__(filename):
    chirps = __get_all_chirps__(filename)
    if chirps is None:
        logger.error("something went wrong reading file")
        return "oopsie woopsie, contact saxy waxy OwO"
    index = random.randint(0, len(chirps) - 1)
    result = chirps[index].strip()
    logger.info("Chirp: {}".format(result))
    return result


# read chirp file and return the list of chirps from it
def __get_all_chirps__(filename):
    with open(filename) as chirps:
        return chirps.readlines()
    return None

client.run(discord_token)
