#
# server.py
#
# functions for obtaining data about discord servers
#

import discord

from database import Server, Channel, User, Role

def create_internal_server(session):

	owner_id = session.query(User).filter(User.id == 1).first()
	if ( owner_id == None ):
		the_owner = User(id=1, name='SusumuTakuan')
		session.add(the_owner)

	server_id = session.query(Server).filter(Server.name == 'internal').first()
	if ( server_id == None ):
		the_server = Server(id=1, name='internal')
		the_server.owner = the_owner
		session.add(the_server)

	role_id = session.query(Role).filter(Role.name == 'developer', Role.server_id == 1).first()
	if ( role_id == None ):
		new_role = Role(name='developer')
		new_role.server = the_server
		session.add(new_role)

	session.commit()


#Registers all of the data about a Discord server into the database
def register_server(session, server):

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
		channel_id = session.query(Channel).filter(Channel.name == channel.name, Channel.server_id == server.id).first()
		if ( channel_id == None ):
			new_channel = Channel(name=channel.name, squelch=False)
			new_channel.server = the_server
			session.add(new_channel)

	for role in server.roles:
		role_id = session.query(Role).filter(Role.name == role.name, Role.server_id == server.id).first()
		if ( role_id == None ):
			new_role = Role(name=role.name)
			new_role.server = the_server
			session.add(new_role)

	session.commit()