import secrets

class OTP:
  def __init__(self, digits: int = 6):
    value = secrets.randbelow(10**digits)
    self.__otp = f"{value:0{digits}}"

  def __str__(self):
    return self.__otp
  
  def get(self) -> str:
    return self.__otp
