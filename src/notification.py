# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

account_sid = 'AC8adb6f3b3b9d5cab186fb158f6954482'
auth_token = '970f2844b96f50945e4ae377c8ed13cf'
client = Client(account_sid, auth_token)

def send_message(content, recipient):
    message = client.messages \
                    .create(
                        body=content,
                        from_='+19382229139',
                        to=recipient
                    )
    print(message.sid)

send_message("Salut mon frère\ncomment tu vas\nt'arrives au bout de ce projet ou bien", "+41792490274")