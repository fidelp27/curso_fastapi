import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre de la BBDD
sqlite_file_name = "../database.sqlite"
# Directorio actual
base_dir = os.path.dirname(os.path.realpath(__file__))

# La URL para conectarse a la BBDD
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Motor de la BBDD
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
