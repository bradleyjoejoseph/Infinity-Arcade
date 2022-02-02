from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime
from cs50 import SQL
from flask_session import Session
import os
#cs50 finance helpers.py login_require function
from login_fix import login_required
import random

#app config
app = Flask(__name__)
admins = [8]


app.config["TEMPLATES_AUTO_RELOAD"] = True


#session config
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#database config
db = SQL("sqlite:///network.db")


#routes
@app.route("/")
def index():
    count = db.execute("select count(*) from users;")
    return render_template("welcome.html", count=count[0]["count(*)"])

@app.route("/home")
@login_required
def home():
    adminPanelAccess = session["id"] in admins
    recents = db.execute("WITH cte1 AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY userID, name ORDER BY time DESC) rn1 FROM history), cte2 AS ( SELECT *, ROW_NUMBER() OVER (PARTITION BY userID ORDER BY time DESC) rn2 FROM cte1 WHERE rn1 = 1 ) SELECT userID, name, image, time FROM cte2 WHERE rn2 <= 5 and userID = ?", session["id"])
    username = db.execute("select username from users where id = ?", session["id"])
    cash = db.execute("select cash from users where id = ?", session["id"])
    popular = db.execute("select image, name, count(*) as count from history group by name order by count desc")
    adminPanel = ""
    if adminPanelAccess == True:
        adminPanel = "<li class='nav-item'><a href='/adminPanel' class='nav-link' style='color:#00bfff;'>adminPanel</a></li>"
    return render_template("index.html", username=username[0]["username"], cash=shorten(cash[0]["cash"]), games=recents, popular=popular, adminPanel=adminPanel)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return render_template("error.html", error="Enter a Username", code="400")
        if not password:
            return render_template("error.html", error="Enter a Password", code="400")
        users = db.execute("select * from users where username = ?", username)
        resultLineCount = len(users)
        if resultLineCount != 1:
            return render_template("error.html", error="Your Username May Be Incorrect", code="400")
        if not check_password_hash(users[0]["password"], password):
            return render_template("error.html", error="Your Password is Incorrect", code="400")

        session["id"] = users[0]["id"]
        session["multiplier"] = 1
        session["jackpot"] = 1000
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        others = db.execute("select username from users")
        for i in range(len(others)):
            if username == others[i]["username"]:
                return render_template("error.html", error="Username is Taken", code="400")
        if not username:
            return render_template("error.html", error="Enter a Username", code="400")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return render_template("error.html", error="Enter a Password", code="400")
        if password != confirmation:
            return render_template("error.html", error="Confirm Your Password", code="400")

        db.execute("insert into users (username, password) values(?, ?)", username, generate_password_hash(password))
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/apps")
def apps():
    games = db.execute("select * from games")
    earnable = db.execute("select name, image from games where money = ?", "true")
    popular = db.execute("select image, name, count(*) as count from history group by name order by count desc")
    multi = db.execute("select name, image from games where money = ?", "multi")
    fun = db.execute("select name, image from games where money = ?", "false")
    return render_template("apps.html", games=games, popular=popular, earnable=earnable, fun=fun, multi=multi)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


# apps

@app.route("/infiniteSpinner")
@login_required
def infiniteSpinner():
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Infinite Spinner", "infiniteSpinner", now)
    values = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    icons = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
    cash = db.execute("select cash from users where id = ?", session["id"])
    cash = cash[0]["cash"]
    multiplier = int(session["multiplier"])
    points = 0
    count = 0
    warning = ""
    jackpot = int(session["jackpot"])
    if cash < multiplier:
        return render_template("error.html", error="You do not have enough money!", code="400")
    for i in range(len(values)):
        for j in range(len(values[i])):
            one = [1, 2]
            two = [3, 4, 5, 6]
            three = [7, 8, 9, 10, 11, 12, 13, 14]
            four = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
            five = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 31, 32]
            decider = random.randint(1,33)
            if decider in one:
                values[i][j] = 10
                icons[i][j] = "Legendary"
                count += 1
            elif decider in two:
                values[i][j] = 7
                icons[i][j] = "Epic"
            elif decider in three:
                values[i][j] = 5
                icons[i][j] = "Rare"
            elif decider in four:
                values[i][j] = 3
                icons[i][j] = "Uncommon"
            elif decider in five:
                values[i][j] = 1
                icons[i][j] = "Common"
    message = ""
    if values[0][0] == values[0][1] == values[0][2] == values[0][3]:
        points += values[0][0] * multiplier
        message = "Four " + icons[0][0] + "s In First Row!"
    if values[0][0] == values[1][1] == values[1][2] == values[2][3]:
        points += values[0][0] * multiplier
        message = icons[0][0] + " Left Diagonal!"
    if values[0][0] == values[2][1] == values[2][2] == values[0][3]:
        points += values[0][0] * multiplier
        message = icons[0][0] + "s Ice Cream Cone!"
    if values[1][0] == values[1][1] == values[1][2] == values[1][3]:
        points += values[1][0] * multiplier
        message = "Four " + icons[1][0] + "s In Second Row!"
    if values[2][0] == values[2][1] == values[2][2] == values[2][3]:
        points += values[2][0] * multiplier
        message = "Four " + icons[2][0] + "s In Third Row!"
    if values[2][0] == values[1][1] == values[1][2] == values[0][3]:
        points += values[2][0] * multiplier
        message = icons[2][0] + " Right Diagonal!"
    if values[2][0] == values[0][1] == values[0][2] == values[2][3]:
        points += values[2][0] * multiplier
        message = icons[2][0] + " Cone!"
    bet = multiplier
    cash = cash - 1 * multiplier
    if count >= 3:
        points += count * 10 * multiplier
    cash += points
    won = points

    if count >= 3:
        message = str(count) + " Gem Win!"

    if (cash / 100) > bet:
        warning = "It is recommended that you increase your bet to recieve the nessesary winnings. Click here to dismiss this warning"

    randomNum1 = random.randint(1,1000)
    randomNum2 = random.randint(1,1000)
    if randomNum1 == randomNum2:
        cash += jackpot * multiplier
        message = "JACKPOT!!!"
        won += jackpot
        jackpot = 1000

    session["jackpot"] = jackpot + bet
    db.execute("update users set cash = ? where id = ?", cash, session["id"])

    return render_template("infiniteSpinner.html", icons=icons, cash=shorten(cash), bet=shorten(bet), won=shorten(won), message=message, warning=warning, jackpot=jackpot)

@app.route("/arcadeMathematicians")
@login_required
def arcadeMath():
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Arcade Mathematicians", "arcadeMathematicians", now)
    cash = db.execute("select cash from users where id = ?", session["id"])
    cash = cash[0]["cash"]
    return render_template("arcadeMathematicians.html", cash=shorten(cash))

@app.route("/cps", methods=["GET", "POST"])
@login_required
def cps():
    if request.method == "POST":
        clicks = float(request.form.get("klix"))
        username = db.execute("select username from users where id = ?", session["id"])
        db.execute("insert into clicker (username, clicks) values(?, ?)", username[0]["username"], round(clicks, 2))
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "CPS Master", "cps", now)
    leaderboard = db.execute("select distinct * from clicker order by clicks desc limit 100")
    return render_template("cps.html", leaderboard=leaderboard)

@app.route("/blackjack", methods=["GET", "POST"])
@login_required
def blackjack():
    if request.method == "POST":
        postType = str(request.form.get("postType"))
        if postType == "play":
            cash = db.execute("select cash from users where id = ?", session["id"])
            cash = cash[0]["cash"]
            bet = int(session["multiplier"])
            won = 0
            cash = cash - bet
            db.execute("update users set cash = ? where id = ?", cash, session["id"])
            return render_template("blackjack.html", cash=shorten(cash), bet=shorten(bet), won=shorten(won), postType=postType)
        if postType == "won":
            who = request.form.get("won")
            cash = db.execute("select cash from users where id = ?", session["id"])
            cash = cash[0]["cash"]
            bet = int(session["multiplier"])
            won = 0
            if who == "player":
                cash = cash + (bet*2)
                won = bet
            db.execute("update users set cash = ? where id = ?", cash, session["id"])
            return render_template("blackjack.html", cash=shorten(cash), bet=shorten(bet), won=shorten(won), postType=postType)
    else:
        now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Blackjack", "blackjack", now)
        cash = db.execute("select cash from users where id = ?", session["id"])
        cash = cash[0]["cash"]
        bet = int(session["multiplier"])
        if cash < bet:
            return render_template("error.html", error="You do not have enough money!", code="400")
        won = 0
        return render_template("blackjack.html", cash=shorten(cash), won=shorten(won), bet=shorten(bet))

@app.route("/poker", methods=["GET", "POST"])
@login_required
def gamePoker():
    if request.method == "POST":
        postType = str(request.form.get("postType"))
        if postType == "play":
            cash = db.execute("select cash from users where id = ?", session["id"])
            cash = cash[0]["cash"]
            bet = int(session["multiplier"])
            won = 0
            cash = cash - bet
            db.execute("update users set cash = ? where id = ?", cash, session["id"])
            return render_template("poker.html", cash=shorten(cash), bet=shorten(bet), won=shorten(won), postType=postType)
        if postType == "won":
            cash = db.execute("select cash from users where id = ?", session["id"])
            cash = cash[0]["cash"]
            bet = int(session["multiplier"])
            earned = request.form.get("earned")
            won = bet * int(earned)
            if int(earned) > 0:
                cash += 1
                cash += int(won)
            db.execute("update users set cash = ? where id = ?", cash, session["id"])
            return render_template("poker.html", cash=shorten(cash), bet=shorten(bet), won=shorten(won), postType=postType)
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Poker", "poker", now)
    cash = db.execute("select cash from users where id = ?", session["id"])
    cash = cash[0]["cash"]
    bet = int(session["multiplier"])
    won = 0
    return render_template("poker.html", cash=shorten(cash), bet=shorten(bet), won=shorten(won))

@app.route("/aim")
@login_required
def aim():
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Aim Trainer", "aim", now)
    return render_template("aim.html")

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    chats = db.execute("select * from chat order by time asc;")
    if request.method == "POST":
        now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        username = db.execute("select username from users where id = ?", session["id"])
        if request.form.get("message") == "/clear":
            if session["id"] in admins:
                db.execute("delete from chat")
                return render_template("chat.html", chats=chats)
        db.execute("insert into chat (username, message, time) values(?, ?, ?)", username[0]["username"], request.form.get("message"), now)
        return render_template("chat.html", chats=chats)
    now = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
    db.execute("insert into history (userID, name, image, time) values(?, ?, ?, ?)", session["id"], "Chat!", "chat", now)
    return render_template("chat.html", chats=chats)

# apps

@app.route("/leaderboard")
@login_required
def leaderboard():
    leaderboard = db.execute("select id, cash, username from users order by cash desc")
    for i in range(len(leaderboard)):
        leaderboard[i]["cash"] = shorten(leaderboard[i]["cash"])
        ending = "th"
        testSubject = str(i + 1)[-1]
        if testSubject == "1":
            ending = "st"
        elif testSubject == "2":
            ending = "nd"
        elif testSubject == "3":
            ending = "rd"
        if i > 8:
            if str(i + 1)[-2] == "1":
                ending = "th"
        leaderboard[i]["Place"] = str(i + 1) + ending



        if leaderboard[i]["id"] == session["id"]:
            thisUser = leaderboard[i]["Place"]
        while len(leaderboard) > 100:
            del leaderboard[100]
    return render_template("leaderboard.html", leaderboard=leaderboard, thisUser=thisUser)

@app.route("/updates")
@login_required
def updates():
    return render_template("updates.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        try:
            if int(request.form.get("multiplier")) >= 0:
                multiplier = request.form.get("multiplier")
            else:
                multiplier = 0
        except:
            return render_template("error.html", error="Enter a valid integer.", code="400")
        session["multiplier"] = multiplier
        return redirect("/home")
    return render_template("settings.html")

@app.route("/FAQ", methods=["GET", "POST"])
@login_required
def faq():
    if request.method == "POST":
        question = request.form.get("cuestion")
        db.execute("insert into faq (userID, question) values(?, ?)", session["id"], question)
        return render_template("FAQ.html")
    else:
        return render_template("FAQ.html")

@app.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    average = 0
    count = 0
    reviewsList = db.execute("select * from reviews order by rating desc")
    for i in range(len(reviewsList)):
        average += reviewsList[i]["rating"]
        count += 1
    if count == 0:
        count = 1
    average = round(average / count, 2)
    if request.method == "POST":
        username = db.execute("select username from users where id = ?", session["id"])
        rating = request.form.get("stars")
        title = request.form.get("title")
        opinion = request.form.get("text")
        db.execute("insert into reviews (username, rating, title, opinion) values(?, ?, ?, ?)", username[0]["username"], rating, title, opinion)

        return render_template("reviews.html", reviewsList=reviewsList, average=average)
    else:
        return render_template("reviews.html", reviewsList=reviewsList, average=average)

# admin things

@app.route("/adminPanel")
@login_required
def admin():
    if session["id"] in admins:
        return render_template("adminPanel.html")
    return render_template("error.html", error="Nice try!", code="But you failed!")

@app.route("/getQuestions")
@login_required
def gq():
    if session["id"] in admins:
        output = db.execute("select * from faq")
        return render_template("get.html", output=output)
    return render_template("error.html", error="Nice try!", code="But you failed!")

@app.route("/getUsers")
@login_required
def gU():
    if session["id"] in admins:
        output = db.execute("select * from users")
        return render_template("get.html", output=output)


@app.route("/getDelete", methods=["GET", "POST"])
@login_required
def gD():
    if session["id"] in admins:
        if request.method == "POST":
            userID = int(request.form.get("userId"))
            db.execute("delete from users where id = ?", userID)
            return render_template("delete.html")
        return render_template("delete.html")
    return render_template("error.html", error="Nice try!", code="But you failed!")

@app.route("/getCash", methods=["GET", "POST"])
@login_required
def gC():
    if session["id"] in admins:
        if request.method == "POST":
            userID = int(request.form.get("userId"))
            cash = int(request.form.get("cash"))
            db.execute("update users set cash = ? where id = ?", cash, userID)
        return render_template("cash.html")
    return render_template("error.html", error="Nice try!", code="But you failed!")
# admin things

# game infos
@app.route("/infiniteSpinner/info")
def infiniteSpinnerInfo():
    name = "Infinite Spinner"
    info = "Infinite Spinner is a game where you spin to match either 3 or more gems or make a line of one object to the other side in a specific way to gain money depending on how valuable the object is.<br><br>Value table:<br> <table style='margin-right:50px; float:left;'> <tr><th>Object</th> <th>Value</th></tr> <tr><td><img style='height:100px;' src='/static/Common.png'></td><td>£1</td></tr><tr><td><img style='height:100px;' src='/static/Uncommon.png'></td><td>£3</td></tr><tr><td><img style='height:100px;' src='/static/Rare.png'></td><td>£5</td></tr><tr><td><img style='height:100px;' src='/static/Epic.png'></td><td>£7</td></tr><tr><td><img style='height:100px;' src='/static/Legendary.png'></td><td>£10</td></tr></table>Combinations table: <table><tr><th>11</th><th>12</th><th>13</th><th>14</th></tr><tr><th>21</th><th>22</th><th>23</th><th>24</th></tr><tr><th>31</th><th>32</th><th>33</th><th>34</th></tr><table><br>11, 12, 13, 14 - Four In The First Row<br>11, 22, 23, 34 - Left Diagonal<br>11, 32, 33, 14 - Ice Cream Cone<br>21, 22, 23, 24 - Four In The Second Row<br>31, 32, 33, 34 - Four in The Third Row<br>31, 22, 23, 14 - Right Diagonal<br>31, 12, 13, 34 - Cone<br><br><br><br><br><br><br><br><br><br><br><br>Bets automatically applied. Mouse required. All Device Support."
    url = "infiniteSpinner"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/arcadeMathematicians/info")
def arcadeMathematiciansInfo():
    name = "Arcade Mathematicians"
    info = "Arcade Mathematicians is a game where you can test your times table skills. Heavily inspired by TTRS.<br><br>This games requires a keyboard. No bets. No timer. No mobile support."
    url = "arcadeMathematicians"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/blackjack/info")
def blackjackInfo():
    name = "Blackjack"
    info = "Blackjack is a casino game. It is played with a standard 52 deck. Aces count as one. Firm bet, cannot be doubled in the middle. Aim is to reach 21 without exeeding it. If player and dealer draw player must hit once more then stand if not exeeded.<br><br>No keyboard input needed. Mouse gameplay, bets applied at in-game play button. WARNING: Press reload button at the end of the game to claim your won money. You have been warned. All Device Support."
    url = "blackjack"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/poker/info")
def pokerInfo():
    name = "Poker"
    info = "Poker is a casino game. Video Poker: Jacks or Better. 5 cards are drawn at random, certain combinations win money, uses standard video poker combinations which include Royal Flush, Straight Flush, Four of a Kind, Full house, Flush, Straight, Three of a Kind, Two of a Kind and Jacks or Better. <a target='_blank' href='https://www.casinoreports.ca/video-poker/rules/'>Use this link for more information on how to play.</a><br><br>No keyboard input needed. Mouse gameplay, bets applied at in-game play button. WARNING: Press reload button at the end of the game to claim your won money. You have been warned. No mobile support."
    url = "poker"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/cps/info")
def cpsInfo():
    name = "CPS Master"
    info = "CPS Master is a game where you click your mouse or tap your screen as fast as possible, see if you can get on the leaderboard! Please don't use autoclicker as this ruins the fun of this game. You can set your time for clicking at the bottom next to the leaderboard. The leaderboard only has the top 100 player's scores.<br><br>This game requires a mouse. Keyboard optional. No bets. Timer can be set or defaults to one second. All Device Support."
    url = "cps"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/aim/info")
def aimInfo():
    name = "Aim Trainer"
    info = "Aim Trainer is a game where you can choose your settings and train your reflexes and aiming skills.<br><br>This game requires a mouse. Keyboard optional. No bets. Other settings included in-game. Computer support only."
    url = "aim"
    return render_template("appWelcome.html", name=name, info=info, url=url)

@app.route("/chat/info")
def chatInfo():
    name = "Chat!"
    info = "A place where you can chat with people all across the world! <br><br>You will need to reload using the refresh button at the extreme top right of the page a few times to see other people's replies. We are working to get it to be instant. All device support."
    url = "chat"
    return render_template("appWelcome.html", name=name, info=info, url=url)

# game infos

def shorten(cash):
    magnitude = 0
    if cash < 0:
        cash * -1
    while abs(cash) >= 1000:
        magnitude += 1
        cash /= 1000
        if magnitude >= 3:
            magnitude -= 1;
            cash *= 1000
    return "%.2f%s" % (cash, ["", "K", "M", "B", "T", "Qua", "Qui", "Sx", "Sp", "Oc", "N", "Dc", "UD", "DD", "TD", "QtD", "QuiD", "HxD", "SpD", "OcD", "ND", "V", "UnV", "DV", "TV", "QuaV", "QuiV", "HxV", "SpV", "OcV", "NV"][magnitude])
