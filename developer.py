#
# developer.py
#
# developer functions for managing SusumuTakuan remotely
#

import discord
import asyncio
import subprocesss

async def update_git(client, message):
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


async def restart_bot(client, message):
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

async def debug_output(client, message):
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

async def debug_error(client, message):
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