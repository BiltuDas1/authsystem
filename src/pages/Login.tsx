import { useState } from "react";
import "../styles/login.scss";
import { useLogin } from "../hooks/useLogin";

function Login() {
  const { login, isLoading } = useLogin();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
    </div>
  );
}

export default Login;
