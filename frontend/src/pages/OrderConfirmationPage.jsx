import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { api } from "../services/api";

const STATUS_STEPS = [
  "PENDING",
  "CONFIRMED",
  "IN_PREPARATION",
  "OUT_FOR_DELIVERY",
  "DELIVERED",
];

export default function OrderConfirmationPage() {
  const { orderId } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api
      .getOrder(orderId)
      .then(setOrder)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [orderId]);

  if (loading) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 text-center text-gray-400">
        <div className="text-4xl mb-3 animate-spin inline-block">⏳</div>
        <p>Loading order…</p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 text-center text-gray-400">
        <p className="text-red-500">{error ?? "Order not found"}</p>
      </div>
    );
  }

  const currentStep = STATUS_STEPS.indexOf(order.status);

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <p className="text-5xl mb-3">🎉</p>
        <h1 className="text-3xl font-bold text-gray-900">Order placed!</h1>
        <p className="text-gray-500 mt-1 font-mono text-sm">{order.order_id}</p>
      </div>

      {order.status !== "CANCELLED" && (
        <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Status</h2>
          <div className="flex items-center gap-1">
            {STATUS_STEPS.map((step, i) => (
              <div key={step} className="flex items-center flex-1">
                <div
                  className={`w-3 h-3 rounded-full flex-shrink-0 ${
                    i <= currentStep ? "bg-orange-500" : "bg-gray-200"
                  }`}
                />
                {i < STATUS_STEPS.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 ${
                      i < currentStep ? "bg-orange-500" : "bg-gray-200"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            {STATUS_STEPS.map((step, i) => (
              <span
                key={step}
                className={`text-[10px] ${i === currentStep ? "text-orange-500 font-semibold" : "text-gray-400"}`}
                style={{
                  width: `${100 / STATUS_STEPS.length}%`,
                  textAlign: "center",
                }}
              >
                {step.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="bg-gray-50 rounded-xl border border-gray-200 p-5 mb-6 text-sm space-y-2">
        <div className="flex justify-between text-gray-600">
          <span>Subtotal</span>
          <span>${order.subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Tax</span>
          <span>${order.tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Delivery fee</span>
          <span>${order.delivery_fee.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Tip</span>
          <span>${order.tip.toFixed(2)}</span>
        </div>
        <div className="flex justify-between font-bold text-gray-900 text-base pt-2 border-t border-gray-200">
          <span>Total</span>
          <span>${order.total.toFixed(2)}</span>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <button
          onClick={() => navigate(`/track/${orderId}`)}
          className="w-full py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-sm font-semibold transition-colors"
        >
          🚗 Track My Delivery
        </button>
        <div className="flex gap-3">
          <Link
            to="/browse"
            className="flex-1 text-center py-3 rounded-xl border border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
          >
            Order again
          </Link>
          <Link
            to="/profile"
            className="flex-1 text-center py-3 rounded-xl border border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
          >
            View profile
          </Link>
        </div>
      </div>
    </div>
  );
}
