import { useState } from "react";
import { login, signup } from "../services/api";

function Auth({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isSignup = mode === "signup";

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = isSignup
        ? await signup(username, password)
        : await login(username, password);
      onAuthenticated(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-mark">AI</div>
        <p className="auth-eyebrow">Company workspace</p>
        <h1>{isSignup ? "Create your account" : "Welcome back"}</h1>
        <p className="auth-description">
          {isSignup
            ? "Create a secure account to access your internal assistant."
            : "Sign in to continue to your internal assistant."}
        </p>

        <form className="auth-form" onSubmit={submit}>
          <label>
            Username
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
              required
              minLength={3}
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete={isSignup ? "new-password" : "current-password"}
              required
              minLength={8}
            />
          </label>

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Please wait..." : isSignup ? "Create account" : "Sign in"}
          </button>
        </form>

        <p className="auth-switch">
          {isSignup ? "Already have an account?" : "Need an account?"}{" "}
          <button
            type="button"
            onClick={() => {
              setMode(isSignup ? "login" : "signup");
              setError("");
            }}
          >
            {isSignup ? "Sign in" : "Sign up"}
          </button>
        </p>
      </section>
    </main>
  );
}

export default Auth;