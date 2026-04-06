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
  getCategories: () => apiFetch("/menuitem/categories"),

  searchRestaurants: async ({ query = "", price_category = "", category = "" }) => {
    const params = new URLSearchParams();
    if (query) params.append("query", query);
    if (price_category) params.append("price_category", price_category);
    if (category) params.append("category", category);

    const queryString = params.toString();
    const url = `/search/${queryString ? `?${queryString}` : ""}`;
    
    const data = await apiFetch(url);
    
    return data.map(restaurant => ({
      ...restaurant,
      id: restaurant.restaurant_id
    }));
  },
  getRestaurant: (id) => apiFetch(`/restaurant/${id}`),
  getMenuByRestaurant: (id) => apiFetch(`/menuitem/restaurant/${id}`),
};
