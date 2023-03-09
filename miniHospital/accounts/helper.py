from django.conf import settings
from twilio.rest import Client


class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_via_message(self):     
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        print(client)

        message = client.messages.create(
                messaging_service_sid=settings.MESSAGING_SERVICE_SID,
                body=f'your otp for the login is :{self.otp}',
                to='+918139835592'
            )
