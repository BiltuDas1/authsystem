import "../styles/register.scss";
import { useState } from "react";
import { useRegister } from "../hooks/useRegister";

function Register() {
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cpassword, setCPassword] = useState("");

  const { register, isLoading } = useRegister();

  return (
    <div id="register-container">
      <h1>Register</h1>
      <form
        id="register-form"
        onSubmit={(e) => {
          e.preventDefault();
          register(firstname, lastname, email, password, cpassword);
        }}
      >
        <input
          type="text"
          name="firstname"
          placeholder="First Name"
          value={firstname}
          onChange={(e) => setFirstname(e.target.value)}
          required
        />
        <input
          type="text"
          name="lastname"
          placeholder="Last Name"
          value={lastname}
          onChange={(e) => setLastname(e.target.value)}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
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
          <button disabled>Registering...</button>
        ) : (
          <button type="submit">Register</button>
        )}
      </form>
    </div>
  );
}

export default Register;
