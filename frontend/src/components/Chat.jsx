import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import ChatInput from "./ChatInput";
import { sendChatMessage } from "../services/api";

function Chat({ token }) {
  const [sessionId] = useState(() => crypto.randomUUID());

  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "assistant",
      content:
        "Hello! I'm the Company AI Assistant. I can help with company policies, employees, and support tickets.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const sendMessage = async (event) => {
    event.preventDefault();

    const message = input.trim();

    if (!message || loading) {
      return;
    }

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(
        message,
        sessionId,
        token
      );

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error("Chat request failed:", error);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Sorry, I could not connect to the AI assistant. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="chat-container">
      <div className="messages">
        {messages.map((message) => (
          <Message
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        {loading && (
          <div className="message-row assistant">
            <div className="avatar assistant-avatar">
              AI
            </div>

            <div className="message-wrapper">
              <div className="message typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        input={input}
        loading={loading}
        onChange={handleInputChange}
        onSubmit={sendMessage}
      />
    </main>
  );
}

export default Chat;