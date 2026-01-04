import { useState, useEffect, useRef } from "react";
import "../styles/login.scss";
import { useLogin } from "../hooks/useLogin";
import { useEmailVerify } from "../hooks/useEmailVerify";
import { useSearchParams, useNavigate } from "react-router-dom";

function Login() {
  const { login, isLoading } = useLogin();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const source = searchParams.get("source");
  const { email_verify } = useEmailVerify();
  const navigate = useNavigate();

  const isExecuted = useRef(false);

  useEffect(() => {
    if (source == "verify-email" && !isExecuted.current) {
      email_verify(token);
      isExecuted.current = true;
    }
    navigate("/auth/login");
  }, [source, token]);

  return (
    <div id="login-container">
      <h1>Log in</h1>
      <form
        id="login-form"
        onSubmit={(e) => {
          e.preventDefault();
          login(email, password);
        }}
      >
        <input
          id="email"
          type="email"
          name="email"
          value={email}
          placeholder="Email"
          onChange={(e) => {
            setEmail(e.target.value);
          }}
          required
        />
        <input
          id="password"
          type="password"
          name="password"
          value={password}
          placeholder="Password"
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          required
        />
        {isLoading ? (
          <button disabled>Logging in...</button>
        ) : (
          <button type="submit">Log in</button>
        )}
      </form>
      <br />
      <a href="reset-password">Forget Password?</a>
    </div>
  );
}

export default Login;
