from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    id_table = Column(Integer, primary_key = True)
    name = Column(String)
    password = Column(String)
    status = Column(String)

    def __repr__(self):
        return ("Username: {},\n"
            "password: {}. \n"
            "status: {}. \n"
        	).format(
        		self.name,
                self.password,
                self.status)


class Post(Base):
    __tablename__ = "Post"
    id_table = Column(Integer, primary_key = True)
    post_string = Column(String)

    def __repr__(self):
        return ("{} \n "
            "\n").format(
                self.post_string)