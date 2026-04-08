import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function NotificationPage() {
  const [activeAnimation, setActiveAnimation] = useState(null);

  // Expanded dummy data
  const notifications = [
    { 
      id: 1, 
      type: "order", 
      title: "Your order is on the way!", 
      description: "Your QuickBite driver is 5 minutes away. Get ready to eat!",
      time: "2 minutes ago", 
      unread: true 
    },
    { 
      id: 2, 
      type: "badge", 
      title: "New badge unlocked: Top Spender", 
      description: "You earned a new badge for your recent purchases. Check it out on your profile.",
      time: "1 hour ago", 
      unread: true 
    },
    { 
      id: 3, 
      type: "promo", 
      title: "Don't forget your monthly spin!", 
      description: "Head over to the Spin & Save page to win up to 20% off your next meal.",
      time: "1 day ago", 
      unread: false 
    },
    { 
      id: 4, 
      type: "system", 
      title: "Welcome to QuickBite!", 
      description: "Thanks for joining us. Start exploring menus and earning rewards today.",
      time: "3 days ago", 
      unread: false 
    },
  ];

  const getIcon = (type) => {
    switch (type) {
      case "order": return "🍔";
      case "badge": return "🏆";
      case "promo": return "🎉";
      default: return "👋";
    }
  };

  // Triggers the animation based on the notification type
  const handleNotificationClick = (type) => {
    // Prevent overlapping animations
    if (activeAnimation) return; 
    
    setActiveAnimation(type);

    // Clear the animation after it finishes (1.5 seconds)
    setTimeout(() => {
      setActiveAnimation(null);
    }, 1500);
  };

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
      {/* pointer-events-none ensures the animation doesn't block you from clicking things underneath */}
      {activeAnimation && (
        <div className="fixed inset-0 pointer-events-none flex items-center justify-center z-50 overflow-hidden">
          {activeAnimation === "order" && (
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
          {activeAnimation === "system" && (
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
        <button className="text-sm font-medium text-orange-500 hover:text-orange-600 bg-orange-50 px-4 py-2 rounded-md transition-colors">
          Mark all as read
        </button>
      </div>

      {/* Notifications List */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        {notifications.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {notifications.map((notif) => (
              <li 
                key={notif.id} 
                onClick={() => handleNotificationClick(notif.type)}
                className={`p-5 hover:bg-gray-50 transition-colors cursor-pointer ${notif.unread ? 'bg-orange-50/30' : 'bg-white'}`}
              >
                <div className="flex gap-4 pointer-events-none">
                  {/* Icon */}
                  <div className="flex-shrink-0 mt-1 text-2xl">
                    {getIcon(notif.type)}
                  </div>
                  
                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-gray-900 flex items-center gap-2">
                      {notif.title}
                      {notif.unread && (
                        <span className="inline-block h-2 w-2 rounded-full bg-red-500"></span>
                      )}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      {notif.description}
                    </p>
                    <p className="text-xs text-gray-400 mt-2 font-medium">
                      {notif.time}
                    </p>
                  </div>

                  {/* Optional Action Button - Using stopPropagation to prevent the li click from firing when clicking the link */}
                  {notif.type === "promo" && (
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
                  {notif.type === "badge" && (
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
            ))}
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
