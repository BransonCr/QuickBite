import { useState, useEffect } from "react";
import { useNavigate, useParams, Link, useLocation } from "react-router-dom";
import { api } from "../services/api";

export default function UpdateMenuItemPage() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Grab IDs from the URL
  const { id: restaurantId, itemId } = useParams();

  // Get the existing item data passed from the detail page
  const existingItem = location.state?.item || {};

  const [formData, setFormData] = useState({
    name: existingItem.name || "",
    description: existingItem.description || "",
    price: existingItem.price || "",
    category: existingItem.category || "",
    is_available: existingItem.is_available ?? true,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Safety check: If they refreshed the page and lost state, send them back
  useEffect(() => {
    if (!existingItem.name) {
      navigate(`/restaurant/${restaurantId}`);
    }
  }, [existingItem, navigate, restaurantId]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        price: parseFloat(formData.price) || 0.0, 
      };

      await api.updateMenuItem(itemId, payload);
      navigate(`/restaurant/${restaurantId}`);
    } catch (err) {
      setError(err.message || "Failed to update menu item.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          to={`/restaurant/${restaurantId}`}
          className="text-sm text-orange-500 hover:text-orange-600 font-medium"
        >
          ← Back to Menu
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">Edit Menu Item</h1>
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Item Name</label>
          <input
            type="text"
            name="name"
            required
            value={formData.name}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            name="description"
            rows="3"
            value={formData.description}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
            <input
              type="number"
              name="price"
              step="0.01"
              min="0"
              required
              value={formData.price}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <input
              type="text"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
        </div>

        <div className="flex items-center gap-2 pt-2">
          <input
            type="checkbox"
            name="is_available"
            id="is_available"
            checked={formData.is_available}
            onChange={handleChange}
            className="w-4 h-4 text-orange-500 border-gray-300 rounded focus:ring-orange-400"
          />
          <label htmlFor="is_available" className="text-sm font-medium text-gray-700">
            Item is currently available
          </label>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-xl mt-4 transition-colors disabled:bg-orange-300 flex justify-center items-center gap-2"
        >
          {isSubmitting ? "Saving..." : "Update Item"}
        </button>
      </form>
    </div>
  );
}