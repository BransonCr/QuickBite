import { useState, useEffect, useCallback } from "react";
import { api } from "../services/api";

const STATUS_COLORS = {
  CART: "bg-gray-100 text-gray-600",
  PENDING: "bg-yellow-100 text-yellow-700",
  CONFIRMED: "bg-blue-100 text-blue-700",
  IN_PREPARATION: "bg-purple-100 text-purple-700",
  OUT_FOR_DELIVERY: "bg-orange-100 text-orange-700",
  DELIVERED: "bg-green-100 text-green-700",
  CANCELLED: "bg-red-100 text-red-600",
};

const ROLE_COLORS = {
  ADMIN: "bg-red-100 text-red-700",
  CUSTOMER: "bg-blue-100 text-blue-700",
  DELIVERY_DRIVER: "bg-orange-100 text-orange-700",
  RESTAURANT_OWNER: "bg-purple-100 text-purple-700",
};

const ORDER_STATUSES = [
  "CART",
  "PENDING",
  "CONFIRMED",
  "IN_PREPARATION",
  "OUT_FOR_DELIVERY",
  "DELIVERED",
  "CANCELLED",
];

function StatCard({ label, value, sub }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      <p className="text-sm font-medium text-gray-700 mt-1">{label}</p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  );
}

function Badge({ label, colorClass }) {
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${colorClass}`}
    >
      {label}
    </span>
  );
}

function BarChart({ data, total }) {
  return (
    <div className="space-y-2">
      {Object.entries(data).map(([key, count]) => {
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        return (
          <div key={key} className="flex items-center gap-3">
            <span className="w-36 text-xs text-gray-500 truncate">{key}</span>
            <div className="flex-1 bg-gray-100 rounded-full h-2">
              <div
                className="bg-orange-400 h-2 rounded-full transition-all duration-500"
                style={{ width: `${pct}%` }}
              />
            </div>
            <span className="w-8 text-right text-xs text-gray-500">
              {count}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function OrdersTab({ orders, onStatusChange }) {
  const [filter, setFilter] = useState("ALL");
  const [updating, setUpdating] = useState(null);

  const visible =
    filter === "ALL" ? orders : orders.filter((o) => o.status === filter);

  async function handleStatusChange(orderId, newStatus) {
    setUpdating(orderId);
    try {
      await onStatusChange(orderId, newStatus);
    } finally {
      setUpdating(null);
    }
  }

  return (
    <div>
      <div className="flex gap-2 flex-wrap mb-4">
        {["ALL", ...ORDER_STATUSES].map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
              filter === s
                ? "bg-orange-500 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {s}
          </button>
        ))}
      </div>
      <div className="overflow-x-auto rounded-xl border border-gray-200">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide">
            <tr>
              <th className="px-4 py-3 text-left">Order ID</th>
              <th className="px-4 py-3 text-left">Customer</th>
              <th className="px-4 py-3 text-left">Restaurant</th>
              <th className="px-4 py-3 text-right">Total</th>
              <th className="px-4 py-3 text-left">Status</th>
              <th className="px-4 py-3 text-left">Update</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {visible.map((o) => (
              <tr key={o.order_id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-mono text-xs text-gray-500">
                  {o.order_id.slice(0, 8)}…
                </td>
                <td className="px-4 py-3 font-mono text-xs text-gray-500">
                  {o.customer_id.slice(0, 8)}…
                </td>
                <td className="px-4 py-3 font-mono text-xs text-gray-500">
                  {o.restaurant_id.slice(0, 8)}…
                </td>
                <td className="px-4 py-3 text-right font-medium">
                  ${o.total.toFixed(2)}
                </td>
                <td className="px-4 py-3">
                  <Badge
                    label={o.status}
                    colorClass={
                      STATUS_COLORS[o.status] ?? "bg-gray-100 text-gray-600"
                    }
                  />
                </td>
                <td className="px-4 py-3">
                  <select
                    disabled={updating === o.order_id}
                    defaultValue={o.status}
                    onChange={(e) =>
                      handleStatusChange(o.order_id, e.target.value)
                    }
                    className="border border-gray-200 rounded-md px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:opacity-50"
                  >
                    {ORDER_STATUSES.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
            {visible.length === 0 && (
              <tr>
                <td
                  colSpan={6}
                  className="px-4 py-8 text-center text-gray-400 text-sm"
                >
                  No orders found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function UsersTab({ users }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide">
          <tr>
            <th className="px-4 py-3 text-left">Username</th>
            <th className="px-4 py-3 text-left">Email</th>
            <th className="px-4 py-3 text-left">Phone</th>
            <th className="px-4 py-3 text-left">Role</th>
            <th className="px-4 py-3 text-left">Location</th>
            <th className="px-4 py-3 text-left">Joined</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {users.map((u) => (
            <tr key={u.user_id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-gray-900">
                {u.username}
              </td>
              <td className="px-4 py-3 text-gray-500">{u.email}</td>
              <td className="px-4 py-3 text-gray-500">{u.phone}</td>
              <td className="px-4 py-3">
                <Badge
                  label={u.role}
                  colorClass={
                    ROLE_COLORS[u.role] ?? "bg-gray-100 text-gray-600"
                  }
                />
              </td>
              <td className="px-4 py-3 text-gray-500">{u.location}</td>
              <td className="px-4 py-3 text-gray-400 text-xs">
                {u.created_at?.slice(0, 10) ?? "—"}
              </td>
            </tr>
          ))}
          {users.length === 0 && (
            <tr>
              <td
                colSpan={6}
                className="px-4 py-8 text-center text-gray-400 text-sm"
              >
                No users found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function RestaurantsTab({ restaurants, onToggleActive }) {
  const [toggling, setToggling] = useState(null);

  async function handleToggle(r) {
    setToggling(r.restaurant_id);
    try {
      await onToggleActive(r.restaurant_id, !r.is_active);
    } finally {
      setToggling(null);
    }
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide">
          <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Location</th>
            <th className="px-4 py-3 text-left">Hours</th>
            <th className="px-4 py-3 text-left">Radius</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-left">Toggle</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {restaurants.map((r) => (
            <tr key={r.restaurant_id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-gray-900">{r.name}</td>
              <td className="px-4 py-3 text-gray-500">{r.location}</td>
              <td className="px-4 py-3 text-gray-500 text-xs">
                {r.operating_hours}
              </td>
              <td className="px-4 py-3 text-gray-500">
                {r.delivery_radius} km
              </td>
              <td className="px-4 py-3">
                <Badge
                  label={r.is_active ? "Active" : "Inactive"}
                  colorClass={
                    r.is_active
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-600"
                  }
                />
              </td>
              <td className="px-4 py-3">
                <button
                  disabled={toggling === r.restaurant_id}
                  onClick={() => handleToggle(r)}
                  className={`px-3 py-1 rounded-md text-xs font-medium transition-colors disabled:opacity-50 ${
                    r.is_active
                      ? "bg-red-50 text-red-600 hover:bg-red-100"
                      : "bg-green-50 text-green-700 hover:bg-green-100"
                  }`}
                >
                  {r.is_active ? "Deactivate" : "Activate"}
                </button>
              </td>
            </tr>
          ))}
          {restaurants.length === 0 && (
            <tr>
              <td
                colSpan={6}
                className="px-4 py-8 text-center text-gray-400 text-sm"
              >
                No restaurants found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function PaymentsTab({ payments, onStatusChange, onDelete }) {
  const getStatusColor = (status) => {
    switch (status) {
      case "SUCCESS": return "bg-green-100 text-green-700";
      case "FAILED": return "bg-red-100 text-red-600";
      default: return "bg-yellow-100 text-yellow-700"; // PENDING
    }
  };

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide">
          <tr>
            <th className="px-4 py-3 text-left">Payment ID</th>
            <th className="px-4 py-3 text-left">Order ID</th>
            <th className="px-4 py-3 text-right">Amount</th>
            <th className="px-4 py-3 text-left">Card</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-left">Update</th>
            <th className="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {payments.map((p) => (
            <tr key={p.payment_id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-mono text-xs text-gray-500">
                {p.payment_id.slice(0, 8)}…
              </td>
              <td className="px-4 py-3 font-mono text-xs text-gray-400">
                {p.order_id.slice(0, 8)}…
              </td>
              <td className="px-4 py-3 text-right font-bold text-gray-900">
                ${p.amount.toFixed(2)}
              </td>
              <td className="px-4 py-3 text-gray-500">
                •••• {p.card_number.slice(-4)}
              </td>
              <td className="px-4 py-3">
                <Badge label={p.status} colorClass={getStatusColor(p.status)} />
              </td>
              <td className="px-4 py-3">
                <select
                  value={p.status}
                  disabled={p.status === "SUCCESS"}
                  onChange={(e) => onStatusChange(p.payment_id, e.target.value)}
                  className="border border-gray-200 rounded-md px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-orange-400"
                >
                  <option value="PENDING">PENDING</option>
                  <option value="SUCCESS">SUCCESS</option>
                  <option value="FAILED">FAILED</option>
                </select>
              </td>
              <td className="px-4 py-3 text-right">
                <button
                  onClick={() => onDelete(p.payment_id)}
                  disabled={p.status === "SUCCESS"}
                  className="text-red-500 hover:text-red-700 text-xs font-bold disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:text-red-500 transition-opacity"
                  title={p.status === "SUCCESS" ? "Cannot delete completed payments" : "Delete Payment"}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
          {payments.length === 0 && (
            <tr>
              <td colSpan={7} className="px-4 py-8 text-center text-gray-400 text-sm">
                No payments found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default function AdminPage() {
  const [tab, setTab] = useState("overview");
  const [stats, setStats] = useState(null);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsData, ordersData, usersData, restaurantsData, paymentsData] =
        await Promise.all([
          api.getAdminStats(),
          api.getOrders(),
          api.getUsers(),
          api.getRestaurants(),
          api.getPayments(),
        ]);
      setStats(statsData);
      setOrders(ordersData);
      setUsers(usersData);
      setRestaurants(restaurantsData);
      setPayments(paymentsData);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function handleStatusChange(orderId, newStatus) {
    await api.updateOrder(orderId, { status: newStatus });
    setOrders((prev) =>
      prev.map((o) =>
        o.order_id === orderId ? { ...o, status: newStatus } : o,
      ),
    );
  }

  async function handleToggleActive(restaurantId, isActive) {
    await api.updateRestaurant(restaurantId, { is_active: isActive });
    setRestaurants((prev) =>
      prev.map((r) =>
        r.restaurant_id === restaurantId ? { ...r, is_active: isActive } : r,
      ),
    );
  }

  async function handlePaymentStatusChange(paymentId, newStatus) {
    try {
      await api.updatePayment(paymentId, { status: newStatus });
      setPayments((prev) =>
        prev.map((p) => (p.payment_id === paymentId ? { ...p, status: newStatus } : p))
      );
    }catch (e) {
      alert("Failed to update payment status: " + (e.message || e));
    }
  }

  async function handleDeletePayment(paymentId) {
    if (!window.confirm("Delete this payment record?")) return;
    await api.deletePayment(paymentId);
    setPayments((prev) => prev.filter((p) => p.payment_id !== paymentId));
  }

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "orders", label: `Orders (${orders.length})` },
    { id: "users", label: `Users (${users.length})` },
    { id: "restaurants", label: `Restaurants (${restaurants.length})` },
    { id: "payments", label: `Payments (${payments.length})` },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-500 mt-1">Platform overview and management</p>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
        >
          {loading ? "Loading…" : "Refresh"}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
          {error}
        </div>
      )}

      {loading && !stats && (
        <div className="text-center py-24 text-gray-400">
          <div className="text-4xl mb-3 animate-spin inline-block">⏳</div>
          <p>Loading dashboard…</p>
        </div>
      )}

      {stats && (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            <StatCard label="Total Users" value={stats.users_count} />
            <StatCard label="Total Orders" value={stats.orders_count} />
            <StatCard
              label="Restaurants"
              value={stats.restaurants_count}
              sub={`${stats.active_restaurants} active`}
            />
            <StatCard
              label="Revenue"
              value={`$${stats.total_revenue.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              sub="Delivered orders"
            />
            <StatCard 
              label="Payment Vol." 
              value={`$${stats.total_payment_volume.toLocaleString()}`} 
              sub="Captured success" 
            />
          </div>

          <div className="flex gap-1 mb-6 border-b border-gray-200">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px ${
                  tab === t.id
                    ? "border-orange-500 text-orange-500"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {tab === "overview" && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl border border-gray-200 p-5">
                <h2 className="text-sm font-semibold text-gray-700 mb-4">
                  Orders by Status
                </h2>
                <BarChart
                  data={stats.orders_by_status}
                  total={stats.orders_count}
                />
              </div>
              <div className="bg-white rounded-xl border border-gray-200 p-5">
                <h2 className="text-sm font-semibold text-gray-700 mb-4">
                  Users by Role
                </h2>
                <BarChart
                  data={stats.users_by_role}
                  total={stats.users_count}
                />
              </div>
            </div>
          )}

          {tab === "orders" && (
            <OrdersTab orders={orders} onStatusChange={handleStatusChange} />
          )}

          {tab === "users" && <UsersTab users={users} />}

          {tab === "restaurants" && (
            <RestaurantsTab
              restaurants={restaurants}
              onToggleActive={handleToggleActive}
            />
          )}

          {tab === "payments" && (
            <PaymentsTab 
              payments={payments} 
              onStatusChange={handlePaymentStatusChange} 
              onDelete={handleDeletePayment} 
            />
          )}
        </>
      )}
    </div>
  );
}
