

export default function CategoryTabs({ category, setCategory }) {
  const categories = ["All", "Google", "Reddit", "Twitter", "News"];

  return (
    <div className="flex space-x-3 relative">
      {categories.map((c) => (
        <button
          key={c}
          onClick={() => setCategory(c)}
          className={`px-4 py-2 rounded-full relative transition-colors ${
            category === c ? "text-blue-600 font-semibold" : "text-gray-600"
          }`}
        >
          {c}

          {/* Animated underline */}
          {category === c && (
            <motion.div
              layoutId="underline"
              className="absolute left-0 bottom-0 w-full h-0.5 bg-blue-600 rounded"
              transition={{ duration: 0.3 }}
            />
          )}
        </button>
      ))}
    </div>
  );
}

