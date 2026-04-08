import { useParams } from "react-router-dom";
import { useDelivery } from "../hooks/useDelivery";

const STATUS_STEPS = ["ASSIGNED", "IN_TRANSIT", "DELIVERED"];

const STATUS_META = {
  ASSIGNED:  { label: "Driver Assigned", emoji: "🧍", color: "bg-yellow-400" },
  IN_TRANSIT: { label: "On the Way",     emoji: "🚗", color: "bg-blue-500"   },
  DELIVERED:  { label: "Delivered!",     emoji: "✅", color: "bg-green-500"  },
};

export default function DeliveryTrackingPage() {
  const { orderId } = useParams();
  const { delivery, loading, error } = useDelivery(orderId);

  if (loading) return (
    <div className="flex justify-center items-center h-64 text-gray-500">
      Loading delivery info...
    </div>
  );

  if (error) return (
    <div className="max-w-md mx-auto mt-16 p-4 bg-red-50 rounded-xl text-red-600 text-center">
      ⚠️ {error}
    </div>
  );

  if (!delivery) return (
    <div className="text-center mt-16 text-gray-400">
      No delivery found for this order.
    </div>
  );

  const currentStep = STATUS_STEPS.indexOf(delivery.status);
  const meta = STATUS_META[delivery.status];

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      <div className="text-center mb-8">
        <p className="text-5xl mb-2">{meta.emoji}</p>
        <h2 className="text-2xl font-bold text-gray-900">{meta.label}</h2>
        <p className="text-gray-400 text-sm mt-1">Order #{orderId}</p>
      </div>

      <div className="flex items-center mb-8">
        {STATUS_STEPS.map((step, i) => {
          const done = i <= currentStep;
          return (
            <div key={step} className="flex-1 flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold
                ${done ? STATUS_META[step].color : "bg-gray-200"}`}>
                {i + 1}
              </div>
              <p className={`text-xs mt-1 text-center ${done ? "text-gray-800 font-semibold" : "text-gray-400"}`}>
                {STATUS_META[step].label}
              </p>
              {i < STATUS_STEPS.length - 1 && (
                <div className={`absolute`} />
              )}
            </div>
          );
        })}
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">📍 Delivering to</span>
          <span className="font-medium text-gray-800 text-right max-w-[60%]">{delivery.address}</span>
        </div>

        {delivery.instructions && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">📝 Instructions</span>
            <span className="font-medium text-gray-800 text-right max-w-[60%]">{delivery.instructions}</span>
          </div>
        )}

        <div className="flex justify-between text-sm">
          <span className="text-gray-500">🚘 Driver ID</span>
          <span className="font-medium text-gray-800">{delivery.driver_id}</span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-500">🕐 Created</span>
          <span className="font-medium text-gray-800">
            {new Date(delivery.created_at).toLocaleString()}
          </span>
        </div>

        {delivery.completed_at && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">✅ Completed</span>
            <span className="font-medium text-green-600">
              {new Date(delivery.completed_at).toLocaleString()}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}