from sqlite3 import *


database = connect('DataBases/flashcards_decks.db')
cur = database.cursor()
#1ère table :
#Nom : Deck
#Nom valeur 1: idDeck -> Primary key
#Nom valeur 2: name
cur.execute("CREATE TABLE Deck (idDeck INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT)")



#seconde table
#Nom : Word
#Nom valeur 1: idWord -> Primary key
#Nom valeur 2: term
#Nom valeur 3: def

cur.execute("CREATE TABLE Word (idWord INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT, def TEXT, knowledge_scale INTEGER)")

#troisième table:
#Nom: Belong
#Nom valeur 1 : idDeck  -> Primary key / Foreign key references Deck
#Nom valeur 2 : idWord -> Primary key / Foreign key references Word

cur.execute("CREATE TABLE Belong (idDeck INTEGER NOT NULL, idWord INTEGER NOT NULL, FOREIGN KEY(idDeck) REFERENCES Deck(idDeck), FOREIGN KEY(idWord) REFERENCES Word(idWord))")



database.commit()
database.close()





