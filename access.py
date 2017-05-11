#
# access.py
#
# functions for dealing with access to Discord bot commands
#

from database import CommandClassAccess, User, Role

def grant_user_access(session, user, commandclass):
	new_grant = CommandClassAccess(user_id = user.id, command_class_id = commandclass.id)
	session.add(new_grant)

	session.commit()

def grant_role_access(session, role, commandclass):
	new_grant = CommandClassAccess(role_id = role.id, command_class_id = commandclass.id)
	session.add(new_grant)

	session.commit()
