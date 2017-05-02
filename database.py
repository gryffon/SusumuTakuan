#
# database.py
#
# set up and manage a database for storing data between sessions
#

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    owner = Column(Integer, ForeignKey('users.id'))

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    server = Column(Integer, ForeignKey('servers.id'))

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    server = Column(Integer, ForeignKey('servers.id'))
    squelch = Column(Boolean, nullable=False)

class CommandClass(Base):
    __tablename__ = 'commandclasses'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    squelch = Column(Boolean, nullable=False)
    command_class = Column(Integer, ForeignKey('commandclasses.id'))

class RoleCommandAccess(Base):
	__tablename__ = 'rolecommands'
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('roles.id'))
	command = Column(Integer, ForeignKey('commands.id'))
	squelch = Column(Boolean, nullable=False)

class RoleCommandClassAccess(Base):
	__tablename__ = 'rolecommandclasses'
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('roles.id'))
	command_class = Column(Integer, ForeignKey('commandclasses.id'))
	squelch = Column(Boolean, nullable=False)

class UserCommandAccess(Base):
	__tablename__ = 'usercommands'
	id = Column(Integer, primary_key=True)
	user = Column(Integer, ForeignKey('users.id'))
	command = Column(Integer, ForeignKey('commands.id'))
	squelch = Column(Boolean, nullable=False)

class UserCommandClassAccess(Base):
	__tablename__ = 'usercommandclasses'
	id = Column(Integer, primary_key=True)
	user = Column(Integer, ForeignKey('users.id'))
	command_class = Column(Integer, ForeignKey('commandclasses.id'))
	squelch = Column(Boolean, nullable=False)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///susumu_takuan.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)