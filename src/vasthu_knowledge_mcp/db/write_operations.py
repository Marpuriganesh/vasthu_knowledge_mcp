from typing import Optional
from .connection import SessionLocal
from src.vasthu_knowledge_mcp.models import (
    Direction,
    Room,
    Page,
    Rule,
    Consequence,
    IndexEntry,
    RuleMapping,
)


def insert_direction(name: str, deity: str, element: str):
    with SessionLocal() as session:
        direction = Direction(name=name, deity=deity, element=element)
        session.add(direction)
        session.commit()


def insert_room(name: str, aliases: str):
    with SessionLocal() as session:
        room = Room(name=name, aliases=aliases)
        session.add(room)
        session.commit()


def insert_page(page_num: int, summary: str, full_text: str):
    with SessionLocal() as session:
        page = Page(page_num=page_num, summary=summary, full_text=full_text)
        session.add(page)
        session.commit()


def insert_index_entry(
    topic: str, category: str, keywords: str, page_refs: str, rule_count: int
):
    with SessionLocal() as session:
        index = IndexEntry(
            topic=topic,
            category=category,
            keywords=keywords,
            page_refs=page_refs,
            rule_count=rule_count,
        )
        session.add(index)
        session.commit()


def insert_rule(
    index_id: int, page_id: int, short_desc: str, full_detail: str, compatibility:int
):
    with SessionLocal() as session:
        rule = Rule(
            index_id=index_id,
            page_id=page_id,
            short_desc=short_desc,
            full_detail=full_detail,
            compatibility=compatibility,
        )
        session.add(rule)
        session.commit()


def insert_rule_mapping(rule_id: int, room_id: Optional[int] = None, direction_id: Optional[int] = None):
    with SessionLocal() as session:
        rule_mapping = RuleMapping(
            rule_id=rule_id, room_id=room_id, direction_id=direction_id
        )
        session.add(rule_mapping)
        session.commit()


def insert_consequence(rule_id:int,description:str,severity:int):
    with SessionLocal() as session:
        consequence = Consequence(
            rule_id=rule_id, description=description, severity=severity
        )
        session.add(consequence)
        session.commit()