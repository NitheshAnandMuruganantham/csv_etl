from .sms import SmsService
from .mail import MailService


class NotificationService:
    def __init__(self):
        self.message = SmsService()
        self.mail = MailService()

    def send_invoice_notification(self, invoice):
        self.message.send_invoice(invoice)
        self.mail.send_invoice(invoice)
        return True
