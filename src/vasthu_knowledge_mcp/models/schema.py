from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Direction(Base):
    __tablename__ = "directions"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    deity = Column(String)
    element = Column(String)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aliases = Column(String)


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    page_num = Column(Integer, nullable=False)
    summary = Column(String(600))
    full_text = Column(String)


class IndexEntry(Base):
    __tablename__ = "index_entries"

    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    category = Column(String)
    keywords = Column(String)
    page_refs = Column(String)
    rule_count = Column(Integer)


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    index_id = Column(Integer, ForeignKey("index_entries.id"))
    page_id = Column(Integer, ForeignKey("pages.id"))
    short_desc = Column(String(600))
    full_detail = Column(String)
    compatibility = Column(Integer)  # -2 (avoid) to 2 (auspicious)


class RuleMapping(Base):
    __tablename__ = "rules_mappings"

    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey("rules.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    direction_id = Column(Integer, ForeignKey("directions.id"), nullable=True)


class Consequence(Base):
    __tablename__ = "consequences"

    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey("rules.id"))
    description = Column(String(500))
    severity = Column(Integer)  # -2 (severe) to 2 (minor)
