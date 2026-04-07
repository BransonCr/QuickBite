import { createContext, useContext, useState } from "react";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [restaurantId, setRestaurantId] = useState(null);
  const [items, setItems] = useState([]);

  function addItem(restaurantId_, item) {
    if (restaurantId && restaurantId !== restaurantId_) {
      setItems([]);
    }
    setRestaurantId(restaurantId_);
    setItems((prev) => {
      const existing = prev.find((i) => i.item_id === item.item_id);
      if (existing) {
        return prev.map((i) =>
          i.item_id === item.item_id ? { ...i, quantity: i.quantity + 1 } : i,
        );
      }
      return [...prev, { ...item, quantity: 1 }];
    });
  }

  function removeItem(itemId) {
    setItems((prev) => {
      const updated = prev
        .map((i) =>
          i.item_id === itemId ? { ...i, quantity: i.quantity - 1 } : i,
        )
        .filter((i) => i.quantity > 0);
      if (updated.length === 0) setRestaurantId(null);
      return updated;
    });
  }

  function clearCart() {
    setItems([]);
    setRestaurantId(null);
  }

  const subtotal = items.reduce((s, i) => s + i.price * i.quantity, 0);
  const itemCount = items.reduce((s, i) => s + i.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        restaurantId,
        items,
        addItem,
        removeItem,
        clearCart,
        subtotal,
        itemCount,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}
