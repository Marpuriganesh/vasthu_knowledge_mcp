```sql
-- Lookup tables
CREATE TABLE directions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,        -- "North", "South-East" etc
    deity TEXT,                -- "Agni", "Indra" etc
    element TEXT               -- "Fire", "Water" etc
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,        -- "Kitchen"
    aliases TEXT               -- "cooking area, pantry" comma separated
);

-- Index table (model's entry point)
CREATE TABLE index (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,       -- "Kitchen Placement"
    category TEXT,             -- "Room Rules", "Direction Rules", "General"
    keywords TEXT,             -- "kitchen, fire, SE, Agni"
    page_refs TEXT,            -- "45, 46, 47"
    rule_count INTEGER
);

-- Pages with lazy loading
CREATE TABLE pages (
    id INTEGER PRIMARY KEY,
    page_num INTEGER NOT NULL,
    summary TEXT,              -- model reads this first
    full_text TEXT             -- loaded on demand
);

-- Core knowledge
CREATE TABLE rules (
    id INTEGER PRIMARY KEY,
    index_id INTEGER REFERENCES index(id),
    page_id INTEGER REFERENCES pages(id),
    short_desc TEXT NOT NULL,  -- model reads this first
    full_detail TEXT,          -- loaded on demand
    compatibility INTEGER      -- -2 to 2
);

-- Heart of the system
CREATE TABLE rule_mappings (
    id INTEGER PRIMARY KEY,
    rule_id INTEGER REFERENCES rules(id),
    room_id INTEGER REFERENCES rooms(id),        -- nullable
    direction_id INTEGER REFERENCES directions(id) -- nullable
);

-- Loaded only when needed
CREATE TABLE consequences (
    id INTEGER PRIMARY KEY,
    rule_id INTEGER REFERENCES rules(id),
    description TEXT,
    severity INTEGER           -- -2 to 2
);
```