import paypalrestsdk
from dotenv import load_dotenv
import os 

load_dotenv()
mode = os.getenv('PAYPAL_MODE')
client_id = os.getenv('PAYPAL_CLIENT_ID')
client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
paypalrestsdk.configure({
    "mode": mode,
    "client_id": client_id,
    "client_secret": client_secret,
})

print("Configured ✅")

payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {"payment_method": "paypal"},
    "transactions": [{
        "amount": {"total": "1.00", "currency": "USD"},
        "description": "Test Payment"
    }],
    "redirect_urls": {
        "return_url": "http://localhost:8000/payment/execute",
        "cancel_url": "http://localhost:8000/payment/cancel",
    },
})

if payment.create():
    print("✅ Payment created!")
else:
    print("❌ Error:", payment.error)
