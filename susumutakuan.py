import discord
import asyncio
import os
import signal
import sys
import imp
import logging

logging.basicConfig()

#Local Imports
import developer
import database
import server

#Set up Client State
CLIENT_TOKEN=os.environ['TOKEN']

#Import config
f = open('takuan.config')
global config
config = imp.load_source('config', '', f)
f.close()

#Create database session
session = database.DBSession()

#Register bot class and functions
server.create_internal_server(session)
developer.register_functions(session)
developer.register_developer_access(session, config.developers)


#Create Discord client
client = discord.Client()

#Handle shutdown gracefully
def sigterm_handler(signum, frame):
    print('Logging out...', flush=True) 
    raise KeyboardInterrupt
    print('Shutting down...')
    sys.exit(0)

#Register SIGTERM Handler
signal.signal(signal.SIGTERM, sigterm_handler)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for client_server in client.servers:
        server.register_server(session, client_server)

#Register events
@client.event
async def on_message(message):
    #Look at DMs for special commands
    if message.channel.type == discord.ChannelType.private:
        if message.content.startswith('!update'):
            await developer.update_git(client, message, config.developers)
        elif message.content.startswith('!restart'):
            await developer.restart_bot(client, message, config.developers)
        elif message.content.startswith('!debug_output'):
            await developer.debug_output(client, message, config.developers)
        elif message.content.startswith('!debug_error'):
            await developer.debug_error(client, message, config.developers)

    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))


@client.event
async def on_server_join(client_server):
    server.register_server(session, client_server)



#Start event loop
client.run(CLIENT_TOKEN)