from src.vasthu_knowledge_mcp.db import (
    get_index,
    get_directions,
    get_consequences,
    get_page_full,
    get_page_summary,
    get_rooms,
    get_rule_details,
    get_rules_by_room_and_direction,
)
from typing import Optional


def register_read_tools(mcp):
    @mcp.tool(
        description="""Get all index entries. Always call this first to understand what knowledge is available before querying anything else. If result is empty, the knowledge base has no data yet. 
Do NOT call this tool again — just report that the database is empty and stop."""
    )
    def get_index_tool():
        results = get_index()
        return {"index_entries": results}
    
    @mcp.tool(
        description="""Get all Vastu directions with their associated deity and element. Use this to map a direction name to its id."""
    )
    def get_directions_tool():
        results = get_directions()
        return {"directions":results}
    
    @mcp.tool(
        description="""Get all consequences associated with a rule. Call when user asks about violations or effects."""
    )
    def get_consequences_tool(rule_id:int):
        results = get_consequences(rule_id)
        return {"consequences":results}
    
    @mcp.tool(
        description="""Get complete text of a page. Only call after get_page_summary when full detail is required."""

    )
    def get_page_full_tool(page_id:int):
        results = get_page_full(page_id)
        return {"page_full":results}
    
    @mcp.tool(
        description="""Get a brief summary of a specific page. Use this before get_page_full to decide if full context is needed."""
    )
    def get_page_summary_tool(page_num:int):
        results = get_page_summary(page_num)
        return {"page_summary":results}
    
    @mcp.tool(
        description="""Get all rooms/spaces with their aliases. Use this to map a room name to its id."""
    )
    def get_rooms_tool():
        results = get_rooms()
        return {"rooms":results}
    
    @mcp.tool(
        description="""Get full details of a specific rule including complete description. Use after browsing short descriptions."""
    )
    def get_rule_details_tool(rule_id:int):
        results = get_rule_details(rule_id)
        return {"rule_details":results}
    
    @mcp.tool(
        description="""Core lookup — get all Vastu rules for a specific room and direction combination. This is the primary tool for floor plan assessment. make sure pass proper arguments room_id:int and direction_id:int"""
    )
    def get_rules_by_room_and_direction_tool(
        room_id: Optional[int]=None, direction_id: Optional[int]=None
    ):
        
        results = get_rules_by_room_and_direction(room_id,direction_id)
        return {"rules_by_room_and_direction":results}
    
    