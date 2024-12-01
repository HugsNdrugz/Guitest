from flask import Flask, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data.db')

# Helper: Fetch data from database
def fetch_query(query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    results = cursor.execute(query, params).fetchall()
    conn.close()
    return results

# Helper: Format timestamps
def format_datetime(timestamp):
    try:
        dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt_object.strftime("%b %d, %I:%M %p")
    except (ValueError, TypeError):
        return str(timestamp)

# Route: Conversations List
@app.route('/')
def conversations():
    query = """
        SELECT sender, MAX(time) as last_message_time
        FROM (
            SELECT sender, time FROM ChatMessages
            UNION ALL
            SELECT sms_type as sender, time FROM SMS
        )
        GROUP BY sender
        ORDER BY last_message_time DESC
    """
    conversations = fetch_query(query)
    formatted_conversations = [
        {"sender": sender, "last_message_time": format_datetime(last_message_time)}
        for sender, last_message_time in conversations
    ]
    return render_template('conversations.html', conversations=formatted_conversations)

# Route: Single Conversation
@app.route('/conversation/<sender>')
def conversation(sender):
    query = """
        SELECT type, text, time
        FROM (
            SELECT 'SMS' as type, text, time FROM SMS WHERE sms_type = ?
            UNION ALL
            SELECT 'Chat' as type, text, time FROM ChatMessages WHERE sender = ?
        )
        ORDER BY time ASC
    """
    messages = fetch_query(query, (sender, sender))
    formatted_messages = [
        {"type": msg_type, "text": text, "time": format_datetime(time)}
        for msg_type, text, time in messages
    ]
    return render_template('conversation.html', sender=sender, messages=formatted_messages)

# Route: Calls View
@app.route('/calls')
def calls():
    query = "SELECT call_type, from_to, time, duration FROM Calls ORDER BY time DESC"
    calls = fetch_query(query)
    formatted_calls = [
        {"type": call_type, "from_to": from_to, "time": format_datetime(time), "duration": duration}
        for call_type, from_to, time, duration in calls
    ]
    return render_template('calls.html', calls=formatted_calls)

# Route: Apps View
@app.route('/apps')
def apps():
    query = "SELECT application_name, install_date FROM InstalledApps ORDER BY install_date DESC"
    apps = fetch_query(query)
    formatted_apps = [
        {"name": app_name, "date": format_datetime(install_date)}
        for app_name, install_date in apps
    ]
    return render_template('apps.html', apps=formatted_apps)

if __name__ == '__main__':
    app.run(debug=True)