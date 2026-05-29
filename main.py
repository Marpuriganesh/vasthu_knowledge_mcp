import argparse
from src.vasthu_knowledge_mcp.db import engine
from src.vasthu_knowledge_mcp.models import Base
from src.vasthu_knowledge_mcp import mcp_run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--command", choices=["migrate", "serve"])
    args = parser.parse_args()
    
    if args.command == "migrate":
        Base.metadata.create_all(engine)
    elif args.command == "serve":
        print("Starting the server...")
        mcp_run()

if __name__ == "__main__":
    main()