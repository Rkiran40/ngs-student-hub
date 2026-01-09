from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, inspect

load_dotenv('backend/.env')
uri = os.getenv('DATABASE_URL')
print('Using DATABASE_URL:', uri)
engine = create_engine(uri)
inspector = inspect(engine)
print('Tables:', inspector.get_table_names())
