from typing import Optional

from src.vasthu_knowledge_mcp.db import (
    insert_consequence,
    insert_direction,
    insert_index_entry,
    insert_page,
    insert_room,
    insert_rule,
    insert_rule_mapping,
)

def register_write_tools(mcp):
    @mcp.tool(
        description="""Insert a consequence for a rule violation. severity is -2 (catastrophic) to 2 (minor)."""
    )
    def insert_consequence_tool(rule_id: int, description: str, severity: int):
        insert_consequence(rule_id=rule_id,description=description,severity=severity)
    
    @mcp.tool(
        description="""Insert a new Vastu direction with its associated deity and element into the knowledge base."""
    )
    def insert_direction_tool(name: str, deity: str, element: str):
        insert_direction(name=name,deity=deity,element=element)
    
    @mcp.tool(
        description="""Add a new topic to the knowledge index. Keywords should be comma separated. Page refs should be comma separated page numbers."""
    )
    def insert_index_entry_tool(
        topic: str, category: str, keywords: str, page_refs: str, rule_count: int
    ):
        insert_index_entry(topic=topic,category=category,keywords=keywords,page_refs=page_refs,rule_count=rule_count)
    
    @mcp.tool(
        description="""Store extracted knowledge from a PDF page. Summary should be dense and keyword-rich, max 600 chars."""

    )
    def insert_page_tool(page_num: int, summary: str, full_text: str):
        insert_page(page_num=page_num,summary=summary,full_text=full_text)
    
    @mcp.tool(
        description="""Insert a new room type. Include all common aliases as comma separated string e.g. 'bathroom, washroom, toilet'."""
    )
    def insert_room_tool(name: str, aliases: str):
        insert_room(name=name,aliases=aliases)
    
    @mcp.tool(
        description="""Insert a Vastu rule. compatibility is -2 (strictly avoid) to 2 (highly auspicious). short_desc max 600 chars."""
    )
    def insert_rule_tool(
        index_id: int,
        page_id: int,
        short_desc: str,
        full_detail: str,
        compatibility: int,
    ):
        insert_rule(index_id=index_id,page_id=page_id,short_desc=short_desc,full_detail=full_detail,compatibility=compatibility)
    
    @mcp.tool(
        description="""Map a rule to a room and/or direction. Leave room_id or direction_id as None for general rules."""
    )
    def insert_rule_mapping_tool(
        rule_id: int, room_id: Optional[int] = None, direction_id: Optional[int] = None
    ):
        insert_rule_mapping(rule_id=rule_id,room_id=room_id,direction_id=direction_id)