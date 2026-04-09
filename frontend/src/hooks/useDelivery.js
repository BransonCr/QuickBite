import { useState, useEffect, useCallback } from "react";
import { deliveryService } from "../services/deliveryService";

export function useDelivery(orderId = null) {
  const [delivery, setDelivery] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchByOrder = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/delivery/order/${id}`);
      if (res.status === 404) {
        setDelivery(null); 
        return;
      }
      if (!res.ok) throw new Error("Failed to fetch delivery for order");
      const data = await res.json();
      setDelivery(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateStatus = useCallback(async (deliveryId, status) => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`/api/delivery/${deliveryId}/status`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(res.status === 401 ? "Not authorized — please log in as admin" : JSON.stringify(err.detail));
      }
      const updated = await res.json();
      setDelivery(updated);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    if (orderId) fetchByOrder(orderId);
  }, [orderId, fetchByOrder]);

  return { delivery, loading, error, fetchByOrder, updateStatus };
}