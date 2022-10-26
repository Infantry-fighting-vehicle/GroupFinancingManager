# Change `sqlalchemy.url` manually in alembic.ini
dbuser = 'root'
dbpass = '852319'
dbhost = '127.0.0.1'
dbport = '3306'
dbname = 'groupfinancingmanager'
DB_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(dbuser, dbpass, dbhost, dbport, dbname)