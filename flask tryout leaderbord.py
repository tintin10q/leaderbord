from flask import Flask, render_template, redirect, url_for, request
import json


class Database():
    # This class is used to wrie and read stuff with the database
    def __init__(self, file):
        self.file = file

    def get(self):
        with open(self.file, "r") as f:
            data = json.load(f)
            f.close()
            return data

    def set(self, data, sort=False):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=2, sort_keys=sort)
            f.close()
            return data

    def add(self, new_data):
        data = self.get()
        data["people"].update(new_data)
        self.set(data)
        return

    def remove(self, person,type="person"):
        if type == "person":
            try:
                data = self.get()
                data["people"].pop(person)
                self.set(data)
                return True
            except:
                return False


app = Flask(__name__)
db = Database("scoreboard.json")


# Give someone a score
@app.route("/update_score/<USER>!<POINTS>/",)
def give_points(USER, POINTS):
    USER = USER.lower()
    try:
        POINTS = int(POINTS)
        data = db.get()
        data["people"][USER]["punten"] += POINTS
        nieuwe_punten = data["people"][USER]["punten"]
        db.set(data, sort=True)
        return "{a} heeft {b} erbij.<br> {a} heeft nu {c} punten.".format(a=USER, b=POINTS,c=nieuwe_punten)
    except:
        return "<b>Something went wrong.<br>Make sure {a} is registered.</b>".format(a=USER)

# Add new user to database
@app.route("/register/<USER>/")
def register_user(USER, LEEFTIJD=-1):
    USER = USER.upper()
    db.add({USER: {"leeftijd": LEEFTIJD, "punten": 0}})
    return "{USER} has been registered".format(USER=USER)

# Delete a user from the database with password
@app.route("/delete/<USER>/",methods=['POST','GET'])
def delete_user(USER):
    USER = USER.lower()
    if request.method == "POST":
        password = request.form['goed']
        if password == "gietertje":
            if db.remove(USER):
                return "{USER} has been deleted from the database".format(USER=USER)
            else:
                return "<b>Something went wrong.<br>Are you sure that {} is a registered person?</b>".format(USER)
    else:
        return render_template('login.html',return_point='delete/{}'.format(USER))

# Show scoreboard
@app.route("/scoreboard/")
def display_scoreboard():
    # dispaly een scoreboard met alle
    # dit is gewoon erg leleijke manier om een lijst te krijgen met een lisjt zoals dit: [[score,naam,id],etc]
    data = db.get()
    namen_lijst = [i.upper() for i in data["people"]]
    score_lijst = [data["people"][i]["punten"] for i in data["people"]]
    print(score_lijst)
    final_lijst = [[i] for i in score_lijst]
    count = 0
    for i in namen_lijst:
        final_lijst[count].append(i)
        count += 1
    count = 1
    final_lijst.sort(reverse=True)
    for i in final_lijst:
        i.append(str(count)+".")
        count += 1


    return render_template("scoreboard.html",final_lijst=final_lijst)

# reset de scoreboard login is nodig
@app.route("/clear_scoreboard/",methods=['POST','GET'])
def clear():
    if request.method == "POST":
        password = request.form['goed']
        if password == "gietertje":
            db.set({"people":{}})
            return "<b>Scoreboard has been destroyed</b>"
        else:
            return "<b>Wrong password!</b>"
    else:
        return render_template("login.html",return_point="clear_scoreboard")

@app.route("/")
def home():
    return redirect(url_for('display_scoreboard'))

if __name__ == "__main__":
    app.run()
