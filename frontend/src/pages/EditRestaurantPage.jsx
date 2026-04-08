import { useState, useEffect } from "react";
import { useNavigate, useParams, Link, useLocation } from "react-router-dom";
import { api } from "../services/api";

export default function EditRestaurantPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { id } = useParams();

  // Grab the data passed from the detail page
  const existingRestaurant = location.state?.restaurant || {};

  const [formData, setFormData] = useState({
    name: existingRestaurant.name || "",
    location: existingRestaurant.location || "",
    postal_code: existingRestaurant.postal_code || "",
    delivery_radius: existingRestaurant.delivery_radius || "",
    contact_info: existingRestaurant.contact_info || "",
    operating_hours: existingRestaurant.operating_hours || "",
    is_active: existingRestaurant.is_active ?? true,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Safety check: if they refreshed the page directly on this URL
  useEffect(() => {
    if (!existingRestaurant.name) {
      navigate(`/restaurant/${id}`);
    }
  }, [existingRestaurant, navigate, id]);

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
        delivery_radius: parseFloat(formData.delivery_radius) || 0.0,
      };

      await api.updateRestaurant(id, payload);
      navigate(`/restaurant/${id}`); // Send them back to the updated detail page
    } catch (err) {
      setError(err.message || "Failed to update restaurant.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          to={`/restaurant/${id}`}
          className="text-sm text-orange-500 hover:text-orange-600 font-medium"
        >
          ← Back to Restaurant
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">Edit Restaurant</h1>
      <p className="text-gray-600 mb-8">Update the details for {formData.name}.</p>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b pb-2">
            <h2 className="text-xl font-semibold text-gray-800">Basic Information</h2>
            <div className="flex items-center gap-2">
              <label htmlFor="is_active" className="text-sm font-bold text-gray-700">Open for Business:</label>
              <input
                type="checkbox"
                name="is_active"
                id="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                className="w-5 h-5 text-green-500 border-gray-300 rounded focus:ring-green-400"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Restaurant Name</label>
            <input
              type="text"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contact Info</label>
              <input
                type="text"
                name="contact_info"
                required
                value={formData.contact_info}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Operating Hours</label>
              <input
                type="text"
                name="operating_hours"
                required
                value={formData.operating_hours}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
          </div>
        </div>

        <div className="space-y-4 pt-4">
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2">Location Details</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Street Address</label>
            <input
              type="text"
              name="location"
              required
              value={formData.location}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Postal Code</label>
              <input
                type="text"
                name="postal_code"
                required
                value={formData.postal_code}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Delivery Radius (km)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                name="delivery_radius"
                required
                value={formData.delivery_radius}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-xl mt-8 transition-colors disabled:bg-orange-300 flex justify-center items-center gap-2"
        >
          {isSubmitting ? "Saving..." : "Save Changes"}
        </button>
      </form>
    </div>
  );
}