# Change `sqlalchemy.url` manually in alembic.ini

dbuser = 'startup'
dbpass = 'hû$§Ó]Çýf¬Y3~XÓ¡:/["pÖ9Ý<'
dbhost = '127.0.0.1'
dbport = '3307'
dbname = 'groupfinancingmanager'
DB_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(dbuser, dbpass, dbhost, dbport, dbname)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_session():
    engine = create_engine(DB_URL)
    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory()
