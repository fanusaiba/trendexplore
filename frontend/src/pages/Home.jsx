import { useEffect, useRef, useState, useContext } from "react";
import axios from "axios";
import countries from "../data/countries";
import { AuthContext } from "../context/AuthContext";

const API_BASE = import.meta.env.VITE_API_BASE;
const WS_BASE = import.meta.env.VITE_WS_BASE;

// Always send cookies
axios.defaults.withCredentials = true;

export default function Home() {
  const { user } = useContext(AuthContext);

  const [country, setCountry] = useState("US");
  const [category, setCategory] = useState("Google");
  const [search, setSearch] = useState("");
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  const [favorites, setFavorites] = useState(
    JSON.parse(localStorage.getItem("favorites")) || []
  );

  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [chatOpen, setChatOpen] = useState(true);
  const [room, setRoom ] = useState("global");

  const chatRef = useRef(null);
  const ws = useRef(null);
  const didConnect = useRef(false);



const generatePrivateRoom = (userA, userB) => {
  return [userA, userB].sort().join("_");
};

const openPrivateChat = (otherEmail) => {
  if (!user?.email) return;

  const privateRoom = generatePrivateRoom(user.email, otherEmail);

  setRoom(privateRoom);

  if (ws.current) {
    ws.current.send(
      JSON.stringify({
        action: "join_room",
        room: privateRoom
      })
    );
  }
};
  /* ---------------------------------- */
  /* 🔥 FETCH TRENDS                    */
  /* ---------------------------------- */
  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const res = await axios.get(
          `${API_BASE}/api/trends?country=${country}&category=${category}`
        );
        setTrends(res.data.trends || []);
      } catch (err) {
        console.error("Failed to fetch trends:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, [country, category]);

  /* ---------------------------------- */
  /* 🔥 WEBSOCKET (StrictMode Safe)     */
  /* ---------------------------------- */
  useEffect(() => {
    if (!user?.email) return;

    if (didConnect.current) return;
    didConnect.current = true;

    const socket = new WebSocket(
      `${WS_BASE}/ws/${encodeURIComponent(user.email)}`
    );

    ws.current = socket;

    socket.onopen = () => {
      console.log("WebSocket Connected ✅");

      socket.send(
        JSON.stringify({
          action: "join_room",
          room: "global",
        })
      );
    };

    socket.onmessage = (event) => {
      let data;
      try {
        data = JSON.parse(event.data);
      } catch {
        return;
      }

      if (data.type === "trend_update" && data.trend) {
        setTrends((prev) => [data.trend, ...prev].slice(0, 20));
        return;
      }

      if (data.type === "message") {
        setMessages((prev) => [...prev, data]);
        return;
      }
    };

    socket.onerror = (err) => {
      console.log("WebSocket error:", err);
    };

    socket.onclose = (e) => {
      console.log("WebSocket closed:", e.code, e.reason);
    };

    return () => {
      didConnect.current = false;

      if (
        socket.readyState === WebSocket.OPEN ||
        socket.readyState === WebSocket.CONNECTING
      ) {
        socket.close();
      }

      ws.current = null;
    };
  }, [user?.email]);

  /* ---------------------------------- */
  /* ✅ AUTO SCROLL CHAT                */
  /* ---------------------------------- */
  useEffect(() => {
    if (!chatRef.current) return;
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages, chatOpen]);

  /* ---------------------------------- */
  /* ✅ SEND MESSAGE                    */
  /* ---------------------------------- */
  const sendMessage = () => {
    const text = chatInput.trim();
    if (!text) return;

    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      console.log("WebSocket not ready yet");
      return;
    }

    ws.current.send(
      JSON.stringify({
        action: "message",
        text: "chatInput",
        room: "global",
      })
    );

    setChatInput("");
  };
/* private message */
useEffect(() => {
  const loadMessages = async () => {
    const res = await axios.get(
  `${API_BASE}/api/rooms/${room}/messages`,
  { withCredentials: False }
);

    setMessages(res.data);
  };



  loadMessages();
}, [room]);
  /* ---------------------------------- */
  /* ⭐ FAVORITES                       */
  /* ---------------------------------- */
  const toggleFavorite = (trend) => {
    let updated;

    if (favorites.some((f) => f.title === trend.title)) {
      updated = favorites.filter((f) => f.title !== trend.title);
    } else {
      updated = [...favorites, trend];
    }

    setFavorites(updated);
    localStorage.setItem("favorites", JSON.stringify(updated));
  };

  const filtered = trends.filter((t) =>
    (t.title || "").toLowerCase().includes(search.toLowerCase())
  );

  /* ---------------------------------- */
  /* 🎨 UI                              */
  /* ---------------------------------- */
  return (
    <div className="p-6 md:p-10 text-white">
      <h2 className="text-3xl font-bold mb-6">🔥 Trending Dashboard</h2>

      {/* Country & Category */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="px-4 py-2 rounded text-white"
        >
          {countries.map((c) => (
            <option key={c.code} value={c.code}>
              {c.name}
            </option>
          ))}
        </select>

        {["Google", "Reddit", "Twitter", "News"].map((item) => (
          <button
            key={item}
            onClick={() => setCategory(item)}
            className={`px-4 py-2 rounded ${
              category === item ? "bg-indigo-600 text-white" : "bg-gray-200 text-black"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      {/* Search */}
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search trends..."
        className="px-4 py-2 rounded bg-gray-800 w-full md:w-1/3 mb-6"
      />

      {/* Trends */}
      {loading ? (
        <p>Loading trends...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filtered.map((trend, index) => {
            const isFav = favorites.some((f) => f.title === trend.title);

            return (
              <div
                key={`${trend.title}-${index}`}
                className="p-4 bg-gray-800 rounded relative"
              >
                <span className="absolute top-2 left-2 text-sm">
                  #{index + 1}
                </span>

                <button
                  onClick={() => toggleFavorite(trend)}
                  className="absolute top-2 right-2"
                >
                  {isFav ? "⭐" : "☆"}
                </button>

                <h3 className="mt-6 font-semibold">{trend.title}</h3>
                <p className="text-gray-400 text-sm">{trend.source}</p>
              </div>
            );
          })}
        </div>
      )}

      {/* CHAT */}
      <div className="fixed right-6 bottom-6 w-80">
        <button
          onClick={() => setChatOpen((v) => !v)}
          className="w-full mb-2 px-3 py-2 bg-indigo-600 rounded"
        >
          {chatOpen ? "Hide Chat" : "Show Chat"}
        </button>

        {chatOpen && (
          <div className="bg-black p-3 rounded flex flex-col h-96">
            <div className="text-sm mb-2">
              You: {user?.email || "guest"}
            </div>

            <div
              ref={chatRef}
              className="flex-1 overflow-y-auto space-y-2 text-sm mb-2"
            >
              {messages.map((msg, i) => (
                <div key={i} className="bg-gray-800 p-2 rounded">
                  <b>{msg.from || "system"}:</b>{" "}
                  {msg.text || msg.message}
                </div>
              ))}
            </div>
              {/* 🧪 Test Private Chat Button */}
            <div className="mt-6">
             <button
                 onClick={() => openPrivateChat("john@gmail.com")}
                  className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded text-white shadow-md"
                >
                 💬 Chat with John
             </button>
            </div>
            <div className="flex gap-2">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                className="flex-1 px-2 py-1 bg-gray-700 rounded"
              />
              <button
                onClick={sendMessage}
                className="px-3 py-1 bg-indigo-600 rounded"
              >
                Send
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
