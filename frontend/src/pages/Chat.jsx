import { useEffect, useRef, useState } from "react";

export default function Chat() {
  const [username, setUsername] = useState("");
  const [joined, setJoined] = useState(false);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const ws = useRef(null);

  const joinChat = () => {
    if (!username.trim()) return;

    // prevent double connection
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      return;
    }

    const socket = new WebSocket(`wss://trendexplore.onrender.com/ws/${username}`);
    ws.current = socket;

    socket.onopen = () => {
      console.log("WebSocket connected");
      setJoined(true);
    };

    socket.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      setMessages((prev) => {
        // stop exact duplicate messages
        const isDuplicate = prev.some(
          (m) =>
            m.type === msg.type &&
            m.username === msg.username &&
            m.text === msg.text
        );

        if (isDuplicate) return prev;
        return [...prev, msg];
      });
    };

    socket.onclose = () => {
      console.log("WebSocket closed");
    };

    socket.onerror = (err) => {
      console.log("WebSocket error:", err);
    };
  };

  const sendMessage = () => {
    if (
      ws.current &&
      ws.current.readyState === WebSocket.OPEN &&
      text.trim() !== ""
    ) {
      ws.current.send(
        JSON.stringify({
          action: "message",
          text: text.trim(),
        })
      );
      setText("");
    }
  };

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-indigo-700 p-4">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-6">
        {!joined ? (
          <div className="flex flex-col items-center gap-4">
            <h2 className="text-2xl font-bold text-gray-800">Join Global Chat</h2>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full max-w-sm px-4 py-3 border rounded-lg text-black focus:outline-none"
            />
            <button
              onClick={joinChat}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
            >
              Join Chat
            </button>
          </div>
        ) : (
          <>
            <h2 className="text-3xl font-bold text-center text-gray-800 mb-4">
              Global Chat
            </h2>

            <div className="h-96 overflow-y-auto border rounded-lg p-4 bg-gray-50 mb-4">
              {messages.length === 0 ? (
                <p className="text-gray-500">No messages yet</p>
              ) : (
                messages.map((msg, i) => (
                  <div key={i} className="mb-3 p-3 bg-white border rounded-lg">
                    <span className="font-semibold text-blue-700">
                      {msg.username || "Server"}:
                    </span>{" "}
                    <span className="text-gray-800">{msg.text}</span>
                  </div>
                ))
              )}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Type a message..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") sendMessage();
                }}
                className="flex-1 px-4 py-3 border rounded-lg text-black focus:outline-none"
              />
              <button
                onClick={sendMessage}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
              >
                Send
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}