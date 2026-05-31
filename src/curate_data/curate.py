import os
from src.curate_data.pdf_utills import PDFManager, get_batch_data, get_pdf_info
from .read_config import config
from src.curate_data.agent import local_create_agent
from langchain_core.prompts import PromptTemplate
from langchain.messages import SystemMessage


def get_pdfs(pdf_dir: str) -> list[str]:
    pdfs = []
    for files in os.listdir(pdf_dir):
        full_path = os.path.join(pdf_dir, files)
        if not os.path.isdir(full_path):
            basename = os.path.basename(files)
            if basename.endswith(".pdf"):
                pdfs.append(basename)
    return pdfs


def get_pages_list(page_count: int, step: int) -> list[tuple[int, int]]:
    if step > page_count:
        raise ValueError("Step can't be greater than page_count")

    pages_list = []

    # Loop from 0 up to page_count, leaping by the step size
    for start in range(0, page_count, step):
        # Calculate the end index, making sure we don't overshoot page_count - 1
        end = min(start + step - 1, page_count - 1)
        pages_list.append((start, end))

    return pages_list


async def curate_main():
    agent = await local_create_agent()
    prompt = PromptTemplate.from_template("""
You are the Vastu Database Builder. Your goal is to extract rules from the text and add them to the database without creating duplicate entities.
                            
Data to process:
[{pages_data}]

STRICT WORKFLOW:
Step 1: READ EXISTING DATA. 
You must immediately call `get_index_tool`, `get_rooms_tool`, and `get_directions_tool`. Do not proceed until you see the results.

Step 2: ANALYZE.
Look at the results from Step 1. Are the topics, rooms, and directions mentioned in the INPUT TEXT already in the database? 

Step 3: CREATE MISSING ENTITIES.
If a room, direction, or index topic is missing, call `insert_room_tool`, `insert_direction_tool`, or `insert_index_entry_tool` to create them.

Step 4: INGEST RULES.
- Call `insert_page_tool` to save the text.
- Call `insert_rule_tool` to save the rule (-2 to 2 compatibility).
- Call `insert_rule_mapping_tool` to link the rule to the room and direction.
- Call `insert_consequence_tool` if effects are mentioned.
                            """)
    BOOKS_DIR = config["books_path"]
    pdf_manager = PDFManager(BOOKS_DIR)
    pdfs = get_pdfs(BOOKS_DIR)
    llm_stream_config = {"configurable": {"user_id": "local-user-123"}}

    for pdf in pdfs:
        r_pdf = pdf_manager.open_document(pdf)
        pdf_info = get_pdf_info(r_pdf)
        pages_list = get_pages_list(pdf_info.get("page_count", 0), 5)
        for i, (start_page, end_page) in enumerate(pages_list):
            pages_blocks = get_batch_data(r_pdf, start_page, end_page)
            input_prompt = {
                "messages":[
                    SystemMessage(
                        content=prompt.format( pages_data=pages_blocks)
                    )
                ]
            }
            print("+"*50)
            print(f"\npages [{start_page}-{end_page}] : \n ")
            async for chunk in agent.astream(
                input_prompt, config=llm_stream_config, stream_mode="updates"
            ):
                for node_name, node_output in chunk.items():
                    print(f"📦 Node Executed: [{node_name}]")
                print("-" * 40)

                # Format and display messages inside the node output nicely
                if "messages" in node_output:
                    for msg in node_output["messages"]:
                        # Check for tool execution calls made by the model
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            print("🛠️ Model requested Tool Call:")
                            for call in msg.tool_calls:
                                print(f"   -> Tool Name: {call['name']}")
                                print(f"   -> Arguments: {call['args']}")

                        # Check for tool results being sent back to the graph
                        elif msg.type == "tool":
                            print("📥 Tool Returned Data:")
                            print(f"   {msg.content}")

                        # Check for standard model output text
                        elif msg.content:
                            print("🤖 Model Response Content:")
                            print(f"   {msg.content}")

                print("-" * 40 + "\n")

            print("--- GRAPH EXECUTION FINISHED ---")
            print("+" * 50)
