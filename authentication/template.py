from pathlib import Path
import os

TEMPLATE_DIR = os.path.join(
  Path(__file__).resolve().parent,
  "html"
)

def seconds_to_readable(seconds: int) -> str:
  units = {
    "day": 60*60*24,
    "hour": 60*60,
    "minute": 60
  }
  for unit, value in units.items():
    units[unit], seconds = divmod(seconds, value)

  result = []
  for unit, value in units.items():
    if value == 0:
      continue
    if value == 1:
      result.append(f"{value} {unit}")
    else:
      result.append(f"{value} {unit + 's'}")

  if seconds != 0:
    result.append(f"{seconds} seconds")

  return " ".join(result)

# with open(os.path.join(TEMPLATE_DIR, "otp.html")) as f:
#   otp_html = f.read()

# def load_otp_template(otp: str, validity: int) -> str:
#   """
#   Loads the email template and replace OTP there and return it
#   """
#   return otp_html.format(OTP=otp, MINUTES=f"{validity//60} minutes")

with open(os.path.join(TEMPLATE_DIR, "verify_email.html")) as f:
  verify_email = f.read()

def load_email_verify(url: str, validity: int) -> str:
  """
  Loads the email template and replace the verification link
  """
  return verify_email.format(VERIFICATION_URL=url, TIME=seconds_to_readable(validity))


with open(os.path.join(TEMPLATE_DIR, "reset_password.html")) as f:
  reset_password = f.read()

def load_reset_password(url: str, validity: int) -> str:
  """
  Loads the Reset password Email template and replace the verification link
  """
  return reset_password.format(RESET_URL=url, TIME=seconds_to_readable(validity))
