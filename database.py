import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from the .env file
loaded = load_dotenv()
print("Environment file loaded:", loaded)

# Fetch database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", 3306)  # Default MySQL port is 3306

# Debugging output
print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB_HOST: {DB_HOST}, DB_NAME: {DB_NAME}, DB_PORT: {DB_PORT}")

# Construct the DATABASE_URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define the sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for declarative models
Base = declarative_base()

def init_db():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

def test_connection():
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            print("Database connection successful!")
    except OperationalError as e:
        print(f"Database connection failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
    init_db()