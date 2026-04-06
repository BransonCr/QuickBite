import { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import RestaurantCard from "../components/RestaurantCard"; // Assumed component

export default function BrowseRestaurantsPage() {
  // Form input states
  const [query, setQuery] = useState("");
  const [priceCategory, setPriceCategory] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  // Data states
  const [restaurants, setRestaurants] = useState([]);
  const [categories, setCategories] = useState([]);
  
  // UI states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  // 1. Fetch available categories on mount
  const fetchCategories = useCallback(async () => {
    try {
      // Assuming api.getCategories() calls the @router.get("/categories") endpoint
      const data = await api.getCategories();
      setCategories(data);
    } catch (e) {
      console.error("Failed to load categories:", e);
    }
  }, []);

  // 2. Fetch restaurants based on filters
  const fetchRestaurants = useCallback(async (searchParams) => {
    setLoading(true);
    setError(null);
    try {
      // Assuming api.searchRestaurants() maps to @router.get("/search")
      // Passing { query, price_category, category }
      const data = await api.searchRestaurants(searchParams);
      setRestaurants(data);
      setHasSearched(true);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchCategories();
    // Fetch initial list of all restaurants (empty parameters)
    fetchRestaurants({ query: "", price_category: "", category: "" });
  }, [fetchCategories, fetchRestaurants]);

  // Form submission handler
  function handleSubmit(e) {
    e.preventDefault();
    fetchRestaurants({
      query: query.trim(),
      price_category: priceCategory,
      category: selectedCategory,
    });
  }

  // Clear filters handler
  function handleClear() {
    setQuery("");
    setPriceCategory("");
    setSelectedCategory("");
    fetchRestaurants({ query: "", price_category: "", category: "" });
  }

  // Calculate active filters for the stats bar
  const activeFiltersCount = [query, priceCategory, selectedCategory].filter(Boolean).length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Browse Restaurants</h1>
        <p className="text-gray-500 mt-1">
          Discover new places to eat or search for your favorites.
        </p>
      </div>

      {/* Search and Filter Form */}
      <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-3 mb-8">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name..."
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white"
        >
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>

        <select
          value={priceCategory}
          onChange={(e) => setPriceCategory(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white"
        >
          <option value="">Any Price</option>
          <option value="$">$ (Inexpensive)</option>
          <option value="$$">$$ (Moderate)</option>
          <option value="$$$">$$$ (Expensive)</option>
        </select>

        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-600 text-white font-medium text-sm px-5 py-2 rounded-lg transition-colors whitespace-nowrap"
        >
          Search
        </button>

        {activeFiltersCount > 0 && (
          <button
            type="button"
            onClick={handleClear}
            className="text-sm text-gray-400 hover:text-gray-600 px-2 whitespace-nowrap"
          >
            Clear
          </button>
        )}
      </form>

      {/* Stats bar */}
      {!loading && !error && hasSearched && (
        <div className="flex items-center gap-6 mb-8 p-4 bg-orange-50 border border-orange-100 rounded-xl">
          <div>
            <p className="text-2xl font-bold text-orange-500">
              {restaurants.length}
            </p>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Results
            </p>
          </div>
          <div className="w-px h-10 bg-orange-200" />
          <div>
            <p className="text-2xl font-bold text-gray-400">
              {activeFiltersCount}
            </p>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Active Filters
            </p>
          </div>
          <div className="w-px h-10 bg-orange-200" />
          <div className="flex-1">
            <p className="text-sm text-gray-600">
              {activeFiltersCount > 0 
                ? "Showing filtered results based on your search criteria." 
                : "Showing all available restaurants."}
            </p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-4xl mb-3 animate-spin inline-block">🍽️</div>
          <p>Finding the best spots...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="text-center py-10 text-red-500 bg-red-50 rounded-xl">
          <p className="font-medium">Failed to load restaurants</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}

      {/* Restaurant Grid */}
      {!loading && !error && hasSearched && (
        <>
          {restaurants.length > 0 ? (
            <section className="mb-10">
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {restaurants.map((restaurant) => (
                  <RestaurantCard key={restaurant.id} restaurant={restaurant} />
                ))}
              </div>
            </section>
          ) : (
            <div className="text-center py-16 text-gray-400">
              <p className="text-5xl mb-4">🔍</p>
              <p className="text-lg font-medium text-gray-600">
                No restaurants found
              </p>
              <p className="text-sm mt-1">
                Try adjusting your search or clearing your filters to see more results.
              </p>
            </div>
          )}
        </>
      )}

      {/* Profile/Home link */}
      <div className="mt-10 text-center">
        <Link
          to="/"
          className="text-sm text-orange-500 hover:text-orange-600 underline underline-offset-2"
        >
          ← Back to Dashboard
        </Link>
      </div>
    </div>
  );
}