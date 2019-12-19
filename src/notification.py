# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")

client = None
msgs_limit = 2
msgs_sent = 0
current_date = None

async def init_twilio():
    global client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_message(content, recipient, date):
    if date == current_date:
        print("Notification already sent today")
        return

    current_date = date
    message = client.messages \
                    .create(
                        body=content,
                        from_='+19382229139',
                        to=recipient
                    )
    print(message.sid)

