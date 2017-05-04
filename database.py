#
# database.py
#
# set up and manage a database for storing data between sessions
#

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

user_role_table = Table('user_role', Base.metadata,
	Column('user_id', Integer, ForeignKey('users.id')),
	Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	roles = relationship('Role', secondary='user_role', backref='users')
	command_classes = relationship('UserCommandAccess', back_populates="user")
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<User:{}'.format(self.name)


class Server(Base):
	__tablename__ = 'servers'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship(User, backref=backref('servers', uselist=True))

	def __repr__(self):
		return '<Server:{}'.format(self.name)

class Role(Base):
	__tablename__ = 'roles'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	server_id = Column(Integer, ForeignKey('servers.id'))
	server = relationship('Server', backref=backref('roles', uselist=True))
	command_classes = relationship('UserCommandAccess', back_populates="user")
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<Role:{}'.format(self.name)

class Channel(Base):
	__tablename__ = 'channels'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	server_id = Column(Integer, ForeignKey('servers.id'))
	server = relationship('Server', backref=backref('channels', uselist=True))
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<Channel:{}'.format(self.name)

class CommandClass(Base):
	__tablename__ = 'commandclasses'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	users = relationship('UserCommandAccess', back_populates="command")
	roles = relationship('RoleCommandAccess', back_populates="command")

	def __repr__(self):
		return '<CommandClass:{}'.format(self.name)

class Command(Base):
	__tablename__ = 'commands'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	command_class_id = Column(Integer, ForeignKey('commandclasses.id'))
	command_class = relationship('CommandClass', backref=backref('commands', uselist=True))
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<Command:{}'.format(self.name)

class UserCommandAccess(Base):
	__tablename__ = 'usercommandaccess'
	command_class_id = Column(Integer, ForeignKey('commandclassess.id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
	squelch = Column(Boolean, nullable=False, default=False)

	command_classes = relationship('CommandClass', back_populates="users")
	user = relationship(User, back_populates="command_classes")

class RoleCommandAccess(Base):
	__tablename__ = 'rolecommandaccess'
	command_class_id = Column(Integer, ForeignKey('commandclassess.id'), primary_key=True)
	role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
	squelch = Column(Boolean, nullable=False, default=False)

	command_classes = relationship('CommandClass', back_populates="roles")
	role = relationship('User', back_populates="command_classes")


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///susumu_takuan.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)