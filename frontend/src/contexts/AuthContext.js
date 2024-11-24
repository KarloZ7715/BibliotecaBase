import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState({
        token: localStorage.getItem('token') || null,
        usuario: JSON.parse(localStorage.getItem('usuario')) || null,
    });

    const login = (token, usuario) => {
        localStorage.setItem('token', token);
        localStorage.setItem('usuario', JSON.stringify(usuario));
        setAuth({ token, usuario });
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
        setAuth({ token: null, usuario: null });
    };

    return (
        <AuthContext.Provider value={{ auth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};