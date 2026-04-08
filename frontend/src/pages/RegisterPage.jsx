import { useState } from "react";
import { api } from "../services/api";

const ROLES = ["CUSTOMER", "ADMIN", "DELIVERY_DRIVER", "RESTAURANT_OWNER"];

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    phone: "",
    role: "CUSTOMER",
    location: "",
    postal_code: "",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function set(field) {
    return (e) => setForm({ ...form, [field]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    try {
      const data = await api.register(form);
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Register — POST /auth/register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username: </label>
          <input value={form.username} onChange={set("username")} />
        </div>
        <div>
          <label>Email: </label>
          <input value={form.email} onChange={set("email")} />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={form.password}
            onChange={set("password")}
          />
        </div>
        <div>
          <label>Phone: </label>
          <input value={form.phone} onChange={set("phone")} />
        </div>
        <div>
          <label>Role: </label>
          <select value={form.role} onChange={set("role")}>
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Location: </label>
          <input value={form.location} onChange={set("location")} />
        </div>
        <div>
          <label>Postal Code: </label>
          <input value={form.postal_code} onChange={set("postal_code")} />
        </div>
        <button type="submit">Register</button>
      </form>
      {result && (
        <pre style={{ color: "green" }}>{JSON.stringify(result, null, 2)}</pre>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
