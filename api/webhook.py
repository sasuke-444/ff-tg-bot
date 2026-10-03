from flask import Flask, request
import requests, os

app = Flask(__name__)
BOT_TOKEN = "8058158982:AAF-Gt-iIjbLKaqkW-7F4Q3hdE0tz3geEng"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Your Like API - you can add more APIs here
LIKE_APIS = [
    "https://ff-like-api.vercel.app/like?uid={uid}&server={server}",
    "https://free-fire-like-api.vercel.app/like?uid={uid}&server={server}",
]

def send_msg(chat_id, text):
    try:
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except: pass

@app.route("/")
def home():
    return "Bot Running!"

@app.route("/api/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return "Bot Running!"
    
    data = request.get_json(force=True, silent=True)
    if not data: return "ok"
    
    msg = data.get("message") or data.get("edited_message")
    if not msg: return "ok"
    
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "").strip()
    
    if not text: return "ok"
    
    low = text.lower()
    
    if low.startswith("/start"):
        send_msg(chat_id, "🔥 FF Like Bot LIVE 24/7!\n\nCommands:\n/like <UID> ind - Indian server\n/like <UID> bd - BD server\n/like <UID> sg - SG server\n\nExample:\n/like 6832457437 ind\n\nOwner: @sasuke_444")
        return "ok"
    
    if low.startswith("/like"):
        parts = text.split()
        # Support: /like 6832457437 ind  OR /like ind 6832457437
        uid = None
        server = "ind"
        
        for p in parts[1:]:
            if p.isdigit() and len(p) >= 6:
                uid = p
            elif p.lower() in ["ind","bd","sg","br","id","vn","th","me","pk","us"]:
                server = p.lower()
        
        if not uid:
            send_msg(chat_id, "❌ Wrong format!\nUse: /like <UID> <server>\nExample: /like 6832457437 ind")
            return "ok"
        
        send_msg(chat_id, f"⏳ Sending likes to {uid} ({server.upper()})... Please wait 10 sec...")
        
        success = False
        for api_template in LIKE_APIS:
            try:
                url = api_template.format(uid=uid, server=server)
                r = requests.get(url, timeout=15)
                j = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
                if r.status_code == 200 and ("success" in str(r.text).lower() or "like" in str(r.text).lower() or j.get("likes") or j.get("status") == "success"):
                    success = True
                    send_msg(chat_id, f"✅ Success! Likes sent to {uid}!\nServer: {server.upper()}\n\nCheck in game now! ❤️")
                    break
            except Exception as e:
                continue
        
        if not success:
            send_msg(chat_id, f"❌ All APIs down or UID {uid} reached daily limit. Try tomorrow morning 6 AM IST — that's when limit resets.")
        
        return "ok"
    
    return "ok"

# For Vercel
# app = app
