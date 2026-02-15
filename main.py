"""
📱 BOT TELEGRAM - Alertes TradingView
Optimisé pour Render.com (Gratuit)
"""

from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# ═════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ═════════════════════════════════════════════════════════════════════════
# FONCTION D'ENVOI TELEGRAM
# ═════════════════════════════════════════════════════════════════════════

def send_telegram_message(message):
    """Envoie un message sur Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Message envoyé sur Telegram")
            return True
        else:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Erreur Telegram: {response.text}")
            return False
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Erreur: {e}")
        return False

# ═════════════════════════════════════════════════════════════════════════
# ROUTE WEBHOOK
# ═════════════════════════════════════════════════════════════════════════

@app.route('/webhook', methods=['POST'])
def webhook():
    """Reçoit les webhooks de TradingView"""
    
    try:
        data = request.get_json()
        print(f"📩 [{datetime.now().strftime('%H:%M:%S')}] Webhook reçu: {data}")
        
        if isinstance(data, dict):
            signal = data.get('signal', 'N/A')
            symbol = data.get('symbol', 'N/A')
            price = data.get('price', 'N/A')
            score = data.get('score', 'N/A')
            sl = data.get('sl', 'N/A')
            tp1 = data.get('tp1', 'N/A')
            tp2 = data.get('tp2', 'N/A')
            structure = data.get('structure', 'N/A')
            timeframe = data.get('timeframe', 'N/A')
        else:
            return "OK", 200
        
        # Message Telegram
        if signal == "LONG":
            emoji = "🟢"
        elif signal == "SHORT":
            emoji = "🔴"
        else:
            emoji = "⚪"
        
        message = f"""
{emoji} <b>SIGNAL {signal}</b> - {symbol}

📊 <b>Timeframe:</b> {timeframe}
💰 <b>Prix:</b> {price}
📈 <b>Score:</b> {score}%

🎯 <b>Structure:</b> {structure}

🛡️ <b>Stop Loss:</b> {sl}
🎯 <b>TP1:</b> {tp1}
🎯 <b>TP2:</b> {tp2}

⏰ {datetime.now().strftime('%H:%M:%S')}
        """
        
        send_telegram_message(message.strip())
        return "OK", 200
        
    except Exception as e:
        print(f"❌ Erreur webhook: {e}")
        return "ERROR", 500

# ═════════════════════════════════════════════════════════════════════════
# ROUTE HOME (Page de test)
# ═════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    """Page d'accueil"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Telegram Alertes TradingView</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #2ecc71;
                margin-bottom: 10px;
                font-size: 32px;
            }}
            .status {{
                background: #f0f9ff;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #3b82f6;
            }}
            .info {{
                background: #fefce8;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #eab308;
            }}
            code {{
                background: #f1f5f9;
                padding: 4px 8px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #dc2626;
                display: block;
                margin: 10px 0;
                word-break: break-all;
            }}
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                border-radius: 10px;
                cursor: pointer;
                transition: transform 0.2s;
                font-weight: 600;
            }}
            button:hover {{
                transform: translateY(-2px);
            }}
            button:active {{
                transform: translateY(0);
            }}
            #result {{
                margin-top: 15px;
                padding: 15px;
                border-radius: 10px;
                display: none;
            }}
            .success {{ background: #dcfce7; color: #166534; display: block; }}
            .error {{ background: #fee2e2; color: #991b1b; display: block; }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e5e7eb;
                color: #6b7280;
                font-size: 14px;
            }}
            .emoji {{ font-size: 24px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span class="emoji">✅</span> Bot Actif !</h1>
            <p style="color: #6b7280; margin-bottom: 20px;">Hébergé sur Render.com</p>
            
            <div class="status">
                <strong>📡 Statut :</strong> En ligne et prêt à recevoir des alertes
            </div>
            
            <div class="info">
                <strong>📝 URL Webhook :</strong>
                <code id="webhook-url"></code>
                <small style="color: #6b7280; display: block; margin-top: 8px;">
                    Utilisez cette URL dans vos alertes TradingView
                </small>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <button onclick="testWebhook()">
                    <span class="emoji">🧪</span> Envoyer Test sur Telegram
                </button>
                <div id="result"></div>
            </div>
            
            <div class="footer">
                <strong>ℹ️ Comment utiliser :</strong>
                <ol style="margin: 10px 0; padding-left: 20px; color: #6b7280;">
                    <li>Copiez l'URL webhook ci-dessus</li>
                    <li>Dans TradingView, créez une alerte</li>
                    <li>Collez l'URL dans "Webhook URL"</li>
                    <li>Recevez les alertes sur Telegram !</li>
                </ol>
            </div>
        </div>
        
        <script>
            document.getElementById('webhook-url').textContent = window.location.origin + '/webhook';
            
            function testWebhook() {{
                const button = document.querySelector('button');
                const result = document.getElementById('result');
                
                button.disabled = true;
                button.textContent = '⏳ Envoi en cours...';
                result.style.display = 'none';
                
                fetch('/webhook', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        signal: "LONG",
                        symbol: "BTCUSDT",
                        price: "43250",
                        score: "85",
                        sl: "42800",
                        tp1: "44000",
                        tp2: "44500",
                        structure: "BOS Bull",
                        timeframe: "1H"
                    }})
                }})
                .then(response => {{
                    if(response.ok) {{
                        result.className = 'success';
                        result.innerHTML = '✅ <strong>Test envoyé !</strong> Vérifiez votre Telegram.';
                    }} else {{
                        result.className = 'error';
                        result.innerHTML = '❌ <strong>Erreur.</strong> Vérifiez vos variables d\'environnement.';
                    }}
                    result.style.display = 'block';
                }})
                .catch(error => {{
                    result.className = 'error';
                    result.innerHTML = '❌ <strong>Erreur réseau.</strong> ' + error.message;
                    result.style.display = 'block';
                }})
                .finally(() => {{
                    button.disabled = false;
                    button.innerHTML = '<span class="emoji">🧪</span> Envoyer Test sur Telegram';
                }});
            }}
        </script>
    </body>
    </html>
    """

# ═════════════════════════════════════════════════════════════════════════
# ROUTE HEALTH CHECK (pour Render)
# ═════════════════════════════════════════════════════════════════════════

@app.route('/health')
def health():
    """Health check pour Render.com"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}, 200

# ═════════════════════════════════════════════════════════════════════════
# DÉMARRAGE
# ═════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Bot Telegram démarré sur Render.com")
    print("=" * 50)
    print(f"📱 Bot Token: {TELEGRAM_BOT_TOKEN[:10] if TELEGRAM_BOT_TOKEN else 'NON DÉFINI'}...")
    print(f"👤 Chat ID: {TELEGRAM_CHAT_ID if TELEGRAM_CHAT_ID else 'NON DÉFINI'}")
    print(f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
