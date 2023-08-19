from twilio.rest import Client
from bootstrap_config import app_config
import traceback


class SmsService:
    def __init__(self):
        self.client = Client(
            app_config["TWILIO_ACCOUNT_SID"], app_config["TWILIO_AUTH_TOKEN"])

    def message(self, to, body):
        self.client.messages.create(
            body=body,
            from_=app_config["TWILIO_PHONE_NUMBER"],
            to=to)

    def construct_bill_message(self, customer, data):
        if data["invoice"]["type"] == 1:
            net_weight = abs(data["invoice"]["scale_weight"] -
                             data["invoice"]["tare_weight"])
        else:
            net_weight = data["invoice"]["scale_weight"]

        return f"""
Dear {customer["name"]},
thank you for choosing {data["weighbridge"]["name"]}!
vehicle number: {data["invoice"]["vehicle_number"]}
date time: {data["invoice"]["created_at"].strftime("%d/%m/%Y %H:%M:%S")}
material: {data["material"]["name"]}
vehicle: {data["vehicle"]["name"]}
scale weight: {data["invoice"]["scale_weight"]}
tare weight: {data["invoice"]["tare_weight"]}
gross weight: {net_weight}
charges: {data["invoice"]["charges"]}
"""

    def send_invoice_sms(self, customer, invoice):
        if customer["phone"] is None:
            return
        message = self.construct_bill_message(customer, invoice)
        self.message(customer["phone"], message)

    def send_invoice(self, invoice):
        if (invoice["customer_1"]):
            try:
                self.send_invoice_sms(invoice["customer_1"], invoice)
            except Exception as e:
                traceback.print_exc()
        if (invoice["customer_2"]):
            try:
                self.send_invoice_sms(invoice["customer_2"], invoice)
            except Exception as e:
                traceback.print_exc()
        if (invoice["customer_2"]):
            try:
                self.send_invoice_sms(invoice["customer_3"], invoice),
            except Exception as e:
                traceback.print_exc()
        return True
