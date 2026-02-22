import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/trends?country=US&category=All", {
      credentials: "include", // IMPORTANT
    })
      .then((res) => res.json())
      .then((data) => setData(data));
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
