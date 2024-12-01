
# Messenger App

## 📍 Overview

The Messenger App is a Flask-based web application that allows users to view and manage SMS messages, chat messages, call logs, and installed applications from a SQLite database. The application provides a clean and responsive user interface with essential functionalities to navigate conversations, view call details, and check installed apps.

---

## 👾 Features

- **View Messages**: Access SMS and ChatMessages from the database.
- **Track Calls**: Display logs including call type, contact info, time, duration, and location.
- **Installed Applications**: List applications with their installation dates.
- **Responsive Design**: Mobile-friendly interface adapting to various screen sizes.
- **Dynamic Data Rendering**: Uses Flask and Jinja2 for rendering database content dynamically.

---

## 📁 Project Structure

```plaintext
/Messenger-App
├── app.py
├── main.py
├── data.db
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── apps.html
│   ├── calls.html
│   ├── conversation.html
├── static/
│   ├── styles.css
│   └── scripts.js
└── replit.nix
```

---

### File Descriptions and Full Code

#### **`app.py`**
```python
from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT sender, MAX(time) AS latest_time FROM ChatMessages GROUP BY sender ORDER BY latest_time DESC;")
    senders = cur.fetchall()
    return render_template("index.html", senders=senders)

@app.route("/conversation/<sender>")
def conversation(sender):
    cur = get_db().cursor()
    cur.execute("SELECT time, text FROM ChatMessages WHERE sender=? ORDER BY time ASC;", (sender,))
    messages = cur.fetchall()
    return render_template("conversation.html", messages=messages, sender=sender)

@app.route("/calls")
def calls():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM Calls ORDER BY time DESC;")
    call_logs = cur.fetchall()
    return render_template("calls.html", calls=call_logs)

@app.route("/apps")
def apps():
    cur = get_db().cursor()
    cur.execute("SELECT application_name, install_date FROM InstalledApps ORDER BY install_date DESC;")
    apps_list = cur.fetchall()
    return render_template("apps.html", apps=apps_list)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
```

---

#### **`main.py`**
```python
import sqlite3

def fetch_query(query, params=()):
    try:
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        print("Error in Queries:", e)
        return None

if __name__ == "__main__":
    results = fetch_query("SELECT * FROM ChatMessages LIMIT 5;")
    for row in results:
        print(row)
```

---

#### **HTML Files (in `templates/`)**

**`layout.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Messenger App</title>
    <link rel="stylesheet" href="/static/styles.css">
    <script src="/static/scripts.js"></script>
</head>
<body>
    <header>
        <h1>Messenger App</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**`index.html`**
```html
{% extends "layout.html" %}

{% block content %}
<h2>Senders</h2>
<ul>
    {% for sender in senders %}
    <li><a href="/conversation/{{ sender[0] }}">{{ sender[0] }}</a> (Last message: {{ sender[1] }})</li>
    {% endfor %}
</ul>
{% endblock %}
```

**`conversation.html`**
```html
{% extends "layout.html" %}

{% block content %}
<h2>Conversation with {{ sender }}</h2>
<ul>
    {% for message in messages %}
    <li><strong>{{ message[0] }}</strong>: {{ message[1] }}</li>
    {% endfor %}
</ul>
<a href="/">Back to Senders</a>
{% endblock %}
```

**`calls.html`**
```html
{% extends "layout.html" %}

{% block content %}
<h2>Call Logs</h2>
<table>
    <tr>
        <th>Type</th>
        <th>From/To</th>
        <th>Time</th>
        <th>Duration</th>
        <th>Location</th>
    </tr>
    {% for call in calls %}
    <tr>
        <td>{{ call[1] }}</td>
        <td>{{ call[2] }}</td>
        <td>{{ call[3] }}</td>
        <td>{{ call[4] }}</td>
        <td>{{ call[5] }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```

**`apps.html`**
```html
{% extends "layout.html" %}

{% block content %}
<h2>Installed Applications</h2>
<table>
    <tr>
        <th>Application</th>
        <th>Install Date</th>
    </tr>
    {% for app in apps %}
    <tr>
        <td>{{ app[0] }}</td>
        <td>{{ app[1] }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```

---

#### **CSS File (`static/styles.css`)**
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f9;
}

header {
    background-color: #007bff;
    color: white;
    padding: 1rem;
    text-align: center;
}

main {
    margin: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1, h2 {
    margin-bottom: 0.5rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 0.5rem;
    text-align: left;
}

ul {
    list-style-type: none;
    padding: 0;
}

ul li {
    margin: 0.5rem 0;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

---

#### **JavaScript File (`static/scripts.js`)**
```javascript
document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded successfully!");
});
```

