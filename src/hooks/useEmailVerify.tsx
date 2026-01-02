import { toast } from "react-toastify";
import axios from "axios";

export function useEmailVerify() {
  function email_verify(token: string | null) {
    if (token == null) {
      toast.error("Invalid URL or Link Expired");
      return;
    }

    axios
      .post("http://localhost:8000/api/v1/email/verify/", {
        token: token,
      })
      .then(() => {
        toast.success("Email verified, now you can login.");
      })
      .catch(() => {
        toast.error("Invalid URL or Link Expired");
      });
  }

  return { email_verify };
}
