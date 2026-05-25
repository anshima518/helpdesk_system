from flask import Flask, render_template, request,redirect,session
import pickle
import sqlite3

app = Flask(__name__)
app.secret_key = "helpdesk_secret_key"

# Load ML Model
with open("models/ticket_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


@app.route("/", methods=["GET", "POST"])


def home():
    if "user" not in session:
        return redirect("/login")

    prediction = None
    confidence = None
    priority = None
    color = "#22c55e"

    if request.method == "POST":

        ticket_text = request.form["ticket"]

        ticket_vector = vectorizer.transform(
            [ticket_text]
        )

        prediction = model.predict(
            ticket_vector
        )[0]

        # Priority Logic
        if prediction == "Infrastructure":
            priority = "High"

        elif prediction == "Network":
            priority = "High"

        elif prediction == "Hardware":
            priority = "Medium"

        elif prediction == "Software":
            priority = "Medium"

        elif prediction == "Access":
            priority = "Low"

        else:
            priority = "Low"

        # Default Status
        status = "Open"

        # Confidence Score
        if hasattr(model, "predict_proba"):

            confidence = round(
                max(
                    model.predict_proba(
                        ticket_vector
                    )[0]
                ) * 100,
                2
            )

        else:
            confidence = 0

        # Category Colors
        if prediction == "Hardware":
            color = "#f97316"

        elif prediction == "Network":
            color = "#3b82f6"

        elif prediction == "Access":
            color = "#a855f7"

        elif prediction == "Infrastructure":
            color = "#ef4444"

        elif prediction == "Software":
            color = "#22c55e"

        # Save Ticket
        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tickets
            (
                ticket_text,
                category,
                confidence,
                priority,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                ticket_text,
                prediction,
                confidence,
                priority,
                status
            )
        )

        conn.commit()
        conn.close()

    # Dashboard Stats
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tickets"
    )
    total_tickets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE category='Hardware'"
    )
    hardware_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE category='Network'"
    )
    network_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE category='Software'"
    )
    software_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        priority=priority,
        color=color,
        total_tickets=total_tickets,
        hardware_count=hardware_count,
        network_count=network_count,
        software_count=software_count
    )


@app.route("/tickets")
def tickets():

    search = request.args.get("search", "")

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    if search:

        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE ticket_text LIKE ?
               OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search}%",
                f"%{search}%"
            )
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM tickets
            ORDER BY id DESC
            """
        )

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "tickets.html",
        rows=rows,
        search=search
    )


@app.route("/analytics")
def analytics():

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM tickets
        GROUP BY category
    """)

    category_data = cursor.fetchall()

    cursor.execute("""
        SELECT priority, COUNT(*)
        FROM tickets
        GROUP BY priority
    """)

    priority_data = cursor.fetchall()

    conn.close()

    category_labels = [row[0] for row in category_data]
    category_values = [row[1] for row in category_data]

    priority_labels = [row[0] for row in priority_data]
    priority_values = [row[1] for row in priority_data]

    return render_template(
        "analytics.html",
        category_labels=category_labels,
        category_values=category_values,
        priority_labels=priority_labels,
        priority_values=priority_values
    )

@app.route("/delete/<int:id>")
def delete_ticket(id):

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tickets WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/tickets")

@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tickets
        SET status=?
        WHERE id=?
        """,
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect("/tickets")

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect("/")

        else:

            error = "Invalid Username or Password"

    return render_template(
        "login.html",
        error=error
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:

            conn = sqlite3.connect("tickets.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (?, ?)
                """,
                (username, password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except:

            error = "Username already exists"

    return render_template(
        "signup.html",
        error=error
    )


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


@app.route("/settings")
def settings():

    return render_template("settings.html")

@app.route("/accounts")
def accounts():

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return render_template(
        "accounts.html",
        users=users
    )

@app.route("/delete_account/<int:id>")
def delete_account(id):

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/accounts")


if __name__ == "__main__":
    app.run(debug=True)