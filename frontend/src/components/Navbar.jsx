import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();

  const link = (to, label) => (
    <Link
      to={to}
      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
        pathname === to
          ? "bg-orange-500 text-white"
          : "text-gray-600 hover:text-orange-500"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-orange-500">
          QuickBite
        </Link>
        <div className="flex gap-1">
          {link("/", "Home")}
          {link("/badges", "Badges")}
          {link("/profile", "Profile")}
        </div>
      </div>
    </nav>
  );
}
