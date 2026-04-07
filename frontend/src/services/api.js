const BASE = "/api";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

export const api = {
  getOrders: () => apiFetch("/order/"),
  getUserOrders: (userId) =>
    apiFetch("/order/").then((orders) =>
      orders.filter((o) => o.customer_id === userId),
    ),
  getBadgeStatus: (userId) => apiFetch(`/notification/badge/${userId}`),
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
};
