from sqlalchemy import text
from src.database.create_tables import engine

def migrate_enum():
    with engine.connect() as connection:
        # Check if 'admin' already exists in the enum to avoid errors on re-run
        result = connection.execute(text("SELECT enum_range(NULL::userrole)"))
        existing_values = result.scalar()
        
        if 'admin' not in existing_values:
            print("Adding 'admin' to userrole enum...")
            # PostgreSQL doesn't allow ALTER TYPE ... ADD VALUE inside a transaction block
            # depends on the version/environment, but usually it needs to be committed immediately
            connection.execute(text("COMMIT")) 
            connection.execute(text("ALTER TYPE userrole ADD VALUE 'admin'"))
            print("Successfully added 'admin' to userrole enum.")
        else:
            print("'admin' already exists in userrole enum.")

if __name__ == "__main__":
    migrate_enum()
