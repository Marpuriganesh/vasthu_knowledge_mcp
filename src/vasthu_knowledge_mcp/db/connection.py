from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent.parent
data_dir = os.path.join(BASE_DIR,"data")
# Safely creates the folder
os.makedirs(data_dir,exist_ok=True)
engine = create_engine(f"sqlite:///{BASE_DIR}/data/vastu.db")

SessionLocal = sessionmaker(bind=engine)

