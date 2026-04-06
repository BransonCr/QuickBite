import { useState, useEffect, useCallback, useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";

const PLACEHOLDER_IMAGES = [
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80"
];

export default function RestaurantDetailPage() {
  const { id } = useParams();
  
  const [restaurant, setRestaurant] = useState(null);
  const [menuItems, setMenuItems] = useState([]); // NEW: Menu state
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPageData = useCallback(async () => {
    try {
      setLoading(true);
      
      // Fetch both the restaurant details AND the menu at the same time!
      const [restData, menuData] = await Promise.all([
        api.getRestaurant(id),
        api.getMenuByRestaurant(id).catch(() => []) // If menu fails, return empty array so page doesn't crash
      ]);

      setRestaurant(restData);
      setMenuItems(menuData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchPageData();
    window.scrollTo(0, 0);
  }, [fetchPageData]);

  // Group menu items by their category (e.g., { "Mains": [...], "Drinks": [...] })
  const groupedMenu = useMemo(() => {
    if (!menuItems || menuItems.length === 0) return {};
    
    return menuItems.reduce((groups, item) => {
      const category = item.category || "Other";
      if (!groups[category]) {
        groups[category] = [];
      }
      groups[category].push(item);
      return groups;
    }, {});
  }, [menuItems]);

  const bannerImage = useMemo(() => {
    if (!id) return PLACEHOLDER_IMAGES[0];
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = id.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % PLACEHOLDER_IMAGES.length;
    return PLACEHOLDER_IMAGES[index];
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center text-gray-400">
        <div className="text-4xl mb-3 animate-spin inline-block">🍽️</div>
        <p>Loading restaurant details...</p>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      // ... (Keep existing error state UI) ...
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <div className="bg-red-50 text-red-500 rounded-xl p-6 inline-block">
          <p className="font-medium text-lg">Failed to load restaurant</p>
          <p className="text-sm mt-1 mb-4">{error || "Restaurant not found"}</p>
          <Link to="/browse" className="text-sm text-red-600 underline">← Back to Browse</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* ... (Keep existing Back Navigation, Hero Banner, and Info Grid) ... */}
      <div className="mb-4">
        <Link to="/browse" className="text-sm text-orange-500 hover:text-orange-600 font-medium">
          ← Back to Search
        </Link>
      </div>

      {/* Hero Banner */}
      <div className="w-full h-64 md:h-80 rounded-2xl overflow-hidden relative mb-8 shadow-sm border border-gray-200">
        <img src={bannerImage} alt={restaurant.name} className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex flex-col justify-end p-6 md:p-8">
          <div className="flex items-center gap-3 mb-2">
            {restaurant.is_active ? (
              <span className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wide shadow-sm">Open Now</span>
            ) : (
              <span className="bg-gray-500 text-white text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wide shadow-sm">Currently Closed</span>
            )}
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-white drop-shadow-md">{restaurant.name}</h1>
        </div>
      </div>

      {/* Info Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-lg font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2">Details</h2>
          <div className="flex gap-3 mb-3 text-gray-600 text-sm">
            <span className="text-xl">📍</span>
            <div><p className="font-medium text-gray-900">Address</p><p>{restaurant.location}</p><p>{restaurant.postal_code}</p></div>
          </div>
          <div className="flex gap-3 text-gray-600 text-sm">
            <span className="text-xl">🕒</span>
            <div><p className="font-medium text-gray-900">Operating Hours</p><p>{restaurant.operating_hours}</p></div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <h2 className="text-lg font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2">Info</h2>
          <div className="flex gap-3 mb-3 text-gray-600 text-sm">
            <span className="text-xl">📞</span>
            <div><p className="font-medium text-gray-900">Contact</p><p>{restaurant.contact_info}</p></div>
          </div>
          <div className="flex gap-3 text-gray-600 text-sm">
            <span className="text-xl">🛵</span>
            <div><p className="font-medium text-gray-900">Delivery Radius</p><p>{restaurant.delivery_radius} km</p></div>
          </div>
        </div>
      </div>

      {/* NEW: Dynamic Menu Section */}
      <div className="mb-10">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Menu</h2>
        
        {menuItems.length === 0 ? (
          <div className="text-center py-12 border-2 border-dashed border-gray-200 rounded-xl bg-gray-50">
            <p className="text-gray-500">No menu items available for this restaurant yet.</p>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Iterate over each category group */}
            {Object.entries(groupedMenu).map(([category, items]) => (
              <div key={category} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                {/* Category Header */}
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-bold text-gray-900 capitalize">{category}</h3>
                </div>
                
                {/* Menu Items List */}
                <div className="divide-y divide-gray-100">
                  {items.map((item) => (
                    <div 
                      key={item.item_id || item.id} // Fallback just in case mapping differs
                      className={`p-6 flex flex-col sm:flex-row justify-between gap-4 transition-colors hover:bg-gray-50 ${!item.is_available ? 'opacity-60' : ''}`}
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="text-base font-bold text-gray-900">{item.name}</h4>
                          {!item.is_available && (
                            <span className="text-[10px] font-bold uppercase tracking-wide bg-red-100 text-red-600 px-2 py-0.5 rounded">Sold Out</span>
                          )}
                        </div>
                        <p className="text-sm text-gray-500 line-clamp-2">{item.description}</p>
                      </div>
                      
                      <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-start gap-4 sm:gap-2">
                        <p className="text-lg font-bold text-gray-900">${item.price.toFixed(2)}</p>
                        <button 
                          disabled={!item.is_available}
                          className="px-4 py-2 bg-orange-50 text-orange-600 text-sm font-medium rounded-lg hover:bg-orange-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                        >
                          + Add
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}