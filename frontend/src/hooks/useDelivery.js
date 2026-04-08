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
      const data = await deliveryService.getDeliveryByOrder(id);
      setDelivery(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateStatus = useCallback(async (deliveryId, status) => {
    try {
      const updated = await deliveryService.updateDeliveryStatus(deliveryId, status);
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