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

def has_user_access(session, user, commandclass):
	has_access = session.query(CommandClassAccess).filter(CommandClassAccess.user_id == user.id, CommandClassAccess.command_class_id == commandclass.id).first()
	if (has_access == None):
		return False
	else:
		return True

def has_role_access(session, role, commandclass):
	has_access = session.query(CommandClassAccess).filter(CommandClassAccess.role_id == role.id, CommandClassAccess.command_class_id == commandclass.id).first()
	if (has_access == None):
		return False
	else:
		return True

def has_access(session, user, commandclass):
	user_access = has_user_access(session, user, commandclass)
	for role in user.roles:
		role_access = has_role_access(session, role, commandclass)
		if ( role_access ):
			break

	if ( user_access or role_access ):
		return True
	else:
		return False
