CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,

    "avatar" BYTEA NOT NULL,
    "email" TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL PRIMARY KEY,

    "icon" BYTEA NOT NULL,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "user" ("id")
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" UUID PRIMARY KEY,

    "icon" BYTEA NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT DEFAULT NULL,
    "expires_at" TIMESTAMP DEFAULT NULL,
    "modified_at" TIMESTAMP DEFAULT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "attachments" BYTEA[] NOT NULL DEFAULT '{}',
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "category_id" INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "category" ("id")
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" UUID PRIMARY KEY,

    "name" BYTEA NOT NULL,
    "value" BYTEA NOT NULL,

    "item_id" UUID NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);