import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState({ items: [], total_amount: 0 });
  const [loading, setLoading] = useState(false);

  // Fetch cart on mount
  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await axios.get('/api/cart/');
      setCart(response.data);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    }
  };

  const addToCart = async (medicineId, quantity = 1) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/cart/', {
        medicine_id: medicineId,
        quantity,
      });
      setCart(response.data);
      toast.success('Added to cart successfully!');
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to add to cart';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const updateCartItem = async (itemId, quantity) => {
    setLoading(true);
    try {
      const response = await axios.put(`/api/cart/items/${itemId}/`, {
        quantity,
      });
      setCart(response.data);
      toast.success('Cart updated successfully!');
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to update cart';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (itemId) => {
    setLoading(true);
    try {
      const response = await axios.delete(`/api/cart/items/${itemId}/`);
      setCart(response.data);
      toast.success('Item removed from cart!');
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to remove item';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const clearCart = async () => {
    setLoading(true);
    try {
      // Remove all items one by one
      for (const item of cart.items) {
        await axios.delete(`/api/cart/items/${item.id}/`);
      }
      setCart({ items: [], total_amount: 0 });
      toast.success('Cart cleared successfully!');
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to clear cart';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const getCartItemCount = () => {
    return cart.items.reduce((total, item) => total + item.quantity, 0);
  };

  const value = {
    cart,
    loading,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    fetchCart,
    getCartItemCount,
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};