import {
  useDefaultResetPassword,
  useResetPassword,
  useResetTokenChecker,
} from "../hooks/useResetPassword";
import "../styles/resetpassword.scss";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";

function ResetPasswordDefaultPage() {
  const [email, setEmail] = useState("");
  const { resetPassword, isLoading } = useDefaultResetPassword();

  return (
    <div id="reset-password-container">
      <h1>Reset Password</h1>
      <form
        id="reset-password-form"
        onSubmit={(e) => {
          e.preventDefault();
          resetPassword(email);
        }}
      >
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {isLoading ? (
          <button disabled>Sending...</button>
        ) : (
          <button type="submit">Send Email</button>
        )}
      </form>
    </div>
  );
}

function ChangePasswordPage({ token }: { token: string }) {
  const { changePassword, isLoading } = useResetPassword();
  const [password, setPassword] = useState("");
  const [cpassword, setCPassword] = useState("");

  return (
    <div id="reset-password-container">
      <h1>Reset Password</h1>
      <form
        id="reset-password-form"
        onSubmit={(e) => {
          e.preventDefault();
          changePassword(token, password, cpassword);
        }}
      >
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          name="cpassword"
          placeholder="Confirm Password"
          value={cpassword}
          onChange={(e) => setCPassword(e.target.value)}
          required
        />
        {isLoading ? (
          <button disabled>Updating...</button>
        ) : (
          <button type="submit">Update Password</button>
        )}
      </form>
    </div>
  );
}

function ResetPassword() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [token, setToken] = useState<string | null>(null);
  const { checkResetToken, isValid } = useResetTokenChecker();

  const isExecuted = useRef(false);
  useEffect(() => {
    setToken(searchParams.get("token"));
    if (token) {
      checkResetToken(token);
    }
    setSearchParams({}, { replace: true });
    isExecuted.current = true;
  }, [token]);

  return (
    <>
      {/* Since the query parameters are cleared, so we need to explicitely tell that token doesn't have null data */}
      {isValid ? (
        <ChangePasswordPage token={token!} />
      ) : (
        <ResetPasswordDefaultPage />
      )}
    </>
  );
}

export default ResetPassword;
