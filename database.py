#
# database.py
#
# set up and manage a database for storing data between sessions
#
import logging

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
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<User:{}'.format(self.name)


class Server(Base):
	__tablename__ = 'servers'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship('User', backref=backref('servers', uselist=True))

	def __repr__(self):
		return '<Server:{}'.format(self.name)

class Role(Base):
	__tablename__ = 'roles'
	id = Column(Integer, primary_key=True)
	server_id = Column(Integer, ForeignKey('servers.id'), primary_key=True)
	name = Column(String(250), nullable=False)
	squelch = Column(Boolean, nullable=False, default=False)
	server = relationship('Server', backref=backref('roles', uselist=True))

	def __repr__(self):
		return '<Role:{}'.format(self.name)

class Channel(Base):
	__tablename__ = 'channels'
	id = Column(Integer, primary_key=True)
	server_id = Column(Integer, ForeignKey('servers.id'), primary_key=True)
	name = Column(String(250), nullable=False)
	squelch = Column(Boolean, nullable=False, default=False)
	server = relationship('Server', backref=backref('channels', uselist=True))

	def __repr__(self):
		return '<Channel:{}'.format(self.name)

class CommandClass(Base):
	__tablename__ = 'command_classes'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	def __repr__(self):
		return '<CommandClass:{}'.format(self.name)

class Command(Base):
	__tablename__ = 'commands'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	command_class_id = Column(Integer, ForeignKey('command_classes.id'))
	command_class = relationship('CommandClass', backref=backref('commands', uselist=True))
	squelch = Column(Boolean, nullable=False, default=False)

	def __repr__(self):
		return '<Command:{}'.format(self.name)

class CommandClassAccess(Base):
	__tablename__ = 'command_classes_access'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False, default=0)
	role_id = Column(Integer, nullable=False, default=0)
	command_class_id = Column(Integer, nullable=False, default=0)
	
class CommandChannelMute(Base):
	__tablename__ = 'command_channel_mute'
	id = Column(Integer, primary_key=True)
	command_id = Column(Integer, nullable=False, default=0)
	command_class_id = Column(Integer, nullable=False, default=0)
	channel_id = Column(Integer, nullable=False, default=0)


logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///susumu_takuan.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)