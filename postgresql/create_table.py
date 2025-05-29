from postgresql.database import engine
import postgresql.models

def create_table():
    postgresql.models.Base.metadata.create_all(bind=engine)