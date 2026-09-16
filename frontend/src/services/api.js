const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function sendChatMessage(message, sessionId, token) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error(
      `Request failed with status ${response.status}`
    );
  }

  return response.json();
}

async function authRequest(path, username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Authentication failed.");
  }

  return data;
}

export function login(username, password) {
  return authRequest("login", username, password);
}

export function signup(username, password) {
  return authRequest("signup", username, password);
}