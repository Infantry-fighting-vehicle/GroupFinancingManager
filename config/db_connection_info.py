# Change `sqlalchemy.url` manually in alembic.ini
dbuser = 'director'
dbpass = 'NEW_USER_PASSWORD'
dbhost = '127.0.0.1'
dbport = '3307'
dbname = 'groupfinancingmanager'
DB_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(dbuser, dbpass, dbhost, dbport, dbname)