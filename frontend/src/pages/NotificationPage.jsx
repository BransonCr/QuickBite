import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api"; // Ensure this path matches where your api.js is located

export default function NotificationPage() {
  // New states for handling manual User ID entry
  const [inputUserId, setInputUserId] = useState("");
  const [activeUserId, setActiveUserId] = useState(null);

  // Existing states
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeAnimation, setActiveAnimation] = useState(null);

  // Fetch only THIS user's notifications based on the manually entered ID
  const fetchNotifications = async () => {
    if (!activeUserId) {
      setLoading(false);
      return; 
    }

    try {
      setLoading(true);
      const data = await api.getUserNotifications(activeUserId);
      setNotifications(data || []);
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  // Re-run the fetch if the activeUserId changes
  useEffect(() => {
    if (activeUserId) {
      fetchNotifications();
    }
  }, [activeUserId]);

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    if (inputUserId.trim()) {
      setActiveUserId(inputUserId.trim());
    }
  };

  const handleLogout = () => {
    setActiveUserId(null);
    setInputUserId("");
    setNotifications([]);
  };

  const getIcon = (type) => {
    switch (type?.toLowerCase()) {
      case "order_update": 
      case "order": return "🍔";
      case "badge": return "🏆";
      case "promo": return "🎉";
      default: return "👋";
    }
  };

  const markAsRead = async (notification) => {
    const id = notification.id || notification.notification_id;
    const isUnread = notification.unread !== undefined ? notification.unread : !notification.is_read;
    
    if (!isUnread) return;

    try {
      await api.updateNotification(id, { 
        ...notification, 
        unread: false,
        is_read: true 
      });
      
      setNotifications((prev) => 
        prev.map((n) => 
          (n.id || n.notification_id) === id 
            ? { ...n, unread: false, is_read: true } 
            : n
        )
      );
    } catch (error) {
      console.error("Failed to mark notification as read:", error);
    }
  };

  const handleMarkAllAsRead = async () => {
    const unreadNotifs = notifications.filter(n => n.unread || !n.is_read);
    if (unreadNotifs.length === 0) return;

    try {
      await Promise.all(
        unreadNotifs.map(notif => {
          const id = notif.id || notif.notification_id;
          return api.updateNotification(id, { 
            ...notif, 
            unread: false, 
            is_read: true 
          });
        })
      );
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark all as read:", error);
    }
  };

  const handleNotificationClick = (notif) => {
    markAsRead(notif);

    if (activeAnimation) return;
    setActiveAnimation(notif.type?.toLowerCase().includes("order") ? "order" : notif.type?.toLowerCase() || "system");

    setTimeout(() => {
      setActiveAnimation(null);
    }, 1500);
  };

  // --- UI STATE 1: Prompt for User ID ---
  if (!activeUserId) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <div className="bg-white p-8 shadow-sm rounded-lg border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">View Notifications</h2>
          <p className="text-gray-500 mb-6">Enter your User ID to see your updates.</p>
          
          <form onSubmit={handleLoginSubmit} className="flex flex-col gap-4">
            <input 
              type="text" 
              placeholder="e.g. 166204c2-..."
              value={inputUserId}
              onChange={(e) => setInputUserId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
            <button 
              type="submit"
              className="w-full bg-orange-500 text-white font-medium py-2 rounded-md hover:bg-orange-600 transition-colors"
            >
              Fetch Notifications
            </button>
          </form>
        </div>
      </div>
    );
  }

  // --- UI STATE 2: Loading Notifications ---
  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <div className="animate-spin text-4xl mb-4">⏳</div>
        <p className="text-gray-500">Loading notifications for {activeUserId}...</p>
      </div>
    );
  }

  // --- UI STATE 3: Display Notifications ---
  return (
    <div className="max-w-3xl mx-auto px-4 py-8 relative">
      
      {/* --- CUSTOM CSS ANIMATIONS --- */}
      <style>
        {`
          @keyframes zoomAcross {
            0% { transform: translateX(-100vw) scale(2); opacity: 1; }
            100% { transform: translateX(100vw) scale(2); opacity: 1; }
          }
          @keyframes popIn {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(4) rotate(10deg); opacity: 1; }
            100% { transform: scale(0); opacity: 0; }
          }
          @keyframes rainDown {
            0% { transform: translateY(-50vh) scale(2); opacity: 1; }
            100% { transform: translateY(100vh) scale(2); opacity: 0; }
          }
        `}
      </style>

      {/* --- ANIMATION OVERLAY --- */}
      {activeAnimation && (
        <div className="fixed inset-0 pointer-events-none flex items-center justify-center z-50 overflow-hidden">
          {activeAnimation.includes("order") && (
            <div className="text-8xl" style={{ animation: "zoomAcross 1.5s ease-in-out forwards" }}>🛵💨</div>
          )}
          {activeAnimation === "badge" && (
            <div className="text-8xl drop-shadow-2xl" style={{ animation: "popIn 1.2s ease-in-out forwards" }}>🏆✨</div>
          )}
          {activeAnimation === "promo" && (
            <div className="flex gap-8 text-6xl" style={{ animation: "rainDown 1.5s ease-in forwards" }}>
              <span>🎉</span><span>💸</span><span>🍔</span><span>🎉</span>
            </div>
          )}
          {(!activeAnimation.includes("order") && !["badge", "promo"].includes(activeAnimation)) && (
            <div className="text-8xl animate-spin transition-opacity duration-1000 opacity-0">👋</div>
          )}
        </div>
      )}

      {/* Header Section */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
          <p className="text-gray-500 mt-1">ID: <span className="font-mono text-xs">{activeUserId}</span></p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={handleLogout}
            className="text-sm font-medium text-gray-600 hover:text-gray-900 px-4 py-2 rounded-md transition-colors"
          >
            Change User
          </button>
          <button 
            onClick={handleMarkAllAsRead}
            className="text-sm font-medium text-orange-500 hover:text-orange-600 bg-orange-50 px-4 py-2 rounded-md transition-colors"
          >
            Mark all as read
          </button>
        </div>
      </div>

      {/* Notifications List */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        {notifications.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {notifications.map((notif) => {
              const id = notif.id || notif.notification_id;
              const isUnread = notif.unread !== undefined ? notif.unread : !notif.is_read; 
              const title = notif.title || (notif.type === "order_update" ? "Order Update" : "Notification");
              const message = notif.description || notif.message;
              const timeDisplay = notif.time || (notif.created_at && new Date(notif.created_at).toLocaleString()) || "Just now";

              return (
                <li 
                  key={id} 
                  onClick={() => handleNotificationClick(notif)}
                  className={`p-5 hover:bg-gray-50 transition-colors cursor-pointer ${isUnread ? 'bg-orange-50/30' : 'bg-white'}`}
                >
                  <div className="flex gap-4 pointer-events-none">
                    {/* Icon */}
                    <div className="flex-shrink-0 mt-1 text-2xl">
                      {getIcon(notif.type)}
                    </div>
                    
                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-gray-900 flex items-center gap-2">
                        {title}
                        {isUnread && (
                          <span className="inline-block h-2 w-2 rounded-full bg-red-500"></span>
                        )}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {message}
                      </p>
                      <p className="text-xs text-gray-400 mt-2 font-medium">
                        {timeDisplay}
                      </p>
                    </div>

                    {/* Optional Action Buttons */}
                    {notif.type?.toLowerCase() === "promo" && (
                      <div className="flex-shrink-0 self-center pointer-events-auto">
                        <Link 
                          to="/spin" 
                          onClick={(e) => e.stopPropagation()}
                          className="text-sm font-medium text-orange-500 hover:text-orange-600 bg-orange-50 px-3 py-1 rounded"
                        >
                          Go to Spin
                        </Link>
                      </div>
                    )}
                    {(notif.type?.toLowerCase() === "badge" || notif.badge) && (
                      <div className="flex-shrink-0 self-center pointer-events-auto">
                        <Link 
                          to="/badges" 
                          onClick={(e) => e.stopPropagation()}
                          className="text-sm font-medium text-orange-500 hover:text-orange-600 bg-orange-50 px-3 py-1 rounded"
                        >
                          View Badges
                        </Link>
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        ) : (
          <div className="py-12 text-center">
            <p className="text-4xl mb-3">📭</p>
            <h3 className="text-lg font-medium text-gray-900">No notifications yet</h3>
            <p className="text-gray-500 mt-1">When you get updates, they'll show up here.</p>
          </div>
        )}
      </div>
    </div>
  );
}
