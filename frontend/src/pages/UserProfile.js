import React, { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import '../styles/UserProfile.css';

const UserProfile = () => {
    const { user, logout, cargando } = useContext(AuthContext);

    if (cargando) {
        return <div>Cargando...</div>;
    }

    if (!user) {
        return <div>No hay usuario autenticado.</div>;
    }

    return (
        <div className="profile-container">
            <h2>Bienvenido, {user.nombre}</h2>
            <p><strong>Correo:</strong> {user.correo}</p>
            <p><strong>Dirección:</strong> {user.direccion}</p>
            <p><strong>Teléfono:</strong> {user.telefono}</p>
            <button onClick={logout}>Cerrar Sesión</button>
        </div>
    );
};

export default UserProfile;