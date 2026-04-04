import { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import { getAllBadgesWithStatus } from "../services/badgeService";
import BadgeCard from "../components/BadgeCard";

const STORAGE_KEY = "quickbite_user_id";

export default function BadgesPage() {
  const [userId, setUserId] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? "",
  );
  const [input, setInput] = useState(userId);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchOrders = useCallback(async (id) => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.getUserOrders(id);
      setOrders(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders(userId);
  }, [userId, fetchOrders]);

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    localStorage.setItem(STORAGE_KEY, trimmed);
    setUserId(trimmed);
  }

  const badges = getAllBadgesWithStatus(orders);
  const earned = badges.filter((b) => b.unlocked);
  const locked = badges.filter((b) => !b.unlocked);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Achievements</h1>
        <p className="text-gray-500 mt-1">
          Earn badges by reaching milestones on your order history.
        </p>
      </div>

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
            }}
            className="text-sm text-gray-400 hover:text-gray-600 px-2"
          >
            Clear
          </button>
        )}
      </form>

      {/* Stats bar */}
      {userId && !loading && !error && (
        <div className="flex items-center gap-6 mb-8 p-4 bg-orange-50 border border-orange-100 rounded-xl">
          <div>
            <p className="text-2xl font-bold text-orange-500">
              {earned.length}
            </p>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Earned
            </p>
          </div>
          <div className="w-px h-10 bg-orange-200" />
          <div>
            <p className="text-2xl font-bold text-gray-400">{locked.length}</p>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Locked
            </p>
          </div>
          <div className="w-px h-10 bg-orange-200" />
          <div className="flex-1">
            <div className="flex justify-between text-xs text-gray-500 mb-1">
              <span>Overall progress</span>
              <span>
                {earned.length}/{badges.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-orange-500 h-2.5 rounded-full transition-all duration-700"
                style={{
                  width: `${Math.round((earned.length / badges.length) * 100)}%`,
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Loading / Error / Empty states */}
      {loading && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-4xl mb-3 animate-spin inline-block">⏳</div>
          <p>Loading your achievements…</p>
        </div>
      )}

      {error && (
        <div className="text-center py-10 text-red-500 bg-red-50 rounded-xl">
          <p className="font-medium">Failed to load orders</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}

      {!loading && !error && !userId && (
        <div className="text-center py-16 text-gray-400">
          <p className="text-5xl mb-4">🏆</p>
          <p className="text-lg font-medium text-gray-600">
            Enter your customer ID to see your badges
          </p>
          <p className="text-sm mt-1">
            Your achievements are tracked automatically from your order history.
          </p>
        </div>
      )}

      {/* Badge grid */}
      {!loading && !error && userId && (
        <>
          {earned.length > 0 && (
            <section className="mb-10">
              <h2 className="text-lg font-semibold text-gray-700 mb-4">
                Earned ({earned.length})
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {earned.map((badge) => (
                  <BadgeCard key={badge.id} badge={badge} />
                ))}
              </div>
            </section>
          )}

          {locked.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-700 mb-4">
                Locked ({locked.length})
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {locked.map((badge) => (
                  <BadgeCard key={badge.id} badge={badge} />
                ))}
              </div>
            </section>
          )}

          {orders.length === 0 && (
            <p className="text-center text-gray-400 py-8">
              No orders found for this customer ID. Place an order to start
              earning badges!
            </p>
          )}
        </>
      )}

      {/* Profile link */}
      {userId && (
        <div className="mt-10 text-center">
          <Link
            to="/profile"
            className="text-sm text-orange-500 hover:text-orange-600 underline underline-offset-2"
          >
            View your profile →
          </Link>
        </div>
      )}
    </div>
  );
}
