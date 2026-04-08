import { useState } from "react";
import { api } from "../services/api";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    try {
      const data = await api.login(form.username, form.password);
      localStorage.setItem("token", data.access_token);
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Login — POST /auth/login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username: </label>
          <input
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {result && (
        <div>
          <p style={{ color: "green" }}>
            Logged in. Token stored in localStorage.
          </p>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
