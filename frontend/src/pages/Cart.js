import React, { useContext } from 'react';
import { Container, Row, Col, Image, Button, Alert } from 'react-bootstrap';
import { CartContext } from '../contexts/CartContext';
import { FaTrash, FaPlus } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Cart.css';

function Cart() {
    const { cartItems, removeFromCart, incrementQuantity } = useContext(CartContext);
    const navigate = useNavigate();

    const subtotal = cartItems.reduce((acc, item) => acc + item.precio * item.quantity, 0);
    const totalProducts = cartItems.reduce((acc, item) => acc + item.quantity, 0);

    if (cartItems.length === 0) {
        return (
            <Container className="mt-4">
                <Alert variant="info">Tu carrito está vacío.</Alert>
            </Container>
        );
    }

    const handleProceedToPayment = () => {
        navigate('/pago');
    };

    return (
        <Container className="mt-4">
            <h2>Tu Carrito</h2>
            {cartItems.map((item) => (
                <Row key={item.id_libro} className="cart-item align-items-center my-3">
                    <Col md={2}>
                        <Image src={item.imagen_url || '/assets/images/placeholder.jpg'} alt={item.titulo} fluid />
                    </Col>
                    <Col md={4}>
                        <Link to={`/libros/${item.id_libro}`} className="cart-item-title">
                            {item.titulo}
                        </Link>
                    </Col>
                    <Col md={2}>
                        <p className="mb-1"><strong>Precio:</strong> ${item.precio}</p>
                        <p className="mb-0">
                            <strong>Stock:</strong>{' '}
                            {item.stock > 0 ? (
                                <span style={{ color: 'green', fontSize: '0.9rem' }}>Disponible</span>
                            ) : (
                                <span style={{ color: 'red', fontSize: '0.9rem' }}>Agotado</span>
                            )}
                        </p>
                    </Col>
                    <Col md={4} className="d-flex align-items-center">
                        <Button
                            variant="danger"
                            onClick={() => removeFromCart(item.id_libro)}
                            className="me-2"
                        >
                            <FaTrash />
                        </Button>
                        <span>{item.quantity}</span>
                        <Button
                            variant="success"
                            onClick={() => incrementQuantity(item.id_libro)}
                            className="ms-2"
                        >
                            <FaPlus />
                        </Button>
                    </Col>
                </Row>
            ))}

            <Row className="mt-4">
                <Col md={{ span: 4, offset: 8 }} className="text-end">
                    <h5>Subtotal ({totalProducts} producto{totalProducts > 1 ? 's' : ''}): ${subtotal.toFixed(2)}</h5>
                    <Button variant="primary" onClick={handleProceedToPayment} className="cart-shop-btn">
                        Proceder al pago
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}

export default Cart;