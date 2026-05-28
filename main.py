import argparse
from src.vasthu_knowledge_mcp.db import engine
from src.vasthu_knowledge_mcp.models import Base

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--command", choices=["migrate", "serve"])
    args = parser.parse_args()
    
    if args.command == "migrate":
        Base.metadata.create_all(engine)
    elif args.command == "serve":
        print("server in progress...")

if __name__ == "__main__":
    main()