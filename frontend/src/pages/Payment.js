import React, { useContext, useState, useEffect } from 'react';
import {
    Container,
    Button,
    Alert,
    Modal,
    Form,
    Row,
    Col,
    ListGroup,
    Spinner,
    Card,
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { CartContext } from '../contexts/CartContext';
import { AuthContext } from '../contexts/AuthContext';
import { FaCheckCircle } from 'react-icons/fa';
import '../styles/Payment.css';

function Payment() {
    const navigate = useNavigate();
    const { cartItems, clearCart } = useContext(CartContext);
    const { user } = useContext(AuthContext);

    const [tarjetas, setTarjetas] = useState([]);
    const [showAddCardModal, setShowAddCardModal] = useState(false);
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [processingPayment, setProcessingPayment] = useState(false);
    const [paymentCompleted, setPaymentCompleted] = useState(false);
    const [selectedCard, setSelectedCard] = useState(null);
    const [totalPedido, setTotalPedido] = useState(0);
    const [loadingCards, setLoadingCards] = useState(true);

    useEffect(() => {
        const total = cartItems.reduce((acc, item) => acc + item.precio * item.cantidad, 0);
        setTotalPedido(total.toFixed(2));

        const fetchTarjetas = async () => {
            try {
                const response = await fetch('http://localhost:8000/tarjetas', {
                    credentials: 'include',
                });
                if (!response.ok) {
                    throw new Error('Error al obtener las tarjetas');
                }
                const data = await response.json();
                setTarjetas(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoadingCards(false);
            }
        };
        fetchTarjetas();
    }, [cartItems]);

    const handleShowAddCardModal = () => setShowAddCardModal(true);
    const handleCloseAddCardModal = () => setShowAddCardModal(false);

    const handleShowConfirmModal = () => {
        if (!selectedCard) {
            alert('Por favor, selecciona una tarjeta de pago.');
            return;
        }
        setShowConfirmModal(true);
    };
    const handleCloseConfirmModal = () => setShowConfirmModal(false);

    const handleAddCard = async (event) => {
        event.preventDefault();
        const form = event.target;
        const tarjetaData = {
            tipo: form.tipo.value,
            numero_tarjeta: form.numero_tarjeta.value,
            nombre_titular: form.nombre_titular.value,
            fecha_expiracion: `${form.fecha_expiracion_anio.value}-${form.fecha_expiracion_mes.value}-01`,
        };

        try {
            const response = await fetch('http://localhost:8000/tarjetas', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tarjetaData),
            });
            if (!response.ok) {
                throw new Error('Error al agregar la tarjeta');
            }
            const nuevaTarjeta = await response.json();
            setTarjetas([...tarjetas, nuevaTarjeta]);
            handleCloseAddCardModal();
        } catch (error) {
            console.error(error);
            alert('Error al agregar la tarjeta');
        }
    };

    const handlePayment = async () => {
        const pedidoData = {
            id_usuario: user?.id_usuario,
            total: parseFloat(totalPedido),
            estado: 'En proceso',
            detallepedido: cartItems.map(item => ({
                id_libro: item.id_libro,
                cantidad: item.cantidad,
                precio_unitario: parseFloat(item.precio),
            })),
        };

        try {
            const response = await fetch('http://localhost:8000/pedidos/', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(pedidoData),
            });
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error al crear el pedido:', errorData);
                throw new Error(errorData.detail || 'Error al crear el pedido');
            }
            const nuevaPedido = await response.json();
            clearCart();
            setPaymentCompleted(true);
            navigate('/perfil');
        } catch (error) {
            console.error(error);
            alert(`Error al crear el pedido: ${error.message}`);
        }
    };

    return (
        <Container className="mt-4 payment-container">
            <h2 className="text-center">Procesar Pago</h2>
            {user && (
                <Card className="user-info-card">
                    <Card.Body>
                        <Card.Title>Entrega para: {user.nombre}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">{user.correo}</Card.Subtitle>
                    </Card.Body>
                </Card>
            )}

            <h4 className="mt-4">Método de pago</h4>
            {loadingCards ? (
                <Spinner animation="border" className="loading-spinner" />
            ) : (
                <>
                    {tarjetas.length > 0 ? (
                        <ListGroup className="tarjetas-list">
                            {tarjetas.map((tarjeta) => (
                                <ListGroup.Item
                                    key={tarjeta.id_tarjeta}
                                    active={selectedCard === tarjeta.id_tarjeta}
                                    onClick={() => setSelectedCard(tarjeta.id_tarjeta)}
                                    className="tarjeta-item"
                                >
                                    <div className="tarjeta-info">
                                        <div className="d-flex justify-content-between align-items-center">
                                            <div>
                                                <span className="tipo-tarjeta">{tarjeta.tipo}</span>
                                                <span className="numero-tarjeta"> ||
                                                    termina en {tarjeta.numero_tarjeta.slice(-4)}
                                                </span>
                                                <br />
                                                <span className="nombre-titular">{tarjeta.nombre_titular}</span>
                                                <br />
                                                <span className="fecha-expiracion">
                                                    Vence: {new Date(tarjeta.fecha_expiracion).toLocaleDateString('es-ES', { month: '2-digit', year: 'numeric' })}
                                                </span>
                                            </div>
                                            {selectedCard === tarjeta.id_tarjeta && (
                                                <FaCheckCircle color="#ffffff" size={20} />
                                            )}
                                        </div>
                                    </div>
                                </ListGroup.Item>
                            ))}
                        </ListGroup>
                    ) : (
                        <p>
                            No tienes tarjetas guardadas.{' '}
                            <a href="#!" onClick={handleShowAddCardModal} className="add-card-link">
                                Agregar una tarjeta de crédito o débito
                            </a>
                        </p>
                    )}
                </>
            )}

            {tarjetas.length > 0 && (
                <p>
                    <a href="#!" onClick={handleShowAddCardModal} className="add-card-link">
                        Agregar una nueva tarjeta de crédito o débito
                    </a>
                </p>
            )}

            <Row className="mt-4">
                <Col md={8}></Col>
                <Col md={4}>
                    <Button variant="primary" onClick={handleShowConfirmModal} className="payment-button">
                        Usar este método de pago
                    </Button>

                    <Card className="summary-card mt-4">
                        <Card.Header>Resumen del Pedido</Card.Header>
                        <ListGroup variant="flush">
                            {cartItems.map((item) => (
                                <ListGroup.Item key={item.id_libro}>
                                    <div className="d-flex justify-content-between">
                                        <span>{item.titulo}</span>
                                        <span>${(item.precio * item.cantidad).toFixed(2)}</span>
                                    </div>
                                </ListGroup.Item>
                            ))}
                            <ListGroup.Item className="total-item">
                                <strong>Total del pedido:</strong>
                                <strong>${totalPedido}</strong>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
            <Modal show={showAddCardModal} onHide={handleCloseAddCardModal} centered>
                <Form onSubmit={handleAddCard}>
                    <Modal.Header closeButton>
                        <Modal.Title>Agregar una tarjeta de crédito o débito</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group className="mb-3">
                            <Form.Label>Tipo de tarjeta</Form.Label>
                            <Form.Control as="select" name="tipo" required>
                                <option value="">Seleccione</option>
                                <option value="Crédito">Crédito</option>
                                <option value="Débito">Débito</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Número de tarjeta</Form.Label>
                            <Form.Control
                                type="text"
                                name="numero_tarjeta"
                                maxLength="16"
                                required
                                placeholder="Ingrese los 16 dígitos"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Nombre del titular</Form.Label>
                            <Form.Control type="text" name="nombre_titular" required placeholder="Nombre completo" />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Fecha de vencimiento</Form.Label>
                            <Row>
                                <Col>
                                    <Form.Control as="select" name="fecha_expiracion_mes" required>
                                        <option value="">Mes</option>
                                        {[...Array(12)].map((_, i) => (
                                            <option key={i + 1} value={(i + 1).toString().padStart(2, '0')}>
                                                {(i + 1).toString().padStart(2, '0')}
                                            </option>
                                        ))}
                                    </Form.Control>
                                </Col>
                                <Col>
                                    <Form.Control as="select" name="fecha_expiracion_anio" required>
                                        <option value="">Año</option>
                                        {[
                                            ...Array(10).keys(),
                                        ].map((i) => (
                                            <option key={i} value={new Date().getFullYear() + i}>
                                                {new Date().getFullYear() + i}
                                            </option>
                                        ))}
                                    </Form.Control>
                                </Col>
                            </Row>
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleCloseAddCardModal}>
                            Cancelar
                        </Button>
                        <Button variant="primary" type="submit">
                            Agregar tarjeta
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>

            <Modal show={showConfirmModal} onHide={handleCloseConfirmModal} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Confirmación de compra</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    ¿Estás seguro que deseas continuar con la compra?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseConfirmModal}>
                        Cancelar
                    </Button>
                    <Button variant="success" onClick={handlePayment}>
                        Pagar
                    </Button>
                </Modal.Footer>
            </Modal>
            {processingPayment && (
                <Alert variant="info" className="mt-4 text-center">
                    Procesando el pago...
                </Alert>
            )}
            {paymentCompleted && (
                <Alert variant="success" className="mt-4 text-center">
                    Pago completado
                </Alert>
            )}
        </Container>
    );
}

export default Payment;