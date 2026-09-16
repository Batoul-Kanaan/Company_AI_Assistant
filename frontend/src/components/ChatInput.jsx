function ChatInput({
  input,
  loading,
  onChange,
  onSubmit,
}) {
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit(event);
    }
  };

  return (
    <form
      className="chat-input-container"
      onSubmit={onSubmit}
    >
      <textarea
        value={input}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        placeholder="Ask about company policies, employees, or tickets..."
        disabled={loading}
        rows={1}
      />

      <button
        type="submit"
        disabled={loading || !input.trim()}
        aria-label="Send message"
      >
        {loading ? "..." : "Send"}
      </button>
    </form>
  );
}


export default ChatInput;