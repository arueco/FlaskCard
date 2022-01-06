from sqlite3 import *
import os
import random

def add_Deck(name):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("INSERT INTO Deck (name) VALUES ('%s')" % name)
    database.commit()
    database.close()

def add_Word(term,definition):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("INSERT INTO Word(term,def,knowledge_scale) VALUES (?,?,?)",(term,definition,1))
    database.commit()
    database.close()

def add_to_Belong():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT IdWord FROM Word")
    idDeck = save("see")
    idWord = cur.fetchall()[-1][0]

    cur.execute("INSERT INTO Belong(idDeck,idWord) VALUES (?,?)",(idDeck,idWord))
    database.commit()
    database.close()

def select_belong():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT * FROM Belong")
    return cur.fetchall()
def select_deck():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT * FROM Deck")
    return cur.fetchall()


def select_deck_edit(id):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT name FROM Deck WHERE idDeck = '%s'"%  id)
    return cur.fetchall()

def select_word():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT * FROM Word")
    return cur.fetchall()

def select_word_per_deck(idDeck):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT Word.idWord,term,def FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE Deck.idDeck = '%s'"% idDeck)
    return cur.fetchall()

def delete_deck_by_idDeck(idDeck):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("DELETE FROM Deck WHERE idDeck = '%s'"% idDeck)
    cur.execute("DELETE FROM Belong WHERE idDeck = '%s'"% idDeck)
    database.commit()
    database.close()



def clear_deck():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("DELETE FROM Deck")
    database.commit()
    database.close()
def clear_words():
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("DELETE FROM Word")
    database.commit()
    database.close()
def clear_word_edit(id):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("DELETE FROM Word WHERE idWord = '%s'"% id)
    cur.execute("DELETE FROM Belong WHERE idWord = '%s'"% id)
    database.commit()
    database.close()


def learn(idDeck):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT Word.idWord,term,def FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale BETWEEN 0 AND 2 AND Deck.idDeck ='%s'"%idDeck)
    notKnown = cur.fetchall()
    cur.execute("SELECT Word.idWord,term,def FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale BETWEEN 3 AND 5 AND Deck.idDeck ='%s'"%idDeck)
    known = cur.fetchall()
    cur.execute("SELECT Word.idWord,term,def FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale > 5 AND Deck.idDeck ='%s'"%idDeck)
    wellKnown = cur.fetchall()
    while len(wellKnown) != len(notKnown+known+wellKnown):
        if len(notKnown)!= 0:
            random_choice = random.randint(0,99)
            if 0<= random_choice <60 and len(notKnown) !=0:
                return notKnown[random.randint(0,len(notKnown)-1)]
            elif 60<=random_choice<90 and len(known) !=0:
                return known[random.randint(0,len(known)-1)]
            elif 90<=random_choice<100 and len(wellKnown) != 0:
                return wellKnown[random.randint(0,len(wellKnown)-1)]
        else:
            random_choice = random.randint(0, 99)
            if 0<= random_choice <60 and len(known) !=0:
                return known[random.randint(0,len(known)-1)]
            elif 60<= random_choice <100 and len(wellKnown):
                return wellKnown[random.randint(0,len(wellKnown)-1)]






def knowledge_scale_upgrade(idWord,answer,TrueAnswer):
    if answer.lower() == TrueAnswer.lower():
        database = connect("DataBases/flashcards_decks.db")
        cur = database.cursor()
        cur.execute("SELECT knowledge_scale FROM Word WHERE idWord = '%s'"% idWord)
        scale = cur.fetchall()[0][0]+1
        request = "UPDATE Word SET knowledge_scale = {} WHERE idWord = {}".format(scale,idWord)
        cur.execute(request)
        database.commit()
        database.close()
        return True
    elif answer != TrueAnswer:
        return False
    elif answer == "default":
        return 'default'




def count_knowledge_scale(idDeck):
    database = connect("DataBases/flashcards_decks.db")
    cur = database.cursor()
    cur.execute("SELECT COUNT(*) FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale BETWEEN 0 AND 2 AND Deck.idDeck ='%s'"%idDeck)
    notKnown = cur.fetchall()[0][0]
    cur.execute("SELECT COUNT(*) FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale BETWEEN 3 AND 5 AND Deck.idDeck ='%s'"%idDeck)
    known = cur.fetchall()[0][0]
    cur.execute("SELECT COUNT(*) FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE knowledge_scale > 5 AND Deck.idDeck ='%s'"%idDeck)
    wellKnown = cur.fetchall()[0][0]
    cur.execute("SELECT COUNT(*) FROM Belong INNER JOIN Word ON Belong.idWord = Word.idWord INNER JOIN Deck ON Belong.idDeck = Deck.idDeck WHERE Deck.idDeck = '%s'"%idDeck)
    total = cur.fetchall()[0][0]
    return (total,notKnown,known,wellKnown)




def save(method,id = 0):
    if method == "add":
        file = open('save.txt', 'w')
        file.write(id)
        file.close()
    elif method == "clear":
        file = open('save.txt', 'r+')
        file.truncate(0)
        file.close()
    elif method == "see":
        file = open('save.txt', 'r')
        value = file.read()
        file.close()
        return value
    elif method == "check_empty":
        return os.path.getsize("save.txt")

def save_answer(method,answer = ""):
    if method == "add":
        file = open('save_answer.txt', 'w')
        file.write(answer)
        file.close()
    elif method == "clear":
        file = open('save_answer.txt', 'r+')
        file.truncate(0)
        file.close()
    elif method == "see":
        file = open('save_answer.txt', 'r')
        value = file.read()
        file.close()
        return value
    elif method == "check_empty":
        return os.path.getsize("save_answer.txt")

def save_old_word(method,answer = []):
    if method == "add":
        if answer is not None:
            file = open('save_old_word.txt', 'w')
            for i in range (len(answer)):
                file.write(str(answer[i])+";")
            file.close()
    elif method == "clear":
        file = open('save_old_word.txt', 'r+')
        file.truncate(0)
        file.close()
    elif method == "see":
        file = open('save_old_word.txt', 'r')
        value = file.read()
        string =""
        list_value = []
        for i in range (len(value)):
            if value[i] == ";":
                list_value.append(string)
                string = ""
            else:
                string += value[i]

        file.close()
        return list_value
    elif method == "check_empty":
        return os.path.getsize("save_old_word.txt")

