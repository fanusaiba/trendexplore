import { useEffect, useState } from "react";
import api  from "../api";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api
      .get("/api/trends?country=US&category=All")
      .then((res) => setData(res.data));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h2>Welcome {data.user}</h2>
      {data.trends.map((trend, index) => (
        <div key={index}>
          <h3>{trend.title}</h3>
          <p>{trend.source} | Score: {trend.score}</p>
        </div>
      ))}
    </div>
  );
}
