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
		new_role = Role(id=1, name='developer', server_id=the_server.id)
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
		the_server = Server(id=server.id, name=server.name)
		the_server.owner = the_owner
		session.add(the_server)
	else:
		the_server = server_id

	for channel in server.channels:
		channel_id = session.query(Channel).filter(Channel.id == channel.id, Channel.server_id == server.id).first()
		if ( channel_id == None ):
			new_channel = Channel(id=channel.id, name=channel.name, server_id=the_server.id)
			session.add(new_channel)

	for role in server.roles:
		role_id = session.query(Role).filter(Role.id == role.id, Role.server_id == server.id).first()
		if ( role_id == None ):
			new_role = Role(id=role.id, name=role.name, server_id=the_server.id)
			session.add(new_role)

	session.commit()

#Scan server for users and populates user/roles tables
async def scan_server(client, message, session):
	command = session.query(Command).filter(Command.name == 'scan_server').first()

	tmp = await client.send_message(message.channel, 'Scanning server for users...')
	users = message.channel.recipients
	for user in users:
		if user.id != client.user.id:
			print('%s/%s requested to scan server for users.' % (user.name, user.id))

	server = message.server

	if ( user.id == server.owner.id ):

		for member in server.members:
			member_id = session.query(User).filter(User.id == member.id).first()
			if ( owner_id == None ):
				the_member = User(id=member.id, name=member.name)
			else:
				the_member = member_id

			for role in member.roles:
				the_role = session.query(Role).filter(Role.id == role.id, Role.server_id == server.id).first()
				if ( the_role not in the_member.roles ):
					the_member.roles.append(the_role)

			session.add(the_member)

		session.commit()
	else:
		print('%s/%s not allowed to run server scan command.' % (user.name, user.id))
		tmp = await client.send_message(message.channel, 'Unauthorized')

#Add user to database
async def add_user(session, member):
	user_id = session.query(User).filter(User.id == member.id).first()
	if ( user_id == None ):
		the_member = User(id=member.id, name=member.name)
		for role in member.roles:
			the_role = session.query(Role).filter(Role.id == role.id, Role.server_id == role.server_id).first()
			the_member.roles.append(the_role)		

		session.add(the_member)
		session.commit()



#Update user roles
async def update_user_roles(session, before, after):

#Add server role
async def add_server_role(session, role):

#Remove server role
async def del_server_role(session, role):

#Update server role
async def update_server_role(session, before, after):