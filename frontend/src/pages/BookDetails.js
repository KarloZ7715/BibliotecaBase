import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Image, Button, Spinner, Alert } from 'react-bootstrap';
import { CartContext } from '../contexts/CartContext';
import { motion } from 'framer-motion';
import '../styles/BookDetails.css';

function BookDetails() {
    const { id } = useParams();
    const { addToCart } = useContext(CartContext);
    const navigate = useNavigate();
    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchBook = async () => {
            try {
                const response = await fetch(`http://localhost:8000/libros/${id}`);
                if (!response.ok) {
                    throw new Error('Error al obtener detalles del libro');
                }
                const data = await response.json();
                setBook(data);
            } catch (err) {
                setError('Error al cargar los detalles del libro');
            } finally {
                setLoading(false);
            }
        };
        fetchBook();
    }, [id]);

    if (loading) return <Spinner animation="border" />;
    if (error) return <Alert variant="danger">{error}</Alert>;
    if (!book) return <Alert variant="info">Libro no encontrado</Alert>;

    const handleAddToCart = () => {
        addToCart(book);
    };

    const handleBuyNow = () => {
        addToCart(book);
        navigate('/carrito');
    };

    return (
        <Container className="book-details-page mt-4">
            <Row>
                <Col md={4}>
                    <Image
                        src={book.imagen_url || '/assets/images/placeholder.jpg'}
                        alt={book.titulo}
                        fluid
                    />
                </Col>
                <Col md={8}>
                    <h2>{book.titulo}</h2>
                    <p><strong>Autor:</strong> {book.autor ? book.autor.nombre : 'Autor Desconocido'}</p>

                    <div className="book-details">
                        <p><strong>Categoría:</strong> {book.categoria ? book.categoria.nombre_categoria : 'Sin categoría'}</p>
                        <p className="price"><strong>Precio:</strong> ${book.precio}</p>
                        <p className="stock">
                            <strong>Stock:</strong>{' '}
                            {book.stock > 0 ? (
                                <span style={{ color: 'green', fontSize: '0.8rem' }}>Disponible</span>
                            ) : (
                                <span style={{ color: 'red', fontSize: '0.8rem' }}>Agotado</span>
                            )}
                        </p>
                        <p><strong>Fecha de Publicación:</strong> {book.fecha_publicacion || 'Desconocida'}</p>
                        <p><strong>ISBN:</strong> {book.isbn || 'No disponible'}</p>
                    </div>

                    <motion.div whileTap={{ scale: 0.95 }}>
                        <Button
                            as={motion.button}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            whileFocus={{ scale: 1.05 }}
                            animate={{ y: 0 }}
                            transition={{ type: 'spring', stiffness: 300 }}
                            variant="success"
                            onClick={handleAddToCart}
                            className="shop_btn"
                        >
                            Agregar al Carrito
                        </Button>
                    </motion.div>

                    <motion.div whileTap={{ scale: 0.95 }} className="mt-3">
                        <Button
                            as={motion.button}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            whileFocus={{ scale: 1.05 }}
                            animate={{ y: 0 }}
                            transition={{ type: 'spring', stiffness: 300 }}
                            variant="primary"
                            onClick={handleBuyNow}
                            className="shop_btn"
                        >
                            Comprar Ahora
                        </Button>
                    </motion.div>
                </Col>
            </Row>
        </Container>
    );
}

export default BookDetails;