import { useEffect, useState } from "react";
import axios from "axios";
import CompareChart from "../components/CompareChart";

export default function Compare() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAllTrends = async () => {
      setLoading(true);
      try {
        const countries = ["US", "UK", "IN"];
        const category = "All";
        let allTrends = [];

        for (const country of countries) {
          const res = await axios.get(
            `http://127.0.0.1:8000/api/trends?country=${country}&category=${category}`
          );

          // Attach country label to each trend (important for chart grouping)
          const countryTrends = res.data.map((trend) => ({
            ...trend,
            country,
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
    <div className="min-h-screen bg-gray-100 px-6 py-10">
      
      <div className="max-w-6xl mx-auto bg-white p-8 rounded-xl shadow-lg">
        
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
      
    </div>
  );
}