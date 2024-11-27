import React, { createContext, useState, useEffect, useContext } from 'react';
import { toast } from 'react-toastify';
import { AuthContext } from './AuthContext';
import {
    obtenerCarrito,
    agregarAlCarrito,
    actualizarCantidadCarrito,
    eliminarDelCarrito,
    vaciarCarrito,
} from '../api';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const { isAuthenticated } = useContext(AuthContext);

    useEffect(() => {
        if (isAuthenticated) {
            cargarCarrito();
        } else {
            setCartItems([]);
        }
    }, [isAuthenticated]);

    const cargarCarrito = async () => {
        try {
            const data = await obtenerCarrito();
            const items = data.map((item) => ({
                id_libro: item.id_libro,
                cantidad: item.cantidad,
                titulo: item.libro.titulo,
                precio: item.libro.precio,
                stock: item.libro.stock,
                imagen_url: item.libro.imagen_url,
            }));
            setCartItems(items);
        } catch (error) {
            console.error('Error al cargar el carrito:', error);
            toast.error('No se pudo cargar el carrito.');
        }
    };

    const addToCart = async (libro) => {
        try {
            await agregarAlCarrito(libro.id_libro);
            cargarCarrito();
            toast.success(`"${libro.titulo}" agregado al carrito.`);
        } catch (error) {
            console.error('Error al agregar al carrito:', error);
            toast.error('Error al agregar el libro al carrito.');
        }
    };

    const removeFromCart = async (id_libro) => {
        try {
            await eliminarDelCarrito(id_libro);
            setCartItems((prevItems) => prevItems.filter((item) => item.id_libro !== id_libro));
            toast.info('Ítem eliminado del carrito.');
        } catch (error) {
            console.error('Error al eliminar del carrito:', error);
            toast.error('Error al eliminar el ítem del carrito.');
        }
    };

    const incrementQuantity = async (id_libro) => {
        try {
            const item = cartItems.find((item) => item.id_libro === id_libro);
            await actualizarCantidadCarrito(id_libro, item.cantidad + 1);
            cargarCarrito();
            toast.success(`Aumentaste la cantidad de "${item.titulo}".`);
        } catch (error) {
            console.error('Error al incrementar la cantidad:', error);
            toast.error('Error al incrementar la cantidad.');
        }
    };

    const decrementQuantity = async (id_libro) => {
        try {
            const item = cartItems.find((item) => item.id_libro === id_libro);
            if (item.cantidad > 1) {
                await actualizarCantidadCarrito(id_libro, item.cantidad - 1);
                cargarCarrito();
            } else {
                await eliminarDelCarrito(id_libro);
                setCartItems((prevItems) => prevItems.filter((item) => item.id_libro !== id_libro));
            }
        } catch (error) {
            console.error('Error al decrementar la cantidad:', error);
            toast.error('Error al decrementar la cantidad.');
        }
    };

    const clearCart = async () => {
        try {
            await vaciarCarrito();
            setCartItems([]);
            toast.success('Carrito vaciado exitosamente.');
        } catch (error) {
            console.error('Error al vaciar el carrito:', error);
            toast.error('Error al vaciar el carrito.');
        }
    };

    return (
        <CartContext.Provider
            value={{
                cartItems,
                addToCart,
                removeFromCart,
                incrementQuantity,
                decrementQuantity,
                clearCart,
            }}
        >
            {children}
        </CartContext.Provider>
    );
};