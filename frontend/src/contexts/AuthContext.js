import React, { createContext, useState, useEffect } from 'react';
import { logoutUsuario, obtenerUsuarioActual } from '../api';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [cargando, setCargando] = useState(true);
    const navigate = useNavigate();

    const login = (userData) => {
        setUser(userData);
    };

    const logout = async () => {
        try {
            await logoutUsuario();
            setUser(null);
            navigate('/login');
        } catch (error) {
            console.error('Error al cerrar sesión:', error);
        }
    };

    const verificarUsuario = async () => {
        try {
            const data = await obtenerUsuarioActual();
            setUser(data);
        } catch (error) {
            setUser(null);
        } finally {
            setCargando(false);
        }
    };

    useEffect(() => {
        verificarUsuario();
    }, []);

    return (
        <AuthContext.Provider value={{
            user,
            isAuthenticated: !!user,
            login,
            logout,
            cargando
        }}>
            {children}
        </AuthContext.Provider>
    );
};