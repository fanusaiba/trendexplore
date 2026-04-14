import { useEffect, useState } from "react";
import api from "../api";
import CompareChart from "../components/CompareChart";

export default function Compare() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAllTrends = async () => {
      setLoading(true);

      try {
        const countries = [
          { code: "US", name: "United States" },
          { code: "GB", name: "United Kingdom" },
          { code: "IN", name: "India" }
        ];

        let allTrends = [];

        for (const country of countries) {
          const res = await api.get(
            `/api/trends?country=${country.code}&category=all`
          );

          const countryTrends = res.data.trends.map((trend) => ({
            ...trend,
            country: country.name,
          }));

          allTrends = [...allTrends, ...countryTrends];
        }

        setTrends(allTrends);

      } catch (err) {
        console.error("Error fetching trends:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllTrends();
  }, []);

  return (
    <div className="max-w-6xl mx-auto bg-white p-5 rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        🌍 Country Trends Comparison
      </h2>

      {loading ? (
        <div className="text-center text-gray-500 py-10">
          Loading trends for comparison...
        </div>
      ) : trends.length === 0 ? (
        <div className="text-center text-gray-400 py-10">
          No trends available.
        </div>
      ) : (
        <CompareChart trends={trends} />
      )}
    </div>
  );
}