import { useState } from "react";
import axios, { AxiosError } from "axios";
import type { FailedResponse } from "../types/auth.types";
import { toast } from "react-toastify";

export function useRegister() {
  const [isLoading, setIsLoading] = useState(false);

  async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
    cpassword: string,
  ) {
    if (password != cpassword) {
      toast.error("Password and Confirm Password doesn't match");
      return;
    }

    setIsLoading(true);
    axios
      .post("http://localhost:8000/api/v1/register/", {
        firstname: firstName,
        lastname: lastName,
        email: email,
        password: password,
      })
      .then(() => {
        setIsLoading(false);
        toast.success(`Verification email has been send to ${email}`);
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

  return { register, isLoading };
}
