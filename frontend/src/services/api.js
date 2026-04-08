const BASE = "/api";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  getOrders: () => apiFetch("/order/"),
  getUserOrders: (userId) =>
    apiFetch("/order/").then((orders) =>
      orders.filter((o) => o.customer_id === userId),
    ),
  getUser: (userId) => apiFetch(`/user/${userId}`),
  getUsers: () => apiFetch("/user/"),
  getRestaurants: () => apiFetch("/restaurant/"),
  getAdminStats: () => apiFetch("/admin/stats"),
  updateOrder: (orderId, data) =>
    apiFetch(`/order/${orderId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  updateRestaurant: (restaurantId, data) =>
    apiFetch(`/restaurant/${restaurantId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  getCategories: () => apiFetch("/menuitem/categories"),
  searchRestaurants: async ({
    query = "",
    price_category = "",
    category = "",
    page = 1,
    limit = 12,
  }) => {
    const skip = (page - 1) * limit;
    const params = new URLSearchParams();
    if (query) params.append("query", query);
    if (price_category) params.append("price_category", price_category);
    if (category) params.append("category", category);
    params.append("skip", skip);
    params.append("limit", limit);
    const queryString = params.toString();
    const url = `/search/?${queryString}`;
    const data = await apiFetch(url);
    return {
      items: data.items.map((restaurant) => ({
        ...restaurant,
        id: restaurant.restaurant_id,
      })),
      total: data.total,
    };
  },
  getRestaurant: (id) => apiFetch(`/restaurant/${id}`),
  getMenuByRestaurant: (id) => apiFetch(`/menuitem/restaurant/${id}`),
  getOrder: (orderId) => apiFetch(`/order/${orderId}`),
  createOrder: (data) =>
    apiFetch("/order/", { method: "POST", body: JSON.stringify(data) }),
  createOrderItem: (data) =>
    apiFetch("/orderitem/", { method: "POST", body: JSON.stringify(data) }),

  // Notification endpoints
  getUserNotifications: (userId) => apiFetch(`/notification/user/${userId}`),
  getNotifications: () => apiFetch("/notification/"),
  getNotification: (notificationId) =>
    apiFetch(`/notification/${notificationId}`),
  createNotification: (notification) =>
    apiFetch("/notification/", {
      method: "POST",
      body: JSON.stringify(notification),
    }),
  updateNotification: (notificationId, notification) =>
    apiFetch(`/notification/${notificationId}`, {
      method: "PUT",
      body: JSON.stringify(notification),
    }),
  deleteNotification: (notificationId) =>
    apiFetch(`/notification/${notificationId}`, { method: "DELETE" }),
  getBadgeStatus: (userId) => apiFetch(`/notification/badge/${userId}`),
  createOrderNotification: (userId, orderId) =>
    apiFetch(`/notification/order/${userId}/${orderId}`, { method: "POST" }),
  createOrderPickupNotification: (userId, orderId) =>
    apiFetch(`/notification/order-pickup/${userId}/${orderId}`, {
      method: "POST",
    }),
  createOrderDeliveryNotification: (userId, orderId) =>
    apiFetch(`/notification/order-delivery/${userId}/${orderId}`, {
      method: "POST",
    }),
  createOrderStatusCustomerNotification: (userId, orderId, status) =>
    apiFetch(
      `/notification/order-status-customer/${userId}/${orderId}/${status}`,
      { method: "POST" },
    ),
  createOrderStatusRestaurantNotification: (userId, orderId, status) =>
    apiFetch(
      `/notification/order-status-restaurant/${userId}/${orderId}/${status}`,
      { method: "POST" },
    ),
  createPaymentStatusCustomerNotification: (
    userId,
    paymentId,
    orderId,
    status,
  ) =>
    apiFetch(
      `/notification/payment-status-customer/${userId}/${paymentId}/${orderId}/${status}`,
      { method: "POST" },
    ),
};
