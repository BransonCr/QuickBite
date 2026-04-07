import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { api } from "../services/api";

const STORAGE_KEY = "quickbite_user_id";
const TAX_RATE = 0.1;
const DELIVERY_FEE = 3.99;

export default function CheckoutPage() {
  const { items, restaurantId, subtotal, clearCart } = useCart();
  const navigate = useNavigate();

  const [customerId, setCustomerId] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? "",
  );
  const [tip, setTip] = useState(0);
  const [customTip, setCustomTip] = useState("");
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState(null);

  const tax = subtotal * TAX_RATE;
  const tipAmount = customTip !== "" ? parseFloat(customTip) || 0 : tip;
  const total = subtotal + tax + DELIVERY_FEE + tipAmount;

  async function placeOrder() {
    if (!customerId.trim()) {
      setError("Enter your customer ID to place an order.");
      return;
    }
    if (items.length === 0) return;

    setPlacing(true);
    setError(null);
    try {
      const order = await api.createOrder({
        customer_id: customerId.trim(),
        restaurant_id: restaurantId,
        status: "PENDING",
        subtotal: parseFloat(subtotal.toFixed(2)),
        tax: parseFloat(tax.toFixed(2)),
        delivery_fee: DELIVERY_FEE,
        tip: parseFloat(tipAmount.toFixed(2)),
        total: parseFloat(total.toFixed(2)),
      });

      await Promise.all(
        items.map((item) =>
          api.createOrderItem({
            order_id: order.order_id,
            item_id: item.item_id,
            quantity: item.quantity,
            price_at_time: item.price,
          }),
        ),
      );

      localStorage.setItem(STORAGE_KEY, customerId.trim());
      clearCart();
      navigate(`/order/${order.order_id}`);
    } catch (e) {
      setError(e.message);
    } finally {
      setPlacing(false);
    }
  }

  if (items.length === 0) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 text-center text-gray-400">
        <p className="text-5xl mb-4">🛒</p>
        <p className="text-lg font-medium text-gray-600">Your cart is empty</p>
        <Link
          to="/browse"
          className="mt-4 inline-block text-sm text-orange-500 hover:text-orange-600 font-medium"
        >
          Browse restaurants
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          to={`/restaurant/${restaurantId}`}
          className="text-sm text-orange-500 hover:text-orange-600 font-medium"
        >
          Back to menu
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 mt-2">Checkout</h1>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Your order</h2>
        <div className="divide-y divide-gray-100">
          {items.map((item) => (
            <div
              key={item.item_id}
              className="flex justify-between py-2 text-sm"
            >
              <span className="text-gray-700">
                {item.quantity}× {item.name}
              </span>
              <span className="font-medium text-gray-900">
                ${(item.price * item.quantity).toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Add a tip</h2>
        <div className="flex gap-2 flex-wrap">
          {[0, 1, 2, 3, 5].map((t) => (
            <button
              key={t}
              onClick={() => {
                setTip(t);
                setCustomTip("");
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                customTip === "" && tip === t
                  ? "bg-orange-500 text-white"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              {t === 0 ? "No tip" : `$${t}`}
            </button>
          ))}
          <input
            type="number"
            min="0"
            step="0.01"
            placeholder="Custom"
            value={customTip}
            onChange={(e) => setCustomTip(e.target.value)}
            className="w-24 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          Customer ID
        </h2>
        <input
          type="text"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          placeholder="Enter your customer ID"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
      </div>

      <div className="bg-gray-50 rounded-xl border border-gray-200 p-5 mb-6 text-sm space-y-2">
        <div className="flex justify-between text-gray-600">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Tax (10%)</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Delivery fee</span>
          <span>${DELIVERY_FEE.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Tip</span>
          <span>${tipAmount.toFixed(2)}</span>
        </div>
        <div className="flex justify-between font-bold text-gray-900 text-base pt-2 border-t border-gray-200">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {error}
        </div>
      )}

      <button
        onClick={placeOrder}
        disabled={placing}
        className="w-full bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition-colors"
      >
        {placing ? "Placing order…" : `Place order · $${total.toFixed(2)}`}
      </button>
    </div>
  );
}
