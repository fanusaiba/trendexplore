import useLocalStorage from "../hooks/useLocalStorage";
import TrendCard from "../components/TrendCard";

export default function Favorites() {
  const [favorites, setFavorites] = useLocalStorage("favorites", []);
  return (
    <div className="p-6 grid sm:grid-cols-2 md:grid-cols-3 gap-4">
      {favorites.map((t) => (
        <TrendCard
          key={t.title}
          trend={t}
          favorites={favorites}
          setFavorites={setFavorites}
        />
      ))}
    </div>
  );
}


