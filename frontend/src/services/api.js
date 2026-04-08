const BASE = "/api";

function getToken() {
  return localStorage.getItem("token");
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // --- Auth ---
  login: async (username, password) => {
    const res = await fetch(`${BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username, password }),
    });
    if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
    return res.json();
  },
  register: (data) =>
    apiFetch("/auth/register", { method: "POST", body: JSON.stringify(data) }),
  forgotPassword: (email) =>
    apiFetch("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
  resetPassword: (token, new_password) =>
    apiFetch("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token, new_password }),
    }),

  // --- Users ---
  getUsers: () => apiFetch("/user/"),
  getUser: (userId) => apiFetch(`/user/${userId}`),
  createUser: (data) =>
    apiFetch("/user/", { method: "POST", body: JSON.stringify(data) }),
  updateUser: (userId, data) =>
    apiFetch(`/user/${userId}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteUser: (userId) => apiFetch(`/user/${userId}`, { method: "DELETE" }),

  // --- Orders ---
  getOrders: () => apiFetch("/order/"),
  getUserOrders: (userId) =>
    apiFetch("/order/").then((orders) =>
      orders.filter((o) => o.customer_id === userId),
    ),
  getOrder: (orderId) => apiFetch(`/order/${orderId}`),
  createOrder: (data) =>
    apiFetch("/order/", { method: "POST", body: JSON.stringify(data) }),
  createOrderItem: (data) =>
    apiFetch("/orderitem/", { method: "POST", body: JSON.stringify(data) }),
  updateOrder: (orderId, data) =>
    apiFetch(`/order/${orderId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // --- Restaurants ---
  getRestaurants: () => apiFetch("/restaurant/"),
  getRestaurant: (id) => apiFetch(`/restaurant/${id}`),
  updateRestaurant: (restaurantId, data) =>
    apiFetch(`/restaurant/${restaurantId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // --- Menu ---
  getCategories: () => apiFetch("/menuitem/categories"),
  getMenuByRestaurant: (id) => apiFetch(`/menuitem/restaurant/${id}`),
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
    const data = await apiFetch(`/search/?${params.toString()}`);
    return {
      items: data.items.map((restaurant) => ({
        ...restaurant,
        id: restaurant.restaurant_id,
      })),
      total: data.total,
    };
  },

  // --- Admin ---
  getAdminStats: () => apiFetch("/admin/stats"),

  // --- Notifications ---
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
