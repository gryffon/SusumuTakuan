#
# server.py
#
# functions for obtaining data about discord servers
#

import discord

from database import Server, Channel

async def on_server_join(server):

	server_id = session.query(Server).filter(Server.name == server.name).first()
	if ( server_id == None ):
		the_server = Server(name=server.name)
		session.add(the_server)
	else:
		the_server = server_id

	for channel in server.channels:
		channel_id = session.query(Channel).filter(Channel.name == channel.name).first()
		if ( channel_id == None ):
			new_channel = Channel(name=channel.name, squelch=False)
			new_channel.server = the_server
			session.add(new_server)

	session.commit()