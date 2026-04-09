export const deliveryService = {

  getAllDeliveries: async () => {
    const res = await fetch(`/api/delivery/`);
    if (!res.ok) throw new Error("Failed to fetch deliveries");
    return res.json();
  },

  createDelivery: async (payload) => {
    const res = await fetch(`/api/delivery/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create delivery");
    return res.json();
  },

  getDeliveryByOrder: async (orderId) => {
    const res = await fetch(`/api/delivery/order/${orderId}`);
    if (!res.ok) throw new Error("Failed to fetch delivery for order");
    return res.json();
  },

  getDelivery: async (deliveryId) => {
    const res = await fetch(`/api/delivery/${deliveryId}`);
    if (!res.ok) throw new Error("Failed to fetch delivery");
    return res.json();
  },

  updateDelivery: async (deliveryId, payload) => {
    const res = await fetch(`/api/delivery/${deliveryId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to update delivery");
    return res.json();
  },

  deleteDelivery: async (deliveryId) => {
    const res = await fetch(`/api/delivery/${deliveryId}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error("Failed to delete delivery");
    return res.json();
  },

  updateDeliveryStatus: async (deliveryId, status) => {
    const res = await fetch(`/api/delivery/${deliveryId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    if (!res.ok) throw new Error("Failed to update delivery status");
    return res.json();
  },
};