DROP TABLE User;
DROP TABLE Category;
DROP TABLE Item;
DROP TABLE Field;


CREATE TABLE User (
    UserID INTEGER PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Surname TEXT,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL
);

CREATE TABLE Category (
    CategoryID INTEGER PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Description TEXT,
    FOREIGN KEY (CategoryID) REFERENCES User (UserID)
);

CREATE TABLE Item (
    ItemID INTEGER PRIMARY KEY NOT NULL,
    Title TEXT NOT NULL,
    Description TEXT,
    FOREIGN KEY (ItemID) REFERENCES Category (CategoryID)
);

CREATE TABLE Field (
    FieldID INTEGER PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Value TEXT,
    FOREIGN KEY (FieldID) REFERENCES Item (ItemID)
);


INSERT INTO User VALUES (0, "cxllmerichie", NULL, "root", "root");
INSERT INTO Category () VALUES (1, "category", NULL, (0));
