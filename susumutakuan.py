import discord
import asyncio
import os
import signal
import sys
import subprocess
import imp

#Set up Client State
CLIENT_TOKEN=os.environ['TOKEN']

#Import config
f = open('takuan.config')
global config
config = imp.load_source('config', '', f)
f.close()

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

@client.event
async def on_message(message):
    #Look at DMs for special commands
    if message.channel.type == discord.ChannelType.private:
        if message.content.startswith('!update'):
            tmp = await client.send_message(message.channel, 'Updating my code via git...')
            users = message.channel.recipients
            for user in users:
                if user.id != client.user.id:
                    print('%s/%s requested to update my code.' % (user.name, user.id))

                if user.id in config.developers:
                    process = subprocess.run(["sh", "control.sh", "refresh"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    tmp = await client.send_message(message.channel, process.stdout)
                else:
                    print('%s/%s not allowed to run update command.' % (user.name, user.id))
                    tmp = await client.send_message(message.channel, 'Unauthorized')
        elif message.content.startswith('!restart'):
            tmp = await client.send_message(message.channel, 'Restarting myself...')
            users = message.channel.recipients
            for user in users:
                if user.id != client.user.id:
                    print('%s/%s requested to restart me.' % (user.name, user.id))

                if user.id in config.developers:
                    process = subprocess.run(["sh", "control.sh", "restart"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    tmp = await client.send_message(message.channel, process.stdout)
                else:
                    print('%s/%s not allowed to run restart command.' % (user.name, user.id))
                    tmp = await client.send_message(message.channel, 'Unauthorized')
        elif message.content.startswith('!debug_output'):
            tmp = await client.send_message(message.channel, 'Providing debug log of stdout...')
            message_array=message.content.split(" ")
            try:
                 num_lines=int(message_array[1])
            except ValueError:
                print("debug_error: User gave invalid value for number of lines")
                tmp = await client.send_message(message.channel, '%s is not a valid number of lines' % (message_array[1]))
            log_lines='-%d' % (num_lines)
            users = message.channel.recipients
            for user in users:
                if user.id != client.user.id:
                    print('%s/%s requested output log.' % (user.name, user.id))

                if user.id in config.developers:
                    process = subprocess.run(["tail", log_lines, "logs/output.log"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    tmp = await client.send_message(message.channel, process.stdout)
                else:
                    print('%s/%s not allowed to run debug command.' % (user.name, user.id))
                    tmp = await client.send_message(message.channel, 'Unauthorized')
        elif message.content.startswith('!debug_error'):
            tmp = await client.send_message(message.channel, 'Providing debug log of stderr...')
            message_array=message.content.split(" ")
            try:
                num_lines=int(message_array[1])
            except ValueError:
                print("debug_error: User gave invalid value for number of lines")
                tmp = await client.send_message(message.channel, '%s is not a valid number of lines' % (message_array[1]))
            log_lines='-%d' % (num_lines)
            users = message.channel.recipients
            for user in users:
                if user.id != client.user.id:
                    print('%s/%s requested error log.' % (user.name, user.id))

                if user.id in config.developers:
                    process = subprocess.run(["tail", log_lines, "logs/error.log"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    tmp = await client.send_message(message.channel, process.stdout)
                else:
                    print('%s/%s not allowed to run debug command.' % (user.name, user.id))
                    tmp = await client.send_message(message.channel, 'Unauthorized')



    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))




#Start event loop
client.run(CLIENT_TOKEN)