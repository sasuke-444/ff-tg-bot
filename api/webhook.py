from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
BOT_TOKEN = "8058158982:AAF-Gt-iIjbLKaqkW-7F4Q3hdE0tz3geEng"
LIKE_API = "https://free-fire-like-api-theta-azure.vercel.app"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

@app.route('/api/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'GET':
        return "Bot Running!"
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"ok": True})
    message = data['message']
    chat_id = message['chat']['id']
    text = message.get('text','')
    if text.startswith('/start'):
        send_message(chat_id, "🔥 *Free Fire 200 Likes Bot* 🔥\n\nUse:\n`/like <uid> <server>`\n\nExample:\n`/like 123456789 bd`\n\nServers: bd, ind, sg, br, me, pk")
    elif text.startswith('/like'):
        try:
            parts = text.split()
            if len(parts) < 2:
                send_message(chat_id, "❌ Use: `/like 123456789 bd`")
                return jsonify({"ok": True})
            uid = parts[1]
            server = parts[2] if len(parts) > 2 else "bd"
            send_message(chat_id, f"⏳ Sending 200 Likes to `{uid}` ({server})...")
            r = requests.get(f"{LIKE_API}/like", params={"uid": uid, "server_name": server}, timeout=30)
            result = r.json()
            if r.status_code == 200:
                send_message(chat_id, f"✅ *Success!*\nUID: `{uid}`\nServer: {server}\n\n🔥 Likes Sent!")
            else:
                send_message(chat_id, f"❌ Failed: {result}")
        except Exception as e:
            send_message(chat_id, f"❌ Error: {str(e)}")
    else:
        send_message(chat_id, "Use `/like <uid> <server>`")
    return jsonify({"ok": True})

@app.route('/', methods=['GET'])
def home():
    return "Telegram Like Bot Running!"
