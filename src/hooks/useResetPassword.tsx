import { useState } from "react";
import axios, { AxiosError } from "axios";
import { toast } from "react-toastify";
import type { FailedResponse } from "../types/auth.types";

export function useDefaultResetPassword() {
  const [isLoading, setIsLoading] = useState(false);

  function resetPassword(email: string) {
    setIsLoading(true);
    axios
      .post("http://localhost:8000/api/v1/email/reset-password/", {
        email: email,
      })
      .then(() => {
        setIsLoading(false);
        toast.success(`Password Reset email has been send to ${email}`);
      })
      .catch((error: AxiosError) => {
        setIsLoading(false);
        const data = error.response!.data as FailedResponse;
        if (error.status == 429) {
          toast.warning(data.reason);
        } else {
          toast.error(data.reason);
        }
      });
  }

  return { resetPassword, isLoading };
}

export function useResetPassword() {
  const [isLoading, setIsLoading] = useState(false);

  function changePassword(token: string, password: string, cpassword: string) {
    if (password != cpassword) {
      toast.error("Password and Confirm Password is not matching");
      return;
    }

    setIsLoading(true);
    axios
      .post("http://localhost:8000/api/v1/email/reset-password/change", {
        token: token,
        password: password,
      })
      .then(() => {
        setIsLoading(false);
        toast.success("Password change successfully");
      })
      .catch((error: AxiosError) => {
        setIsLoading(false);
        const data = error.response!.data as FailedResponse;
        if (error.status == 429) {
          toast.warning(data.reason);
        } else {
          toast.error(data.reason);
        }
      });
  }

  return { changePassword, isLoading };
}

export function useResetTokenChecker() {
  const [isValid, setIsValid] = useState<boolean | null>(null);

  async function checkResetToken(token: string) {
    await axios
      .get(
        `http://localhost:8000/api/v1/email/reset-password/verifyToken?token=${token}`,
      )
      .then(() => {
        setIsValid(true);
      })
      .catch((error: AxiosError) => {
        setIsValid(false);
        const data = error.response!.data as FailedResponse;
        if (error.status == 429) {
          toast.warning(data.reason);
        } else {
          toast.error("Invalid URL or URL Expired");
        }
      });
  }
  return { checkResetToken, isValid };
}
