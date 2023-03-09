from django.conf import settings
from twilio.rest import Client


class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_via_message(self):     
        client= Client('AC20895086bbda77a2ae09e4e1ceb8ccec','87ee036b030b8b35fb48422adee69672')

        message = client.messages.create(
                messaging_service_sid='MG13fb9ab6a40aa9c83bfa1ccf0282b644',
                body=f'your otp for the login is :{self.otp}',
                to='+918139835592'
            )
