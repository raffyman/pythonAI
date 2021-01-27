from flask import Flask, request, jsonify
from flask_cors import CORS
import aiml
import mebot

app = Flask(__name__)
CORS(app)

mebot = mebot.MeBot(user_ip="23.21.4.2")


@app.route("/", methods=["POST"])
def msg():
    msg = request.json["usr_msg"]
    reply = mebot.conversate(msg)
    print("Reply", reply)
    return reply
