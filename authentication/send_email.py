import urllib3
import json
import dotenv


class Email:
  def __init__(self, api_key: str, sender_email: str, sender_name: str):
    self.__api_key = api_key
    self.__sender_email = sender_email
    self.__sender_name = sender_name
    self.__http = urllib3.PoolManager()

  def send(self, to: str, subject: str, html_body: str) -> bool:
    data = {
      "sender": {
        "name": self.__sender_name,
        "email": self.__sender_email
      },
      "to": [
        {
          "email": to
        }
      ],
      "subject": subject,
      "htmlContent": html_body
    }

    response = self.__http.request(
      method="POST", 
      url="https://api.brevo.com/v3/smtp/email",
      body=json.dumps(data).encode(),
      headers={
        "content-type": "application/json",
        "accept": "application/json",
        "api-key": self.__api_key
      }
    )
    return response.status == 201
  

config = dotenv.dotenv_values()
EMAIL = None
if config["BREVO_API_KEY"] is not None and \
   config["SENDER_EMAIL"] is not None and \
   config["SENDER_NAME"] is not None:
  EMAIL = Email(
    api_key=config["BREVO_API_KEY"],
    sender_email=config["SENDER_EMAIL"],
    sender_name=config["SENDER_NAME"]
  )