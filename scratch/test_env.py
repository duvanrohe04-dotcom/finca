from dotenv import load_dotenv
import os

loaded = load_dotenv()
print(f"File .env exists: {os.path.exists('.env')}")
print(f"dotenv loaded: {loaded}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
