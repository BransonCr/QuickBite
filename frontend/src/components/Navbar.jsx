import React, { useState, useRef, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // 1. Check if we are currently on the notifications page
  const isNotifPage = pathname === "/notifications";

  // Closes the dropdown when the user clicks outside of it
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // 2. Automatically close the dropdown if the route changes to /notifications
  useEffect(() => {
    if (isNotifPage) {
      setIsDropdownOpen(false);
    }
  }, [isNotifPage]);

  // Dummy notifications
  const notifications = [
    { id: 1, text: "Your order is on the way!", time: "2m ago" },
    { id: 2, text: "New badge unlocked: Top Spender", time: "1h ago" },
    { id: 3, text: "Don't forget your monthly spin!", time: "1d ago" },
  ];

  const link = (to, label) => (
    <Link
      to={to}
      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
        pathname === to
          ? "bg-orange-500 text-white"
          : "text-gray-600 hover:text-orange-500"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-orange-500">
          QuickBite
        </Link>
        <div className="flex items-center gap-1">
          {link("/", "Home")}
          {link("/browse", "Browse")}
          {link("/badges", "Badges")}
          {link("/profile", "Profile")}

          {/* Notification Bell & Dropdown */}
          <div className="relative mx-1" ref={dropdownRef}>
            <button
              // 3. Only toggle if we are NOT on the notifications page
              onClick={() => {
                if (!isNotifPage) setIsDropdownOpen(!isDropdownOpen);
              }}
              // 4. Disable the button functionality when on the page
              disabled={isNotifPage}
              // 5. Apply active styles conditionally
              className={`p-2 focus:outline-none transition-colors relative rounded-full ${
                isNotifPage
                  ? "bg-orange-500 text-white cursor-default" // Highlighted state
                  : "text-gray-600 hover:text-orange-500 hover:bg-gray-50 cursor-pointer" // Default state
              }`}
              aria-label="Notifications"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                />
              </svg>
              {/* Adjust indicator dot colors so it doesn't clash with the orange background */}
              <span
                className={`absolute top-1.5 right-2 block h-1.5 w-1.5 rounded-full ring-2 ${
                  isNotifPage
                    ? "bg-white ring-orange-500"
                    : "bg-red-500 ring-white"
                }`}
              ></span>
            </button>

            {/* Dropdown Menu - Ensure it never renders if on the notif page */}
            {isDropdownOpen && !isNotifPage && (
              <div className="absolute right-0 top-full mt-2 w-72 bg-white rounded-md shadow-lg py-1 border border-gray-100 z-50">
                <div className="px-4 py-2 border-b border-gray-100 flex justify-between items-center">
                  <h3 className="text-sm font-bold text-gray-900">
                    Notifications
                  </h3>
                  <Link
                    to="/notifications"
                    className="text-xs text-orange-500 hover:text-orange-600 font-medium"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    View All
                  </Link>
                </div>
                <div className="max-h-64 overflow-y-auto">
                  {notifications.map((notif) => (
                    <div
                      key={notif.id}
                      className="px-4 py-3 hover:bg-gray-50 border-b border-gray-50 last:border-0 transition-colors"
                    >
                      <p className="text-sm text-gray-800">{notif.text}</p>
                      <p className="text-xs text-gray-400 mt-1">{notif.time}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {link("/spin", "Spin & Save")}
          {link("/admin", "Admin")}
          {link("/login", "Login")}
          {link("/register", "Register")}
          {link("/users", "Users")}
        </div>
      </div>
    </nav>
  );
}
