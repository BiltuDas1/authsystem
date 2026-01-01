import { useState } from "react";
import axios, { AxiosError } from "axios";
import Cookies from "js-cookie";
import type { SuccessResponse, FailedResponse } from "../types/login.types";
import { toast } from "react-toastify";

export function useLogin() {
  const [isLoading, setIsLoading] = useState(false);

  async function login(email: string, password: string) {
    setIsLoading(true);
    axios
      .post("http://localhost:8000/api/v1/login/", {
        email: email,
        password: password,
      })
      .then((response) => {
        const data = response.data as SuccessResponse;
        Cookies.set("id", data.user.id);
        Cookies.set("access_token", data.access_token);
        Cookies.set("refresh_token", data.refresh_token);
        setIsLoading(false);
        toast.success("Login Successful");
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

  return { login, isLoading };
}
