from flask import Flask, render_template,request,redirect,url_for
from functions import *
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/decks",methods=['POST','GET'])
def decks():
    save("clear")
    if request.method == 'POST':
        new_deck = request.form.get('nm-deck')
        if type(new_deck) == str and new_deck != '':
            add_Deck(new_deck)

    listDeck = select_deck()
    return render_template("decks.html", listDeck = listDeck)
@app.route("/decks/confirm_delete",methods=['POST','GET'])
def delete_deck():
    delete = request.form["list_deck_delete"]
    delete_deck_by_idDeck(delete)
    return redirect(url_for('decks'))

@app.route("/decks/edit",methods=['POST','GET'])
def edit_decks():
    if save("check_empty") == 0:
        select = request.form["list_deck"]
        save("add", select)
    if request.method == 'POST':
        term = request.form.get("term")
        definition = request.form.get("def")
        if type(term) == str and term != '' and type(definition) == str and definition != '':
            add_Word(term, definition)
            add_to_Belong()
    select = save("see")
    name_deck = select_deck_edit(select)
    listWord = select_word_per_deck(select)
    return render_template("deck_edit.html",listWord = listWord,name_deck=name_deck[0][0])

@app.route("/decks/edit/delete_confirm",methods=['POST','GET'])
def delete_word():
    delete = request.form["select_word"]
    clear_word_edit(delete)
    return redirect(url_for('edit_decks'))

@app.route("/study/choice",methods=['POST','GET'])
def choice():
    save_old_word("clear")
    save("clear")
    save_answer("clear")
    listDeck = select_deck()
    return render_template("deck_choice.html",listDeck = listDeck)


@app.route("/study",methods=['POST','GET'])
def study():
    if save("check_empty") == 0:
        select = request.form["study_deck"]
        save("add", select)
    select = save("see")
    name_deck = select_deck_edit(select)
    word = learn(select)
    stats = count_knowledge_scale(select)
    if  save_old_word("check_empty") == 0:
        old_word = ""
    else:
        old_word = save_old_word("see")
    save_old_word("clear")
    save_old_word("add",word)
    answer = save_answer("see")
    answer_test = "default"
    if type(old_word) == list:
        answer_test = knowledge_scale_upgrade(old_word[0], answer, old_word[2])
    print(answer_test)

    return render_template("study.html",word = word,total = stats[0] ,notKnown=stats[1],known = stats[2],wellKnown = stats[3],name_deck = name_deck [0][0],answer = answer,old_word = old_word,answer_test = answer_test)

@app.route("/study/answer",methods=['POST','GET'])
def answer():
    save_answer("clear")
    answer = request.form["answer_user"]
    save_answer("add", answer)

    return redirect(url_for("study"))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1664,debug=True)