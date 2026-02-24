import { useState } from "react";
import { Heart, Share2, Brain } from "lucide-react";
import axios from "axios";
import {api} from "../api";
export default function TrendCard({ trend, favorites, setFavorites }) {
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  const isFav = favorites.some((f) => f.title === trend.title);

  const toggleFavorite = () => {
    if (isFav) {
      setFavorites(favorites.filter((f) => f.title !== trend.title));
    } else {
      setFavorites([...favorites, trend]);
    }
  };

  const copyLink = () => {
    navigator.clipboard.writeText(trend.url);
    alert("Link copied to clipboard!");
  };

  const analyzeTrend = async () => {
    try {
      setLoading(true);
      const res = await api.post("/api/analyze", {
        title: trend.title,
      });
      setInsight(res.data);
    } catch (err) {
      console.error("AI analysis failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.04 }}
      transition={{ duration: 0.25 }}
      className="
        p-5 rounded-2xl
        bg-white/5 backdrop-blur-md
        border border-white/10
        hover:bg-white/10
        transition cursor-pointer
      "
    >
      <h2 className="font-semibold text-lg mb-1 text-white">
        {trend.title}
      </h2>
      <p className="text-sm text-gray-400 mb-4">
        {trend.source}
      </p>

      <div className="flex justify-between items-center mb-3">
        <a
          href={trend.url}
          target="_blank"
          rel="noreferrer"
          className="text-indigo-400 hover:text-indigo-300 text-sm"
        >
          View Source →
        </a>

        <div className="flex space-x-4 items-center">
          <Heart
            size={20}
            onClick={toggleFavorite}
            className={`cursor-pointer transition ${
              isFav
                ? "fill-red-500 text-red-500"
                : "text-gray-400 hover:text-red-500"
            }`}
          />
          <Share2
            size={20}
            onClick={copyLink}
            className="cursor-pointer text-gray-400 hover:text-indigo-400"
          />
          <Brain
            size={20}
            onClick={analyzeTrend}
            className="cursor-pointer text-gray-400 hover:text-purple-400"
            title="Analyze trend with AI"
          />
        </div>
      </div>

      {loading && (
        <p className="text-sm text-gray-400">
          Analyzing with AI...
        </p>
      )}

      {insight && (
        <div className="mt-3 p-3 rounded-lg bg-black/30 border border-white/10 text-sm text-gray-300">
          <p>
            <strong className="text-white">🧠 Insight:</strong>{" "}
            {insight.summary}
          </p>
          <p className="mt-1">
            <strong className="text-white">Sentiment:</strong>{" "}
            {insight.sentiment}
          </p>
        </div>
      )}
    </motion.div>
  );
}
