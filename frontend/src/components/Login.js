import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { loginUsuario } from '../api';

const Login = () => {
    const [correo, setCorreo] = useState('');
    const [contraseña, setContraseña] = useState('');
    const { login } = useContext(AuthContext);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await loginUsuario({ correo, contraseña });
            login(data.access_token, { correo });
        } catch (err) {
            setError('Credenciales incorrectas');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Iniciar Sesión</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div>
                <label>Correo:</label>
                <input
                    type="email"
                    value={correo}
                    onChange={(e) => setCorreo(e.target.value)} required />
            </div>
            <div>
                <input>Contraseña:</input>
                <input type="password" value={contraseña} onChange={(e) => setContraseña(e.target.value)} required />
            </div>
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;