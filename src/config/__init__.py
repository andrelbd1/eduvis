import os
from dotenv import load_dotenv

class Settings:
    
    load_dotenv(override=True)
    
    # Setting Environment
    ENV = os.environ["ENV"]
    
settings = Settings()