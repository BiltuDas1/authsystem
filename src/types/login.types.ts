export interface SuccessResponse {
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

export interface FailedResponse {
  result: false;
  reason: string;
}
