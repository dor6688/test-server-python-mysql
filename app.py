from flask import Flask, jsonify
from mysql.connector import connect
import random

app = Flask(__name__)

# MySQL Configuration
DB_CONFIG = {
    "host": "localhost",  # Update for Render if deploying
    "user": "root",  # Replace with your MySQL username
    "password": "",  # Replace with your MySQL password
    "database": "whatsapp_message"
}


@app.route("/random-message", methods=["GET"])
def get_random_message():
    conn = None
    try:
        # Connect to the MySQL database
        conn = connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Query to get all rows from the `message` table
        cursor.execute("SELECT * FROM message")
        messages = cursor.fetchall()

        if not messages:
            return jsonify({"error": "No messages found!"}), 404

        # Select a random message
        random_message = random.choice(messages)
        return jsonify(random_message)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
