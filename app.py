import os
import re
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

@app.route("/slack/commands", methods=["POST"])
def applaud():
    user_id = request.form.get("user_id")
    text = request.form.get("text")
    response_url = request.form.get("response_url")

    # Parse command: <@USER> X message
    match = re.match(r"<@([A-Z0-9]+)>\s+(\d+)\s+(.+)", text)
    if not match:
        return "❌ Format: /applaud @user X message", 200

    to_user, points, message = match.groups()
    points = int(points)

    # TODO: implement point deduction logic here

    # Immediate response to user
    user_response = f"👏 You gave {points} points to <@{to_user}>!"
    post_message = f":clap: <@{user_id}> gave *{points}* points to <@{to_user}>:\n> {message}"

    # Post to applause-wall (replace with actual channel name or ID)
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": "#applause-information",  # <-- customize this
            "text": post_message
        }
    )

    return user_response, 200

if __name__ == "__main__":
    app.run(port=3000)
