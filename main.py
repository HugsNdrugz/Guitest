import sqlite3

# Path to your SQLite database
db_path = 'data.db'

# Function to test queries
def test_queries():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Test SMS and ChatMessages query
    print("Messages Query Test:")
    try:
        query = """
            SELECT 'SMS' as type, sms_type as sender, time, text
            FROM SMS
            UNION ALL
            SELECT 'Chat' as type, sender, time, text
            FROM ChatMessages
            ORDER BY time DESC
        """
        messages = cursor.execute(query).fetchall()
        print("Messages:", messages)
    except Exception as e:
        print("Error in Messages Query:", e)

    # Test Calls query
    print("\nCalls Query Test:")
    try:
        query = "SELECT call_type, from_to, time, duration, location FROM Calls ORDER BY time DESC"
        calls = cursor.execute(query).fetchall()
        print("Calls:", calls)
    except Exception as e:
        print("Error in Calls Query:", e)

    # Test InstalledApps query
    print("\nInstalled Apps Query Test:")
    try:
        query = "SELECT application_name, package_name, install_date FROM InstalledApps"
        apps = cursor.execute(query).fetchall()
        print("Installed Apps:", apps)
    except Exception as e:
        print("Error in Installed Apps Query:", e)

    conn.close()

test_queries()