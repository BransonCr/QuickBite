import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import AdminPage from "./pages/AdminPage";
import BadgesPage from "./pages/BadgesPage";
import ProfilePage from "./pages/ProfilePage";
import BrowseRestaurantsPage from "./pages/BrowseRestaurantsPage";
import RestaurantDetailPage from "./pages/RestaurantDetailPage";
import SpinWheelPage from "./pages/SpinWheelPage";
import NotificationPage from "./pages/NotificationPage";
import CheckoutPage from "./pages/CheckoutPage";
import OrderConfirmationPage from "./pages/OrderConfirmationPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import UserPage from "./pages/UserPage";
import { CartProvider } from "./context/CartContext";

function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            <Route
              path="/"
              element={
                <div className="max-w-4xl mx-auto px-4 py-16 text-center">
                  <p className="text-6xl mb-4">🍔</p>
                  <h1 className="text-4xl font-bold text-gray-900 mb-2">
                    QuickBite
                  </h1>
                  <p className="text-gray-500">
                    Fast food delivery at your fingertips.
                  </p>
                </div>
              }
            />
            <Route path="/badges" element={<BadgesPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/browse" element={<BrowseRestaurantsPage />} />
            <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
            <Route path="/spin" element={<SpinWheelPage />} />
            <Route path="/notifications" element={<NotificationPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/order/:orderId" element={<OrderConfirmationPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/users" element={<UserPage />} />
          </Routes>
        </div>
      </CartProvider>
    </BrowserRouter>
  );
}

export default App;
