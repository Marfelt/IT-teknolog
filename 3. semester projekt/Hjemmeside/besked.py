from twilio.rest import Client
import keys

def send_sms():
    client = Client(keys.account_sid, keys.auth_token)
    
    try:
        message = client.messages.create(
            body="Person has fallen! Check the GPS feed: http://192.168.233.219:8080",
            from_=keys.twilio_number,
            to=keys.target_number
        )
        print(message.body)
    except Exception as e:
        print(f"Error sending SMS: {e}")
