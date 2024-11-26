import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { registrarUsuario } from '../api';
import '../styles/Register.css';

const Register = () => {
    const [nombre, setNombre] = useState('');
    const [correo, setCorreo] = useState('');
    const [contraseña, setContraseña] = useState('');
    const [confirmarContraseña, setConfirmarContraseña] = useState('');
    const [direccion, setDireccion] = useState('');
    const [telefono, setTelefono] = useState('');
    const { login } = useContext(AuthContext);
    const [errores, setErrores] = useState({});
    const navigate = useNavigate();

    const validar = () => {
        let errores = {};
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const telefonoRegex = /^[0-9]+$/;

        if (!nombre) {
            errores.nombre = 'El nombre es obligatorio';
        }

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

        if (!confirmarContraseña) {
            errores.confirmarContraseña = 'Confirma tu contraseña';
        } else if (contraseña !== confirmarContraseña) {
            errores.confirmarContraseña = 'Las contraseñas no coinciden';
        }

        if (!direccion) {
            errores.direccion = 'La dirección es obligatoria';
        }

        if (!telefono) {
            errores.telefono = 'El teléfono es obligatorio';
        } else if (!telefonoRegex.test(telefono)) {
            errores.telefono = 'El teléfono debe contener solo números';
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
                const data = await registrarUsuario({ nombre, correo, contraseña, direccion, telefono });
                if (data) {
                    login(data);
                    navigate('/perfil');
                } else {
                    setErrores({ form: 'Error al registrar usuario' });
                }
            } catch (err) {
                if (err.response && err.response.status === 400) {
                    setErrores({ correo: 'El correo ya está registrado' });
                } else {
                    setErrores({ form: 'Error al registrar usuario' });
                }
            }
        }
    };

    return (
        <div className="register-container">

            <form className="register-form" onSubmit={handleSubmit}>
                <h2>Registrarse</h2>
                {errores.form && <p className="error">{errores.form}</p>}

                <div className="form-group">
                    <label htmlFor="nombre">Nombre:</label>
                    <input
                        type="text"
                        id="nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />
                    {errores.nombre && <p className="error">{errores.nombre}</p>}
                </div>

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

                <div className="form-group">
                    <label htmlFor="confirmarContraseña">Confirmar Contraseña:</label>
                    <input
                        type="password"
                        id="confirmarContraseña"
                        value={confirmarContraseña}
                        onChange={(e) => setConfirmarContraseña(e.target.value)}
                        required
                    />
                    {errores.confirmarContraseña && <p className="error">{errores.confirmarContraseña}</p>}
                </div>

                <div className="form-group">
                    <label htmlFor="direccion">Dirección:</label>
                    <input
                        type="text"
                        id="direccion"
                        value={direccion}
                        onChange={(e) => setDireccion(e.target.value)}
                        required
                    />
                    {errores.direccion && <p className="error">{errores.direccion}</p>}
                </div>

                <div className="form-group">
                    <label htmlFor="telefono">Teléfono:</label>
                    <input
                        type="text"
                        id="telefono"
                        value={telefono}
                        onChange={(e) => setTelefono(e.target.value)}
                        required
                    />
                    {errores.telefono && <p className="error">{errores.telefono}</p>}
                </div>

                <button type="submit">Registrarse</button>
                <p className="login-link">
                    ¿Ya tienes una cuenta? <Link to="/login">Inicia Sesión</Link>
                </p>
            </form>
        </div>
    );
};

export default Register;