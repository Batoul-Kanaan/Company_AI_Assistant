function Message({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${role}`}>
      {!isUser && (
        <div className="avatar assistant-avatar">
          AI
        </div>
      )}

      <div className="message-wrapper">
        <div className="message">
          {content}
        </div>
      </div>

      {isUser && (
        <div className="avatar user-avatar">
          You
        </div>
      )}
    </div>
  );
}


export default Message;