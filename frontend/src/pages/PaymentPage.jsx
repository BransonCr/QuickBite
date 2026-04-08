import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { api } from "../services/api";

export default function PaymentPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { orderId, subtotal, tax, deliveryFee, tip, finalTotal = 0 } = location.state || {};
  
  const { items, restaurantId, clearCart } = useCart();
  
  const [cardNumber, setCardNumber] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false); 
  const [error, setError] = useState(null);

  if (items.length === 0 || !orderId) {
    return (
      <div className="text-center py-16">
        <p>Your cart is empty or the order session expired.</p>
        <button onClick={() => navigate("/browse")} className="text-orange-500 mt-4 font-medium">
          Go back to browsing
        </button>
      </div>
    );
  }

  const handleExpiryChange = (e) => {
    let val = e.target.value.replace(/\D/g, ""); 
    if (val.length >= 3) {
      val = val.substring(0, 2) + "/" + val.substring(2, 6);
    }
    setExpiry(val.substring(0, 7)); 
  };

  async function handlePaymentSubmit(e) {
    e.preventDefault();
    setIsProcessing(true);
    setError(null);
  
    try {
      const paymentPayload = {
        order_id: orderId,
        amount: finalTotal,
        card_number: cardNumber,
        expiration_date: expiry,
        cvv: cvv
      };
  
      const pendingPayment = await api.createPayment(paymentPayload);
      
      await api.updatePayment(pendingPayment.payment_id, { status: "SUCCESS" });
  
      clearCart();
      navigate(`/order/${orderId}`, { state: location.state });
  
    } catch (err) {
      setError(err.message || "Payment failed.");
    } finally {
      setIsProcessing(false);
    }
  }

  async function handleCancelOrder() {
    setIsCancelling(true);
    setError(null);
    try {
      await api.deleteOrderItems(orderId);
      await api.deleteOrder(orderId);
      
      navigate("/checkout");
    } catch (err) {
      setError("Failed to cancel order. Please try again.");
      setIsCancelling(false);
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Secure Checkout</h1>

      <div className="bg-gray-50 p-4 rounded-xl mb-8 border border-gray-100">
        <h2 className="font-medium text-gray-700 mb-2">Total to Pay</h2>
        <p className="text-3xl font-bold text-orange-500">${finalTotal.toFixed(2)}</p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* Payment Form */}
      <form onSubmit={handlePaymentSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
          <input
            type="text"
            required
            maxLength="16"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
            placeholder="0000 0000 0000 0000"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Expiry</label>
            <input
              type="text"
              required
              placeholder="MM/YY"
              value={expiry}
              onChange={handleExpiryChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">CVV</label>
            <input
              type="text"
              required
              maxLength="3"
              placeholder="123"
              value={cvv}
              onChange={(e) => setCvv(e.target.value.replace(/\D/g, ''))}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-4 space-y-3">
          <button
            type="submit"
            // Disable if paying OR canceling
            disabled={isProcessing || isCancelling} 
            className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-xl transition-colors disabled:bg-orange-300 flex justify-center items-center gap-2"
          >
            {isProcessing ? (
              <>
                <span className="animate-spin inline-block">🔄</span> Processing...
              </>
            ) : (
              `Pay $${finalTotal.toFixed(2)}`
            )}
          </button>

          {/* 4. The Cancel Button */}
          <button
            type="button" // Important so it doesn't submit the form!
            onClick={handleCancelOrder}
            disabled={isProcessing || isCancelling}
            className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-3 rounded-xl transition-colors disabled:opacity-50 flex justify-center items-center gap-2"
          >
             {isCancelling ? (
              <>
                <span className="animate-spin inline-block">🔄</span> Canceling...
              </>
            ) : (
              "Cancel and return to cart"
            )}
          </button>
        </div>
      </form>
      
      <p className="text-center text-xs text-gray-400 mt-6">
        🔒 Payments are secure and encrypted.
      </p>
    </div>
  );
}