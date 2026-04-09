import { useParams } from "react-router-dom";
import { useDelivery } from "../hooks/useDelivery";
import { useState } from "react";

const STATUS_STEPS = ["ASSIGNED", "IN_TRANSIT", "DELIVERED"];

const STATUS_META = {
  ASSIGNED:  { label: "Driver Assigned", emoji: "🧍", color: "bg-yellow-400" },
  IN_TRANSIT: { label: "On the Way",     emoji: "🚗", color: "bg-blue-500"   },
  DELIVERED:  { label: "Delivered!",     emoji: "✅", color: "bg-green-500"  },
};

export default function DeliveryTrackingPage() {
  const params = useParams();
  const orderId = params.orderId;
  const { delivery, loading, error, fetchByOrder, updateStatus } = useDelivery(orderId);
  const [simulating, setSimulating] = useState(false);
  const [simError, setSimError] = useState(null);

  const handleSimulate = async () => {
    setSimError(null);
    if (!orderId) {
      setSimError("No order ID in URL — navigate here from an order confirmation page.");
      return;
    }
    setSimulating(true);
    try {
      const res = await fetch("/api/delivery/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_id: orderId,
          driver_id: "driver-demo-001",
          address: "123 QuickBite Lane, Vancouver, BC",
          instructions: "Leave at door",
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setSimError("Backend error: " + JSON.stringify(data.detail));
        return;
      }
      await fetchByOrder(orderId);
    } catch (err) {
      setSimError("Network error: " + err.message);
    } finally {
      setSimulating(false);
    }
  };

  const handleStatusAdvance = async () => {
    if (!delivery) return;
    const currentIndex = STATUS_STEPS.indexOf(delivery.status);
    const nextStatus = STATUS_STEPS[currentIndex + 1];
    if (!nextStatus) return;
    await updateStatus(delivery.delivery_id, nextStatus);
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64 text-gray-500">
      Loading delivery info...
    </div>
  );

  if (error && error !== "Delivery not found") return (
    <div className="max-w-md mx-auto mt-16 p-4 bg-red-50 rounded-xl text-red-600 text-center">
      ⚠️ {error}
    </div>
  );

  if (!delivery) return (
    <div className="max-w-md mx-auto px-4 py-16 text-center">
      <p className="text-5xl mb-4">📦</p>
      <h2 className="text-xl font-bold text-gray-800 mb-2">No delivery assigned yet</h2>
      <p className="text-gray-400 text-sm mb-6">
        Order: <span className="font-mono">{orderId ?? "unknown"}</span>
      </p>
      {simError && (
        <div className="mb-4 p-3 bg-red-50 rounded-xl text-red-600 text-sm text-left">
          {simError}
        </div>
      )}
      <button
        onClick={handleSimulate}
        disabled={simulating || !orderId}
        className="w-full py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold transition-colors disabled:opacity-50"
      >
        {simulating ? "Creating delivery..." : "🚀 Simulate Delivery"}
      </button>
    </div>
  );

  const currentStep = STATUS_STEPS.indexOf(delivery.status);
  const meta = STATUS_META[delivery.status];
  const isComplete = delivery.status === "DELIVERED";

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      <div className="text-center mb-8">
        <p className="text-5xl mb-2">{meta.emoji}</p>
        <h2 className="text-2xl font-bold text-gray-900">{meta.label}</h2>
        <p className="text-gray-400 text-sm mt-1 font-mono">Order #{orderId}</p>
      </div>

      <div className="flex items-start mb-8">
        {STATUS_STEPS.map((step, i) => {
          const done = i <= currentStep;
          return (
            <div key={step} className="flex-1 flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${done ? STATUS_META[step].color : "bg-gray-200"}`}>
                {i + 1}
              </div>
              <p className={`text-xs mt-1 text-center ${done ? "text-gray-800 font-semibold" : "text-gray-400"}`}>
                {STATUS_META[step].label}
              </p>
            </div>
          );
        })}
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 space-y-3 mb-6">
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
          <span className="font-medium text-gray-800">{new Date(delivery.created_at).toLocaleString()}</span>
        </div>
        {delivery.completed_at && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">✅ Completed</span>
            <span className="font-medium text-green-600">{new Date(delivery.completed_at).toLocaleString()}</span>
          </div>
        )}
      </div>

      {!isComplete && (
        <button
          onClick={handleStatusAdvance}
          className="w-full py-3 rounded-xl bg-gray-800 hover:bg-gray-900 text-white text-sm font-semibold transition-colors"
        >
          ⏩ Advance to "{STATUS_META[STATUS_STEPS[currentStep + 1]]?.label}"
        </button>
      )}
      {isComplete && (
        <div className="text-center py-4 text-green-600 font-semibold">
          🎉 Your order has been delivered!
        </div>
      )}
    </div>
  );
}