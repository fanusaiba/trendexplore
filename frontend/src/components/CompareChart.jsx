import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function CompareChart({ trends }) {
  /**
   * trends: array of trend objects from backend
   * Each trend: { title, source, country, score, url }
   */

  // Convert data into chart-friendly format
  // Group trends by title across countries
  const grouped = {};

  trends.forEach((t) => {
    if (!grouped[t.title]) grouped[t.title] = { title: t.title };
    grouped[t.title][t.country] = t.score;
  });

  const chartData = Object.values(grouped);

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="font-semibold text-lg mb-4">Trend Comparison</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <XAxis dataKey="title" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="US" fill="#1D4ED8" />
          <Bar dataKey="UK" fill="#10B981" />
          <Bar dataKey="IN" fill="#F59E0B" />
          {/* Add more countries if needed */}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
