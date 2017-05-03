#
# server.py
#
# functions for obtaining data about discord servers
#

import discord

from database import Server, Channel, User

def register_server_and_channels(session, server):

	owner_id = session.query(User).filter(User.id == server.owner.id).first()
	if ( owner_id == None ):
		the_owner = User(id=server.owner.id, name=server.owner.name)
		session.add(the_owner)
	else:
		the_owner = owner_id

	server_id = session.query(Server).filter(Server.name == server.name).first()
	if ( server_id == None ):
		the_server = Server(name=server.name)
		the_server.owner = the_owner
		session.add(the_server)
	else:
		the_server = server_id

	for channel in server.channels:
		channel_id = session.query(Channel).filter(Channel.name == channel.name).first()
		if ( channel_id == None ):
			new_channel = Channel(name=channel.name, squelch=False)
			new_channel.server = the_server
			session.add(the_server)

	session.commit()