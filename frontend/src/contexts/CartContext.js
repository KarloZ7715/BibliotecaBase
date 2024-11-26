import React, { createContext, useState, useEffect } from 'react';
import { toast } from 'react-toastify';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);

    const addToCart = (book) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find(item => item.id_libro === book.id_libro);
            if (existingItem) {
                if (existingItem.quantity < book.stock) {
                    toast.success(`Añadiste otro "${book.titulo}" al carrito.`);
                    return prevItems.map(item =>
                        item.id_libro === book.id_libro
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    );
                } else {
                    toast.error('Has alcanzado el límite de stock disponible para este libro.');
                    return prevItems;
                }
            } else {
                if (book.stock > 0) {
                    toast.success(`Añadiste "${book.titulo}" al carrito.`);
                    return [{ ...book, quantity: 1 }, ...prevItems];
                } else {
                    toast.error('Este libro está agotado.');
                    return prevItems;
                }
            }
        });
    };

    const removeFromCart = (bookId) => {
        setCartItems((prevItems) =>
            prevItems
                .map(item =>
                    item.id_libro === bookId
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                )
                .filter(item => item.quantity > 0)
        );
    };

    const incrementQuantity = (bookId) => {
        setCartItems((prevItems) =>
            prevItems.map(item => {
                if (item.id_libro === bookId) {
                    if (item.quantity < item.stock) {
                        return { ...item, quantity: item.quantity + 1 };
                    } else {
                        toast.error('Has alcanzado el límite de stock disponible para este libro.');
                    }
                }
                return item;
            })
        );
    };

    return (
        <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, incrementQuantity }}>
            {children}
        </CartContext.Provider>
    );
};