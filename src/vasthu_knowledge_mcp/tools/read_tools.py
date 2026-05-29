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


def register_read_tools(mcp):
    @mcp.tool(
        description="""Get all index entries. Always call this first to understand what knowledge is available before querying anything else."""
    )
    def get_index_tool():
        return get_index()
    
    @mcp.tool(
        description="""Get all Vastu directions with their associated deity and element. Use this to map a direction name to its id."""
    )
    def get_directions_tool():
        return get_directions()
    
    @mcp.tool(
        description="""Get all consequences associated with a rule. Call when user asks about violations or effects."""
    )
    def get_consequences_tool(rule_id:int):
        return get_consequences(rule_id)
    
    @mcp.tool(
        description="""Get complete text of a page. Only call after get_page_summary when full detail is required."""

    )
    def get_page_full_tool(page_id:int):
        return get_page_full(page_id)
    
    @mcp.tool(
        description="""Get a brief summary of a specific page. Use this before get_page_full to decide if full context is needed."""
    )
    def get_page_summary_tool(page_num:int):
        return get_page_summary(page_num)
    
    @mcp.tool(
        description="""Get all rooms/spaces with their aliases. Use this to map a room name to its id."""
    )
    def get_rooms_tool():
        return get_rooms()
    
    @mcp.tool(
        description="""Get full details of a specific rule including complete description. Use after browsing short descriptions."""
    )
    def get_rule_details_tool(rule_id:int):
        return get_rule_details(rule_id)
    
    @mcp.tool(
        description="""Core lookup — get all Vastu rules for a specific room and direction combination. This is the primary tool for floor plan assessment."""
    )
    def get_rules_by_room_and_direction_tool(room_id:int,direction_id:int):
        return get_rules_by_room_and_direction(room_id,direction_id)
    
    