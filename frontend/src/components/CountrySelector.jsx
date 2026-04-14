export default function CountrySelector({ country, setCountry }) {
  const countries = ["US", "IN", "UK", "CA", "AU"];

  return (
    <select
      value={country}
      onChange={(e) => setCountry(e.target.value)}
      className="
        bg-white/10 border border-white/20
        px-4 py-2 rounded-lg text-sm
        focus:outline-none focus:ring-2 focus:ring-indigo-500
      "
    >
      {countries.map((c) => (
        <option key={c} value={c} className="text-black">
          {c}
        </option>
      ))}
    </select>
  );
}
