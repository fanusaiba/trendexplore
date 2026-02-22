import { useEffect, useRef, useState } from "react";

export default function Chat() {
  const [username, setUsername] = useState("");
  const [joined, setJoined] = useState(false);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const ws = useRef(null);

  const joinChat = () => {
    if (!username.trim()) return;

    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/${username}`);

    ws.current.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      setMessages((m) => [...m, msg]);
    };

    ws.current.onclose = () => {
      console.log("WebSocket closed");
    };

    setJoined(true);
  };

  const sendMessage = () => {
    if (ws.current && text.trim() !== "") {
      ws.current.send(JSON.stringify({ action: "message", text }));
      setText("");
    }
  };

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
        console.log("WebSocket disconnected on cleanup");
      }
    };
  }, []);

  return (
    <div className="p-6">
      {!joined ? (
        <div className="flex flex-col items-center gap-3">
          <input
            type="text"
            placeholder="Enter your name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="px-4 py-2 rounded bg-white text-black placeholder-gray-500 w-64 border"
          />
          <button
            onClick={joinChat}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Join Chat
          </button>
        </div>
      ) : (
        <div className="max-w-2xl mx-auto bg-white p-4 rounded shadow">
          
          {/* Chat Messages */}
          <div className="h-80 overflow-y-auto border p-3 mb-4 text-black bg-white rounded">
            {messages.map((m, i) => (
              <div key={i} className="mb-2 text-black">
                <strong className="text-black">
                  {m.from || "Server"}:
                </strong>{" "}
                <span className="text-black">{m.text}</span>
              </div>
            ))}
          </div>

          {/* Input Section */}
          <div className="flex gap-2">
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="flex-1 border p-2 rounded text-black bg-white"
              placeholder="Type a message..."
            />
            <button
              onClick={sendMessage}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              Send
            </button>
          </div>

        </div>
      )}
    </div>
  );
}