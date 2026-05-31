from .connection import SessionLocal
from src.vasthu_knowledge_mcp.models import (
    Direction,
    Room,
    Page,
    Rule,
    Consequence,
    IndexEntry,
    RuleMapping
)
from typing import Optional


def get_index():
    # get_index() — entry point, model reads this first
    with SessionLocal() as session:
        return session.query(IndexEntry).all()
    
def get_rules_by_room_and_direction(
    room_id: Optional[int] = None, direction_id: Optional[int] = None
):
    with SessionLocal() as session:
        query = session.query(RuleMapping)
        if room_id is not None:
            query = query.filter(RuleMapping.room_id == room_id)
        if direction_id is not None:
            query = query.filter(RuleMapping.direction_id == direction_id)
        return query.all()
    
def get_page_summary(page_num:int):
    # get_page_summary(page_num)
    with SessionLocal() as session:
        page = session.query(Page).filter(Page.page_num == page_num).first()
    return page.summary if page else None


def get_page_full(page_id:int):
    # get_page_full(page_id) — lazy load
    with SessionLocal() as session:
        return session.query(Page).filter(Page.id == page_id).first()
    
def get_rule_details(rule_id:int):
    # get_rule_detail(rule_id) — lazy load
    with SessionLocal() as session:
        return session.query(Rule).filter(Rule.id == rule_id).first()
    
def get_consequences(rule_id:int):
    # get_consequences(rule_id) — lazy load
    with SessionLocal() as session:
        return session.query(Consequence).filter(Consequence.rule_id == rule_id).all()
    
def get_rooms():
    # get_rooms() — list all rooms
    with SessionLocal() as session:
        return session.query(Room).all()
    
def get_directions():
    # get_directions() — list all directions
    with SessionLocal() as session:
        return session.query(Direction).all()