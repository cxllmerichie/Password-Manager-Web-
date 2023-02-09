CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,
    "username" TEXT UNIQUE NOT NULL,
    "avatar_url" TEXT DEFAULT NULL,
    "email" TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL PRIMARY KEY,
    "title" TEXT NOT NULL UNIQUE,
    "icon_url" TEXT DEFAULT NULL,
    "is_group" BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    "time" TIME NOT NULL,
    "duration" TIME NOT NULL DEFAULT '00:15:00',
    "title" TEXT NOT NULL,
    "caption" TEXT DEFAULT NULL,
    "visibility" INT NOT NULL DEFAULT 1,
    "administrators" INT ARRAY
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" SERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    "time" TIME NOT NULL,
    "text" TEXT NOT NULL,
    "media_url" TEXT DEFAULT NULL,
    "is_edited" BOOLEAN DEFAULT FALSE,
    "is_read" BOOLEAN DEFAULT FALSE,
    "sender_id" INT NOT NULL,
    "dialog_id" INT NOT NULL,
    CONSTRAINT "fk_dialog" FOREIGN KEY("dialog_id") REFERENCES "dialog"("id")
);