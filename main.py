import sys

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship

# Create Database
con = psycopg2.connect(
    database='postgres',
    user='admin',
    password='admin',
    host='localhost',
    port='5432')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
try:
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('mydb'))
        )
    print("Database created.")
except psycopg2.DatabaseError:
    print("Database already exists.")
except Exception as ex:
    print("Unexpected Error.")
    print(ex)
    sys.exit(1)

# Create Tables
engine = create_engine('postgresql://admin:admin@localhost/mydb', echo=True)
Base = declarative_base()

''' Many to Many Association Table '''
association_table = Table(
    'association',
    Base.metadata,
    Column('parent_id', ForeignKey('parent.id'), primary_key=True),
    Column('child_id', ForeignKey('child.id'), primary_key=True)
)


class Parent(Base):
    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)
    job = Column(String)

    # M:M Relationship with Child
    children = relationship(
        "Child",
        secondary=association_table,
        backref="parents")


class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)
    school = Column(String)

    # 1:M Relationship with Toy
    toys = relationship("Toy")


class Toy(Base):
    __tablename__ = 'toy'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    # M:1 Relationship with Child
    child_id = Column(Integer, ForeignKey('child.id'))


Base.metadata.bind = engine
Base.metadata.create_all()
