import { Link } from "react-router-dom";
import { useMemo } from "react";

// A collection of great restaurant/food placeholder images
const PLACEHOLDER_IMAGES = [
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=400&q=80"
];

export default function RestaurantCard({ restaurant }) {
  // Destructure with fallback values
  const {
    id,
    name = "Unnamed Restaurant",
    price_category = "",
    rating = 0,
    image, // We don't set a default here anymore, the hook handles it
  } = restaurant;

  // Use the restaurant's ID to deterministically pick a placeholder image.
  const displayImage = useMemo(() => {
    if (image) return image; // Use actual image if backend provides one
    
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = id.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    const index = Math.abs(hash) % PLACEHOLDER_IMAGES.length;
    return PLACEHOLDER_IMAGES[index];
  }, [id, image]);

  return (
    <Link 
      to={`/restaurant/${id}`}
      className="group flex flex-col bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow duration-200"
    >
      {/* Image Container */}
      <div className="relative h-48 w-full overflow-hidden bg-gray-100">
        <img
          src={displayImage}
          alt={name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      {/* Content Container */}
      <div className="p-4 flex flex-col flex-1">
        <div className="flex justify-between items-start mb-1 gap-2">
          <h3 className="text-lg font-bold text-gray-900 group-hover:text-orange-500 transition-colors">
            {name}
          </h3>
          {/* Rating Indicator */}
          <div className="flex items-center gap-1 bg-gray-50 px-1.5 py-0.5 rounded text-sm font-medium text-gray-700 shrink-0">
            <span className="text-yellow-400">★</span>
            {rating > 0 ? rating.toFixed(1) : "New"}
          </div>
        </div>

        {/* Footer / Price & Action - Added mt-auto to push to bottom */}
        <div className="mt-auto flex items-center text-sm font-medium text-gray-700 pt-3 border-t border-gray-100">
          <span className="text-green-600">{price_category || "$$"}</span>
          <span className="mx-2 text-gray-300">•</span>
          <span className="text-orange-500 group-hover:text-orange-600 transition-colors">
            View Menu →
          </span>
        </div>
      </div>
    </Link>
  );
}