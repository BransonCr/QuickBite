import { useState } from "react";
import { api } from "../services/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [forgotResult, setForgotResult] = useState(null);
  const [forgotError, setForgotError] = useState(null);

  const [resetForm, setResetForm] = useState({ token: "", new_password: "" });
  const [resetResult, setResetResult] = useState(null);
  const [resetError, setResetError] = useState(null);

  async function handleForgot(e) {
    e.preventDefault();
    setForgotError(null);
    setForgotResult(null);
    try {
      const data = await api.forgotPassword(email);
      setForgotResult(data);
    } catch (err) {
      setForgotError(err.message);
    }
  }

  async function handleReset(e) {
    e.preventDefault();
    setResetError(null);
    setResetResult(null);
    try {
      const data = await api.resetPassword(
        resetForm.token,
        resetForm.new_password,
      );
      setResetResult(data);
    } catch (err) {
      setResetError(err.message);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Forgot Password — POST /auth/forgot-password</h2>
      <form onSubmit={handleForgot}>
        <div>
          <label>Email: </label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <button type="submit">Send Reset Token</button>
      </form>
      {forgotResult && (
        <pre style={{ color: "green" }}>
          {JSON.stringify(forgotResult, null, 2)}
        </pre>
      )}
      {forgotError && <p style={{ color: "red" }}>{forgotError}</p>}

      <hr />

      <h2>Reset Password — POST /auth/reset-password</h2>
      <form onSubmit={handleReset}>
        <div>
          <label>Token: </label>
          <input
            value={resetForm.token}
            onChange={(e) =>
              setResetForm({ ...resetForm, token: e.target.value })
            }
          />
        </div>
        <div>
          <label>New Password: </label>
          <input
            type="password"
            value={resetForm.new_password}
            onChange={(e) =>
              setResetForm({ ...resetForm, new_password: e.target.value })
            }
          />
        </div>
        <button type="submit">Reset Password</button>
      </form>
      {resetResult && (
        <pre style={{ color: "green" }}>
          {JSON.stringify(resetResult, null, 2)}
        </pre>
      )}
      {resetError && <p style={{ color: "red" }}>{resetError}</p>}
    </div>
  );
}
