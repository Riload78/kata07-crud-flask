CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"abstract"	TEXT NOT NULL,
	"amount"	REAL NOT NULL,
	"currency"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);