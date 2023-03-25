CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,

    "avatar" BYTEA DEFAULT NULL,
    "email" TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL PRIMARY KEY,

    "icon" BYTEA DEFAULT NULL,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "user" ("id")
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL PRIMARY KEY,

    "icon" BYTEA DEFAULT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT DEFAULT NULL,
    "expiration_date" TIMESTAMP DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "category_id" INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "category" ("id")
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" SERIAL PRIMARY KEY,

    "name" BYTEA NOT NULL,
    "value" BYTEA NOT NULL,

    "item_id" INT NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);