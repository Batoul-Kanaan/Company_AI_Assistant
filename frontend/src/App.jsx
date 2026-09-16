import Chat from "./components/Chat";
import Auth from "./components/Auth";
import "./index.css";
import { useState } from "react";


function App() {
  const [auth, setAuth] = useState(() => {
    const stored = localStorage.getItem("company-ai-auth");
    return stored ? JSON.parse(stored) : null;
  });

  const handleAuthenticated = (data) => {
    localStorage.setItem("company-ai-auth", JSON.stringify(data));
    setAuth(data);
  };

  const logout = () => {
    localStorage.removeItem("company-ai-auth");
    setAuth(null);
  };

  if (!auth) {
    return <Auth onAuthenticated={handleAuthenticated} />;
  }

  return (
    <div className="app">
      <header className="chat-header">
        <div className="header-content">
          <div className="header-icon">
            AI
          </div>

          <div>
            <h1>Company AI Assistant</h1>
            <p>Internal company assistant</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Online
        </div>
        <button className="logout-button" type="button" onClick={logout}>
          Sign out
        </button>
      </header>

      <Chat token={auth.access_token} />
    </div>
  );
}


export default App;