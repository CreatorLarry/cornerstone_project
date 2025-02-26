from twilio.rest import Client
from django.conf import settings

def send_sms(recipient_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=recipient_number
    )
    return message.sid
