export interface LoginSuccessResponse {
  result: true;
  access_token: string;
  refresh_token: string;
  user: {
    id: string;
    firstname: string;
    lastname: string;
    email: string;
    role: string;
  };
}

export interface RegisterSuccessResponse {
  result: true;
  description: string;
}

export interface FailedResponse {
  result: false;
  reason: string;
}
