sql = '''
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BYTEA NOT NULL,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BYTEA NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT DEFAULT NULL,
    "expires_at" TIMESTAMP DEFAULT NULL,
    "modified_at" TIMESTAMP DEFAULT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "category_id" INTEGER NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "category" ("id")
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" TEXT PRIMARY KEY,

    "name" BYTEA NOT NULL,
    "value" BYTEA NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "attachment" (
    "id" TEXT PRIMARY KEY,

    "content" BYTEA NOT NULL,
    "mime" TEXT NOT NULL,
    "filename" TEXT NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "map" (
    "key" TEXT,
    "value" BYTEA
);
'''