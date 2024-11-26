import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { loginUsuario } from '../api';
import '../styles/Login.css';

const Login = () => {
    const [correo, setCorreo] = useState('');
    const [contraseña, setContraseña] = useState('');
    const { login } = useContext(AuthContext);
    const [errores, setErrores] = useState({});
    const navigate = useNavigate();

    const validar = () => {
        let errores = {};
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!correo) {
            errores.correo = 'El correo es obligatorio';
        } else if (!correoRegex.test(correo)) {
            errores.correo = 'Correo electrónico inválido';
        }

        if (!contraseña) {
            errores.contraseña = 'La contraseña es obligatoria';
        } else if (contraseña.length < 6) {
            errores.contraseña = 'La contraseña debe tener al menos 6 caracteres';
        }

        return errores;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const erroresValidacion = validar();
        if (Object.keys(erroresValidacion).length > 0) {
            setErrores(erroresValidacion);
        } else {
            try {
                const data = await loginUsuario({ correo, contraseña });
                if (data) {
                    login(data);
                    navigate('/perfil');
                } else {
                    setErrores({ form: 'Datos de usuario inválidos' });
                }
            } catch (err) {
                if (err.response && err.response.status === 400) {
                    setErrores({ form: 'Credenciales incorrectas' });
                } else {
                    setErrores({ form: 'Error al iniciar sesión' });
                }
            }
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Iniciar Sesión</h2>
                {errores.form && <p className="error">{errores.form}</p>}
                <div className="form-group">
                    <label htmlFor="correo">Correo:</label>
                    <input
                        type="email"
                        id="correo"
                        value={correo}
                        onChange={(e) => setCorreo(e.target.value)}
                        required
                    />
                    {errores.correo && <p className="error">{errores.correo}</p>}
                </div>
                <div className="form-group">
                    <label htmlFor="contraseña">Contraseña:</label>
                    <input
                        type="password"
                        id="contraseña"
                        value={contraseña}
                        onChange={(e) => setContraseña(e.target.value)}
                        required
                    />
                    {errores.contraseña && <p className="error">{errores.contraseña}</p>}
                </div>
                <button type="submit">Iniciar Sesión</button>
                <p className="register-link">
                    ¿No tienes una cuenta? <Link to="/registro">Regístrate</Link>
                </p>
            </form>
        </div>
    );
};

export default Login;