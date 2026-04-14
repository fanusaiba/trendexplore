export default function Header() {
  return (
    <nav className="flex items-center justify-between px-8 py-4 backdrop-blur-md bg-white/5 border-b border-white/10">
      <h1 className="text-2xl font-bold tracking-wide">
        TrendExplore 🌍
      </h1>

      <div className="flex gap-6 text-sm text-gray-300">
        <a className="hover:text-white transition cursor-pointer">
          Home
        </a>
        <a className="hover:text-white transition cursor-pointer">
          Chat
        </a>
        <a className="hover:text-white transition cursor-pointer">
          Compare
        </a>
      </div>
    </nav>
  );
}
