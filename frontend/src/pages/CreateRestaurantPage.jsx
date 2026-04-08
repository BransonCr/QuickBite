import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function CreateRestaurantPage() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    owner_id: "",
    name: "",
    location: "",
    postal_code: "",
    delivery_radius: "",
    contact_info: "",
    operating_hours: ""
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Auto-fill the owner ID if they are logged in
  useEffect(() => {
    const userId = localStorage.getItem("quickbite_user_id");
    if (userId) {
      setFormData(prev => ({ ...prev, owner_id: userId }));
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      // Format the payload to match the Pydantic schema exactly
      const payload = {
        ...formData,
        // Ensure delivery_radius is sent as a float to satisfy FastAPI
        delivery_radius: parseFloat(formData.delivery_radius) || 0.0,
      };

      const newRestaurant = await api.createRestaurant(payload);
      
      // Navigate to the newly created restaurant's page or a dashboard
      navigate(`/restaurant/${newRestaurant.restaurant_id || newRestaurant.id}`);
      
    } catch (err) {
      setError(err.message || "Failed to create restaurant. Please check your inputs.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Partner with QuickBite</h1>
      <p className="text-gray-600 mb-8">Fill out the details below to list your restaurant.</p>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        
        {/* Basic Info */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2">Basic Information</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Restaurant Name</label>
            <input
              type="text"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g., Burger Joint"
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contact Info (Phone/Email)</label>
              <input
                type="text"
                name="contact_info"
                required
                value={formData.contact_info}
                onChange={handleChange}
                placeholder="555-0199 or hello@burgerjoint.com"
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
                placeholder="Mon-Sun: 10AM - 10PM"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Location Info */}
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
              placeholder="123 Main St, Cityville"
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
                placeholder="A1A 1A1"
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
                placeholder="e.g., 5.0"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* System Settings */}
        <div className="space-y-4 pt-4">
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2">System Settings</h2>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Owner ID</label>
            <input
              type="text"
              name="owner_id"
              required
              value={formData.owner_id}
              onChange={handleChange}
              placeholder="User ID of the restaurant owner"
              className="w-full border border-gray-300 bg-gray-50 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
            <p className="text-xs text-gray-500 mt-1">This links the restaurant to your user account.</p>
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-xl mt-8 transition-colors disabled:bg-orange-300 flex justify-center items-center gap-2"
        >
          {isSubmitting ? (
            <>
              <span className="animate-spin inline-block">🔄</span> Creating...
            </>
          ) : (
            "Create Restaurant"
          )}
        </button>
      </form>
    </div>
  );
}