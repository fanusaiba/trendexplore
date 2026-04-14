import { useEffect, useState } from "react";
import api from "../api";
import countries from "../data/countries";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(countries[0]);

  useEffect(() => {
    if (!selectedCountry) return;

    api
      .get(`/api/trends?country=${selectedCountry.code}&category=all`)
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));

  }, [selectedCountry]);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h2>🔥 Trending Dashboard</h2>

      {/* 🌍 COUNTRY DROPDOWN */}
      <select
        value={selectedCountry.code}
        onChange={(e) => {
          const country = countries.find(c => c.code === e.target.value);
          setSelectedCountry(country);
        }}
      >
        {countries.map((c) => (
          <option key={c.code} value={c.code}>
            {c.name}
          </option>
        ))}
      </select>

      {/* 📊 TRENDS */}
      {data.trends.map((trend, index) => (
        <div key={index}>
          <h3>{trend.title}</h3>
          <p>{trend.source} | Score: {trend.score}</p>
        </div>
      ))}
    </div>
  );
}