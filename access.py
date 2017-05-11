#
# access.py
#
# functions for dealing with access to Discord bot commands
#

from database import CommandClassAccess

def grant_user_access(user, commandclass):
	new_grant = CommandClassAccess(user_id = user.id, command_class_id = commandclass.id)
	session.add(new_grant)

	session.commit()

def grant_role_access(role, commandclass):
	new_grant = CommandClassAccess(role_id = role.id, command_class_id = commandclass.id)
	session.add(new_grant)

	session.commit()
