import { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import {
  getRecentlyEarnedBadges,
  getAllBadgesWithStatus,
  formatEarnedDate,
} from "../services/badgeService";

const STORAGE_KEY = "quickbite_user_id";

function StatCard({ label, value }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 text-center">
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500 uppercase tracking-wide mt-1">
        {label}
      </p>
    </div>
  );
}

function MiniBadge({ badge }) {
  const dateLabel = formatEarnedDate(badge.earnedAt);
  return (
    <div className="flex items-center gap-3 bg-green-50 border border-green-200 rounded-xl p-4">
      <span className="text-3xl select-none">{badge.icon}</span>
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-gray-900 text-sm">{badge.name}</p>
        <p className="text-xs text-gray-500 truncate">{badge.description}</p>
        {dateLabel && (
          <p className="text-xs text-green-500 mt-0.5">Earned {dateLabel}</p>
        )}
      </div>
      <span className="flex items-center justify-center w-6 h-6 rounded-full bg-green-500 text-white text-xs font-bold flex-shrink-0">
        ✓
      </span>
    </div>
  );
}

export default function ProfilePage() {
  const [userId, setUserId] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? "",
  );
  const [input, setInput] = useState(userId);
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (id) => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const [userOrders, userData] = await Promise.allSettled([
        api.getUserOrders(id),
        api.getUser(id),
      ]);
      if (userOrders.status === "fulfilled") setOrders(userOrders.value);
      if (userData.status === "fulfilled") setUser(userData.value);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(userId);
  }, [userId, fetchData]);

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    localStorage.setItem(STORAGE_KEY, trimmed);
    setUserId(trimmed);
  }

  const delivered = orders.filter((o) => o.status === "DELIVERED");
  const totalSpent = delivered.reduce((s, o) => s + (o.total ?? 0), 0);
  const uniqueRestaurants = new Set(delivered.map((o) => o.restaurant_id)).size;

  const recentBadges = getRecentlyEarnedBadges(orders, 3);
  const allBadges = getAllBadgesWithStatus(orders);
  const earnedCount = allBadges.filter((b) => b.unlocked).length;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Profile</h1>

      {/* User ID form */}
      <form onSubmit={handleSubmit} className="flex gap-2 mb-8">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your customer ID"
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-600 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors"
        >
          Load
        </button>
        {userId && (
          <button
            type="button"
            onClick={() => {
              localStorage.removeItem(STORAGE_KEY);
              setUserId("");
              setInput("");
              setOrders([]);
              setUser(null);
            }}
            className="text-sm text-gray-400 hover:text-gray-600 px-2"
          >
            Clear
          </button>
        )}
      </form>

      {loading && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-4xl mb-3 animate-spin inline-block">⏳</div>
          <p>Loading profile…</p>
        </div>
      )}

      {!loading && !userId && (
        <div className="text-center py-16 text-gray-400">
          <p className="text-5xl mb-4">👤</p>
          <p className="text-lg font-medium text-gray-600">
            Enter your customer ID to view your profile
          </p>
        </div>
      )}

      {!loading && userId && (
        <>
          {/* User info card */}
          <div className="bg-white border border-gray-200 rounded-xl p-5 mb-6 flex items-center gap-4">
            <div className="w-14 h-14 rounded-full bg-orange-100 flex items-center justify-center text-2xl select-none flex-shrink-0">
              👤
            </div>
            <div className="min-w-0">
              {user ? (
                <>
                  <p className="font-bold text-lg text-gray-900 truncate">
                    {user.username}
                  </p>
                  <p className="text-sm text-gray-500 truncate">{user.email}</p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    Member since {formatEarnedDate(user.created_at) ?? "—"}
                  </p>
                </>
              ) : (
                <>
                  <p className="font-mono text-sm text-gray-700 truncate">
                    {userId}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    Customer account
                  </p>
                </>
              )}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-3 mb-8">
            <StatCard label="Orders" value={delivered.length} />
            <StatCard label="Restaurants" value={uniqueRestaurants} />
            <StatCard label="Total spent" value={`$${totalSpent.toFixed(2)}`} />
          </div>

          {/* Recent achievements */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">
                Recent Achievements
              </h2>
              <Link
                to="/badges"
                className="text-sm text-orange-500 hover:text-orange-600 font-medium"
              >
                View all ({earnedCount}/{allBadges.length}) →
              </Link>
            </div>

            {recentBadges.length > 0 ? (
              <div className="flex flex-col gap-3">
                {recentBadges.map((badge) => (
                  <MiniBadge key={badge.id} badge={badge} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 bg-gray-50 rounded-xl border border-gray-100">
                <p className="text-3xl mb-2">🏅</p>
                <p className="text-gray-500 text-sm">No badges earned yet.</p>
                <p className="text-gray-400 text-xs mt-1">
                  Place an order to start unlocking achievements!
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
