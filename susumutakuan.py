import discord
import asyncio
import os
import signal
import sys
import subprocess

#Set up Client State
CLIENT_TOKEN=os.environ['TOKEN']

#Create Discord client
client = discord.Client()

#Handle shutdown gracefully
def sigterm_handler(signum, frame):
    print('Logging out...', flush=True) 
    raise KeyboardInterrupt
    sys.exit('Shutting down...')

#Register SIGTERM Handler
signal.signal(signal.SIGTERM, sigterm_handler)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    #Look at DMs for special commands
    if message.channel.type == discord.ChannelType.private:
        if message.content.startswith('!update'):
            tmp = await client.send_message(message.channel, 'Updating my code via git...')
            subprocess.call(["ls", "-l"])

    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))




#Start event loop
client.run(CLIENT_TOKEN)