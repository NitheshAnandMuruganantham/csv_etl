import sib_api_v3_sdk
from bootstrap_config import app_config
import traceback


class MailService():

    def send(self, to, name, subject, content, template_id):
        configuration = sib_api_v3_sdk.Configuration()

        configuration.api_key['api-key'] = app_config["SENDINBLUE_API_KEY"]

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        sender = {"name": "nithesh anand", "email": "anand@infraweigh.co"}

        to = [{"email": to, "name": name}]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, template_id=template_id,
            sender=sender, subject=subject, params=content)

        return api_instance.send_transac_email(send_smtp_email)

    def send_password_reset(self, to, token):
        self.send(to, "Password Reset",
                  "Click on the link to reset your password: http://localhost:3000/reset-password?token=" + token)

    def send_invite(self, to, token):
        print("Sending invite to " + to)
        self.send(to, "Invite To Join Infraweigh Network",
                  "Click on the link to accept your invite: http://localhost:3000/invite?token=" + token + "&email=" + to)

    def send_customer_invoice(self, customer, data):
        if data["invoice"]["type"] == 1:
            net_weight = abs(data["invoice"]["scale_weight"] -
                             data["invoice"]["tare_weight"])
        else:
            net_weight = data["invoice"]["scale_weight"]
        self.send(customer["email"], customer["name"], "Weighbridge Slip Generated", {
            "Weighbridge_name": data["weighbridge"]["name"],
            "vehicle_number": data["invoice"]["vehicle_number"],
            "address": data["weighbridge"]["profile_data"].get("address"),
            "date": data["invoice"]["created_at"].strftime("%d/%m/%Y %H:%M:%S"),
            "material": data["material"]["name"],
            "vehicle": data["vehicle"]["name"],
            "scale_weight": data["invoice"]["scale_weight"],
            "tare_weight": data["invoice"]["tare_weight"],
            "net_weight": net_weight,
            "charges": data["invoice"]["charges"],
        }, 2)

    def send_invoice(self, invoice):
        if (invoice["customer_1"]):
            try:
                self.send_customer_invoice(invoice["customer_1"], invoice)
            except Exception as e:
                traceback.print_exc()
        if (invoice["customer_2"]):
            try:
                self.send_customer_invoice(invoice["customer_2"], invoice)
            except Exception as e:
                traceback.print_exc()
        if (invoice["customer_2"]):
            try:
                self.send_customer_invoice(invoice["customer_3"], invoice),
            except Exception as e:
                traceback.print_exc()
        return True
