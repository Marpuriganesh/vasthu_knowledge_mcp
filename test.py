from src.vasthu_knowledge_mcp.db import get_index

# Check index
entries = get_index()
for e in entries:
    print(e.topic, e.page_refs)
