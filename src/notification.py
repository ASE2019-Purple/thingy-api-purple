# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")

client = None

async def init_twilio():
    global client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_message(content, recipient):
    message = client.messages \
                    .create(
                        body=content,
                        from_='+19382229139',
                        to=recipient
                    )
    print(message.sid)

