import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api"; // Ensure this path matches where your api.js is located

export default function NotificationPage({ userId }) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeAnimation, setActiveAnimation] = useState(null);

  // Fetch only THIS user's notifications
  const fetchNotifications = async () => {
    if (!userId) {
      setLoading(false);
      return; 
    }

    try {
      setLoading(true);
      // Calls the new endpoint: /api/notification/user/{userId}
      const data = await api.getUserNotifications(userId);
      setNotifications(data || []);
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  // Re-run the fetch if the userId changes (e.g., someone logs in/out)
  useEffect(() => {
    fetchNotifications();
  }, [userId]);

  const getIcon = (type) => {
    // Handling potential variations in type naming from the backend
    switch (type?.toLowerCase()) {
      case "order_update": 
      case "order": return "🍔";
      case "badge": return "🏆";
      case "promo": return "🎉";
      default: return "👋";
    }
  };

  // Mark a single notification as read in the database
  const markAsRead = async (notification) => {
    const id = notification.id || notification.notification_id;
    const isUnread = notification.unread !== undefined ? notification.unread : !notification.is_read;
    
    if (!isUnread) return; // Skip if already read

    try {
      // Send the update to the backend
      await api.updateNotification(id, { 
        ...notification, 
        unread: false,
        is_read: true 
      });
      
      // Update local React state instantly for a snappy UI
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

  // Mark all unread notifications as read
  const handleMarkAllAsRead = async () => {
    const unreadNotifs = notifications.filter(n => n.unread || !n.is_read);
    if (unreadNotifs.length === 0) return;

    try {
      // Execute all update API calls concurrently
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
      // Refresh the list from the server just to be perfectly in sync
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark all as read:", error);
    }
  };

  // Triggers the animation and marks as read
  const handleNotificationClick = (notif) => {
    markAsRead(notif);

    if (activeAnimation) return; // Prevent overlapping animations
    setActiveAnimation(notif.type?.toLowerCase().includes("order") ? "order" : notif.type?.toLowerCase() || "system");

    // Clear the animation after it finishes (1.5 seconds)
    setTimeout(() => {
      setActiveAnimation(null);
    }, 1500);
  };

  // UI States
  if (!userId) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <p className="text-gray-500">Please log in to view your notifications.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <div className="animate-spin text-4xl mb-4">⏳</div>
        <p className="text-gray-500">Loading your notifications...</p>
      </div>
    );
  }

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
          <p className="text-gray-500 mt-1">Stay updated on your orders and rewards.</p>
        </div>
        <button 
          onClick={handleMarkAllAsRead}
          className="text-sm font-medium text-orange-500 hover:text-orange-600 bg-orange-50 px-4 py-2 rounded-md transition-colors"
        >
          Mark all as read
        </button>
      </div>

      {/* Notifications List */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        {notifications.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {notifications.map((notif) => {
              // Normalize data fields from the backend
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
