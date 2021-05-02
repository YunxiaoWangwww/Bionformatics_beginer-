mport os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    table = db.execute("SELECT * FROM stocks WHERE user_id = :id ORDER BY total_shares", id = session["user_id"])
    names = []
    shares2 = []
    price1 = []
    cash_balances = []
    total_share = []
    grand_totals = []
    length = len(table)
    if length != 0:
        for row in table:
            name = row["stock_name"]
            names.append(name)
            shares = row["total_shares"]
            shares2.append(shares)
            price = lookup(row["stock_symbol"])
            price = int(price["price"])
            price1.append(price)
            cash_balance = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
            cash_balance = int(cash_balance[0]['cash'])
            cash_balances.append(cash_balance)
            total_share_price = price*shares
            total_share.append(total_share_price)
            grand_total = total_share_price+cash_balance
            grand_totals.append(grand_total)
        return render_template("index.html", length = length, name = names, shares = shares2, price = price1, total_share_price=total_share, cash_balance = cash_balances, grand_total=grand_totals)
    else:
        cash_balance = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        cash_balance = int(cash_balance[0]['cash'])
        return render_template("index2.html", cash_balance = cash_balance)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        share = int(request.form.get("share"))
        stock = lookup(symbol)
        if not symbol or stock == None:
            return apology("Stock symbol does not exist", 403)
        elif share <= 0:
            return apology("Number of shares need to be greater than 0", 403)
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id =session["user_id"])
            cash = cash[0]['cash']
            cash_now = cash - share*int(stock["price"])
            if cash_now <= 0:
                return apology("Not enough money", 403)
            else:
                db.execute("UPDATE users SET cash = :cash_now WHERE id = :id", id = session["user_id"], cash_now = cash_now)
                db.execute("INSERT INTO transactions(user_id, cash_before, stock, stock_price, shares, cash_left,mode, time) VALUES (:id,:cash, :stock,:stock_price, :share, :cash_now, :mode, :time)", id = session["user_id"],
                    cash = cash, stock = stock["name"],stock_price = stock["price"], share = share, cash_now = cash_now, mode = "Bought", time = datetime.now())
                rows = db.execute("SELECT * FROM stocks WHERE stock_name == :stock", stock = stock['name'])
                if len(rows) == 0:
                    db.execute("INSERT INTO stocks(user_id, stock_name, stock_symbol, stock_price, total_shares) VALUES (:id, :stock, :symbol, :price,:shares)", id = session["user_id"], stock = stock["name"], symbol = symbol,  price = stock["price"], shares = share)
                elif len(rows) == 1:
                    total_shares = db.execute("SELECT total_shares FROM stocks WHERE stock_name == :stock", stock = stock['name'])
                    total_shares = total_shares[0]['total_shares']
                    db.execute("UPDATE stocks SET total_shares = ?", total_shares + share)
                    index()
                return redirect("/")


@app.route("/transaction", methods = ["GET", "POST"])
@login_required
def transaction():
    if request.method == "GET":
        return render_template("transaction.html")
    else:
        cash = int(request.form.get("cash"))
        if not cash or cash <=0:
            return apology("Cash amount is incorrect", 403)
        else:
            cash_before = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
            cash_before = cash_before[0]['cash']
            db.execute("UPDATE users SET cash = :cash_after WHERE id = :id", cash_after = cash + cash_before, id = session["user_id"])
            db.execute("INSERT INTO transactions(user_id, cash_before, stock, stock_price, shares, cash_left, mode, time) VALUES (:id,:cash, :stock,:stock_price, :share, :cash_present, :mode, :time)", id = session["user_id"],cash = cash_before, stock = "-",
                stock_price = cash, share = "-", cash_present = cash + cash_before, mode = "Transfer", time = datetime.now())
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")
    else:
        symbol = request.form.get("symbol")
        share = int(request.form.get("share"))
        stock = lookup(symbol)
        shares = db.execute("SELECT total_shares FROM stocks WHERE user_id = :id AND stock_symbol = :symbol", id = session["user_id"], symbol = symbol)
        if not symbol or stock == None:
            return apology("Stock symbol does not exist", 403)
        elif share <= 0:
            return apology("Number of shares need to be greater than 0", 403)
        elif len(shares) == 0:
            return apology("You do not have any shares", 403)
        else:
            shares = shares[0]['total_shares']
            if (shares < share):
                return apology("Shares trying to sell exceed shares held")
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id =session["user_id"])
            cash = cash[0]['cash']
            cash_present = share*int(stock["price"]) + cash
            db.execute("UPDATE users SET cash = :cash_present WHERE id = :id", id = session["user_id"], cash_present = cash_present)
            db.execute("INSERT INTO transactions(user_id, cash_before, stock, stock_price, shares, cash_left, mode, time) VALUES (:id,:cash, :stock,:stock_price, :share, :cash_present, :mode, :time)", id = session["user_id"],
                cash = cash, stock = stock["name"],stock_price = stock["price"], share = share, cash_present = cash_present, mode = "Sold", time = datetime.now())
            rows = db.execute("SELECT * FROM stocks WHERE stock_name == :stock", stock = stock['name'])
            if len(rows) == 1:
                share_now = shares - share
                if share_now > 0:
                    db.execute("UPDATE stocks SET total_shares = ?", share_now)
                elif share_now == 0:
                    db.execute("DELETE FROM stocks WHERE stock_name= :stock_name", stock_name = stock['name'])
            return redirect("/")


@app.route("/history")
@login_required
def history():
    table = db.execute("SELECT * FROM transactions WHERE user_id = :id ORDER BY time DESC", id = session["user_id"])
    names = []
    shares1 =[]
    prices = []
    cashes_before = []
    cashes_left = []
    modes = []
    times=[]
    length = len(table)
    if length != 0:
        for row in table:
            name = row["stock"]
            names.append(name)
            shares = row["shares"]
            shares1.append(shares)
            price = row["stock_price"]
            prices.append(price)
            cash_before = row["cash_before"]
            cashes_before.append(cash_before)
            cash_left = row["cash_left"]
            cashes_left.append(cash_left)
            mode = row["mode"]
            modes.append(mode)
            time = row["time"]
            times.append(time)
        return render_template("history.html", length = length, name = names, shares = shares1, price = prices, cash_before = cashes_before, cash_left = cashes_left,
            mode = modes, time = times)
    else:
        return render_template("no_history.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/password", methods = ["GET", "POST"])
def password():
    if request.method == "GET":
        return render_template("password.html")
    else:
        username = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_password = generate_password_hash(new_password)
        alert = False
        user = db.execute("SELECT * FROM users WHERE username = :username", username = username)
        if len(user) == 0 or not username:
            return apology("No such user", 403)
        elif not old_password or not new_password:
            return apology("Password inputs/input are/is empty", 403)
        elif len(user) == 1:
            password = db.execute("SELECT hash FROM users WHERE username = :username", username = username)
            password = password[0]['hash']
            if check_password_hash(password,old_password):
                alert == True
                db.execute("UPDATE users SET hash = ? WHERE username = username", new_password)
            else:
                return apology("Old password does not match the record", 403)
        return render_template("login.html", alert=alert)




@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock == None:
            return apology("Stock symbol does not exist", 403)
        else:
            return render_template("quoted.html", stock = stock)




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return apology("You must provide a username", 402)
        row = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(row) != 'NULL':
            return apology("Username exists", 403)
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        if len(password) < 8 or not password or not password_confirmation:
            return apology("Password must contain at least 8 characters", 403)
        elif password != password_confirmation:
            return apology("Password passed in the confirmation does not match the previous password input", 403)
        else:
            password_hashed = generate_password_hash(password)
            db.execute("INSERT INTO users(username,hash) VALUES(:username,:password_hashed)", username = username, password_hashed = password_hashed)
            return redirect("/login")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

