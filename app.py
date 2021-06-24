from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
app.secret_key = 'HiTherePun'

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)
app.secret_key = 'HiTherePun'

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], 
                            [None, None, None],
                            [None, None, None]]
        session["turn"] = "X"
        session["win"] = None
    
    if session["win"]:
        return render_template("game.html", game=session["board"], turn=session["turn"], extra=session["win"])
    
    return render_template("game.html", game=session["board"], turn=session["turn"])

def checkwin(row,col):
    for i in range(3):
        if session["board"][row][i] != session["board"][row][col]:
            break
        if i == 2:
            return 1

    for i in range(3):
        if session["board"][i][col] != session["board"][row][col]:
            break
        if i == 2:
            return 1

    if row == col:
        for i in range(3):
            if session["board"][i][i] != session["board"][row][col]:
                break
            if i == 2:
                return 1
    
    if row + col == 2:
        for i in range(3):
            if session["board"][i][2-i] != session["board"][row][col]:
                break
            if i == 2:
                return 1

    cou = 0
    for i in range(3):
        for j in range(3):
            if session["board"][i][j] == None:
                cou += 1
    if cou == 0:
        return 0

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    ch = checkwin(row,col)
    if ch == 1:
        session["win"] = f'{session["turn"]} wins!'
    if ch == 0:
        session["win"] = "Draw!"
    if session["turn"] == 'X':
        session["turn"] = 'O'
    else:
        session["turn"] = 'X'
    
    return redirect("/")

@app.route("/botplay")
def botplay():
    if session["win"]:
        return redirect("/")
    ans = minimax(session["turn"],session["board"])
    if ans[1] is not None:
        return redirect(url_for('play', row=ans[1][0], col=ans[1][1]))

def minimax(player, board):

    possible=[]
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                possible.append((i, j))
    if not possible:
        return (0,None)
    if player == 'X':
        value = -2
        for i,j in possible:
            board[i][j] = 'X'
            ans = checkwin(i,j)
            if ans == 1:
                result = 1
            elif ans == 0:
                result = 0
            else :
                result = minimax('O', board)[0]
            if value < result:
                value = result
                step = (i,j)
            board[i][j] = None
    elif player == 'O':
        value = 2
        for i,j in possible:
            board[i][j] = 'O'
            ans = checkwin(i,j)
            if ans == 1:
                result = -1
            elif ans == 0:
                result = 0
            else :
                result = minimax('X', board)[0]
            if value > result:
                value = result
                step = (i,j)
            board[i][j] = None
            
    return (value, step)


@app.route("/clear")
def clear():
    session["board"] = [[None, None, None], 
                        [None, None, None],
                        [None, None, None]]
    session["turn"] = "X"
    session["win"] = None
    return redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run()