import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import '../styles/UserProfile.css';
import { Button, Form, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';

const UserProfile = () => {
    const { user, logout, cargando } = useContext(AuthContext);
    const [pedidos, setPedidos] = useState([]);
    const [tarjetas, setTarjetas] = useState([]);
    const [formData, setFormData] = useState({
        nombre: '',
        correo: '',
        direccion: '',
        telefono: '',
        contraseña: '',
    });
    const [mensaje, setMensaje] = useState(null);
    const [error, setError] = useState(null);
    const [validations, setValidations] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        if (user) {
            setFormData({
                nombre: user.nombre,
                correo: user.correo,
                direccion: user.direccion || '',
                telefono: user.telefono || '',
                contraseña: '',
            });

            axios
                .get(`http://localhost:8000/pedidos`, { withCredentials: true })
                .then((response) => {
                    setPedidos(response.data);
                })
                .catch((err) => {
                    console.error(err);
                });

            axios
                .get(`http://localhost:8000/tarjetas`, { withCredentials: true })
                .then((response) => {
                    setTarjetas(response.data);
                })
                .catch((err) => {
                    console.error(err);
                });
        }
    }, [user]);

    if (cargando) {
        return <div className="loading">Cargando...</div>;
    }

    if (!user) {
        return <div className="not-authenticated">No hay usuario autenticado.</div>;
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });

        let tempValidations = { ...validations };

        switch (name) {
            case 'correo':
                tempValidations.correo = validateEmail(value) ? null : 'El correo electrónico no tiene un formato válido.';
                break;
            case 'telefono':
                tempValidations.telefono = validatePhone(value) ? null : 'El número de teléfono solo debe contener dígitos.';
                break;
            case 'contraseña':
                tempValidations.contraseña = value.length >= 6 || value.length === 0 ? null : 'La contraseña debe tener al menos 6 caracteres.';
                break;
            default:
                break;
        }

        setValidations(tempValidations);

        if (Object.values(tempValidations).every((msg) => msg === null)) {
            setError(null);
        }
    };

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const validatePhone = (phone) => {
        const re = /^\d+$/;
        return re.test(String(phone));
    };

    const handleActualizar = async (e) => {
        e.preventDefault();
        const { nombre, correo, direccion, telefono, contraseña } = formData;
        let valid = true;
        let tempValidations = {};

        if (!validateEmail(correo)) {
            tempValidations.correo = 'El correo electrónico no tiene un formato válido.';
            valid = false;
        }

        if (telefono && !validatePhone(telefono)) {
            tempValidations.telefono = 'El número de teléfono solo debe contener dígitos.';
            valid = false;
        }

        if (contraseña && contraseña.length < 6) {
            tempValidations.contraseña = 'La contraseña debe tener al menos 6 caracteres.';
            valid = false;
        }

        setValidations(tempValidations);

        if (!valid) {
            setError('Por favor, corrige los errores en el formulario.');
            setMensaje(null);
            return;
        }

        setIsSubmitting(true);

        const updateData = {
            nombre,
            correo,
            direccion,
            telefono,
        };

        if (contraseña) {
            updateData.contraseña = contraseña;
        }

        try {
            const response = await axios.put(
                `http://localhost:8000/usuarios/${user.id_usuario}`,
                updateData,
                { withCredentials: true }
            );
            setMensaje('Información actualizada correctamente.');
            setError(null);
            setValidations({});
        } catch (err) {
            console.error(err);
            setError('Error al actualizar la información.');
            setMensaje(null);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleEliminarTarjeta = async (id_tarjeta) => {
        if (window.confirm('¿Estás seguro de que deseas eliminar esta tarjeta?')) {
            try {
                await axios.delete(`http://localhost:8000/tarjetas/${id_tarjeta}`, { withCredentials: true });
                setTarjetas(tarjetas.filter(tarjeta => tarjeta.id_tarjeta !== id_tarjeta));
                setMensaje('Tarjeta eliminada correctamente.');
                setError(null);
            } catch (err) {
                console.error(err);
                setError('Error al eliminar la tarjeta.');
                setMensaje(null);
            }
        }
    };

    return (
        <div className="profile-container">
            <h2>Perfil de Usuario</h2>
            {mensaje && <Alert variant="success">{mensaje}</Alert>}
            {error && <Alert variant="danger">{error}</Alert>}
            <div className="profile-content">
                <div className="profile-section">
                    <h3>Información del Usuario</h3>
                    <p><strong>Correo:</strong> {user.correo}</p>
                    <p><strong>Dirección:</strong> {user.direccion || 'No proporcionada'}</p>
                    <p><strong>Teléfono:</strong> {user.telefono || 'No proporcionado'}</p>
                </div>

                <div className="profile-section">
                    <h3>Pedidos</h3>
                    {pedidos.length > 0 ? (
                        <ul className="orders-list">
                            {pedidos.map((pedido) => (
                                <li key={pedido.id_pedido} className="order-item">
                                    <div><strong>ID Pedido:</strong> {pedido.id_pedido}</div>
                                    <div><strong>Total:</strong> ${parseFloat(pedido.total).toFixed(2)}</div>
                                    <div><strong>Estado:</strong> {pedido.estado}</div>
                                    <div><strong>Fecha:</strong> {new Date(pedido.fecha_pedido).toLocaleDateString()}</div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No has realizado ningún pedido.</p>
                    )}
                </div>

                <div className="profile-section">
                    <h3>Tarjetas de Pago</h3>
                    {tarjetas.length > 0 ? (
                        <div className="tarjetas-list">
                            {tarjetas.map((tarjeta) => (
                                <div key={tarjeta.id_tarjeta} className="tarjeta-item">
                                    <div className="tarjeta-info">
                                        <i className="fas fa-credit-card tarjeta-icon"></i>
                                        <span>**** **** **** {tarjeta.numero_tarjeta.slice(-4)}</span>
                                    </div>
                                    <Button variant="danger" size="sm" onClick={() => handleEliminarTarjeta(tarjeta.id_tarjeta)}>
                                        <i className="fas fa-trash-alt"></i> Eliminar
                                    </Button>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>No tienes tarjetas registradas.</p>
                    )}
                </div>

                <div className="profile-section">
                    <h3>Inicio de Sesión y Seguridad</h3>
                    <Form onSubmit={handleActualizar} className="update-form">
                        <Form.Group className="mb-3" controlId="formNombre">
                            <Form.Label>Nombre</Form.Label>
                            <Form.Control
                                type="text"
                                name="nombre"
                                value={formData.nombre}
                                onChange={handleChange}
                                required
                                placeholder="Ingrese su nombre"
                            />
                            {validations.nombre && <Form.Text className="text-danger">{validations.nombre}</Form.Text>}
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formCorreo">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                type="email"
                                name="correo"
                                value={formData.correo}
                                onChange={handleChange}
                                required
                                placeholder="Ingrese su correo electrónico"
                                isInvalid={!!validations.correo}
                            />
                            <Form.Control.Feedback type="invalid">
                                {validations.correo}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formTelefono">
                            <Form.Label>Número de Teléfono</Form.Label>
                            <Form.Control
                                type="text"
                                name="telefono"
                                value={formData.telefono}
                                onChange={handleChange}
                                placeholder="Ingrese su número de teléfono"
                                isInvalid={!!validations.telefono}
                            />
                            <Form.Control.Feedback type="invalid">
                                {validations.telefono}
                            </Form.Control.Feedback>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formDireccion">
                            <Form.Label>Dirección</Form.Label>
                            <Form.Control
                                type="text"
                                name="direccion"
                                value={formData.direccion}
                                onChange={handleChange}
                                placeholder="Ingrese su dirección"
                            />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formContraseña">
                            <Form.Label>Contraseña</Form.Label>
                            <Form.Control
                                type="password"
                                name="contraseña"
                                value={formData.contraseña}
                                onChange={handleChange}
                                placeholder="Ingrese una nueva contraseña"
                                isInvalid={!!validations.contraseña}
                            />
                            <Form.Control.Feedback type="invalid">
                                {validations.contraseña}
                            </Form.Control.Feedback>
                            <Form.Text className="text-muted">
                                Si deseas cambiar tu contraseña, ingresa una nueva. Debe tener al menos 6 caracteres.
                            </Form.Text>
                        </Form.Group>

                        <Button variant="primary" type="submit" className="btn-update" disabled={isSubmitting}>
                            {isSubmitting ? (
                                <>
                                    <Spinner
                                        as="span"
                                        animation="border"
                                        size="sm"
                                        role="status"
                                        aria-hidden="true"
                                    /> Actualizando...
                                </>
                            ) : (
                                'Actualizar Información'
                            )}
                        </Button>
                    </Form>
                    <Button variant="danger" className="btn-logout" onClick={logout}>
                        Cerrar Sesión
                    </Button>
                </div>
            </div>
        </div>
    );

};

export default UserProfile;