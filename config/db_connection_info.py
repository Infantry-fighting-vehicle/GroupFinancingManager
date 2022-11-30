# Change `sqlalchemy.url` manually in alembic.ini

dbuser = 'root'
dbpass = '000000'
dbhost = '127.0.0.1'
dbport = '3306'
dbname = 'groupfinancingmanager'
DB_URL = "mysql://{}:{}@{}:{}/{}".format(dbuser, dbpass, dbhost, dbport, dbname)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine(DB_URL, pool_size=30, max_overflow=0)
SessionFactory = sessionmaker(bind=engine)

def get_database_session():
    Session = SessionFactory()
    Session.flush()
    return Session
