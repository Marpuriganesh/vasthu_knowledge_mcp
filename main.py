import argparse
import asyncio
from src.vasthu_knowledge_mcp.db import engine
from src.vasthu_knowledge_mcp.models import Base
from src.vasthu_knowledge_mcp import mcp_run
from src.curate_data import curate_main
from src.curate_data.agent import test_agent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", choices=["migrate", "serve", "curate","test_agent"])
    args = parser.parse_args()
    
    match args.command:
        case "migrate":
            Base.metadata.create_all(engine)
        case "serve":
            print("Starting the server...")
            mcp_run()
        case "curate":
            curate_main()
        case "test_agent":
            asyncio.run(test_agent())
        case _:
            print("Unknown command please check help for usage!")

if __name__ == "__main__":
    main()