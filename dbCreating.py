from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///instance/Database.db', echo = True)
meta = MetaData()

students = Table(
   'users', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String, primary_key = True), 
   Column('username', String, primary_key = True),
   Column('email', String, primary_key = True),
   Column('phone', String, primary_key = True),
   Column('password', String, primary_key = True),
)
meta.create_all(engine)