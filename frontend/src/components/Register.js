import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { registerUsuario, loginUsuario } from '../api';
import { registrarUsuario } from '../services/api';

const Register = () => {
    const [nombre, setNombre] = useState('');
    const [correo, setCorreo] = useState('');
    const [contraseña, setContraseña] = useState('');
    const { login } = useContext(AuthContext);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registrarUsuario({ nombre, correo, contraseña });
            const data = await loginUsuario({ correo, contraseña });
            login(data.access_token, { correo });
        } catch (err) {
            setError('Error al registrar');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Registrarse</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div>
                <label>Nombre:</label>
                <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            </div>
            <div>
                <label>Correo:</label>
                <input type="email" value={correo} onChange={(e) => setCorreo(e.target.value)} required />
            </div>
            <div>
                <label>Contraseña:</label>
                <input type="password" value={contraseña} onChange={(e) => setContraseña(e.target.value)} required />
            </div>
            <button type="submit">Registrarse</button>
        </form>
    );
};

export default Register;