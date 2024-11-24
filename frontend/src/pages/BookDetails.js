import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Image, Button, Spinner, Alert } from 'react-bootstrap';
import '../styles/BookDetails.css';

function BookDetails() {
    const { id_libro } = useParams();
    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchBook = async () => {
            try {
                const response = await fetch(`http://localhost:8000/libros/${id_libro}`);
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
    }, [id_libro]);

    if (loading) return <Spinner animation="border" />;
    if (error) return <Alert variant="danger">{error}</Alert>;
    if (!book) return <Alert variant="info">Libro no encontrado</Alert>;

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
                    <p>
                        <strong>Autor:</strong> {book.autor ? book.autor.nombre : 'Autor Desconocido'}
                    </p>
                    <p>
                        <strong>Categoría:</strong>{' '}
                        {book.categoria ? book.categoria.nombre_categoria : 'Sin categoría'}
                    </p>
                    <p className="price">
                        <strong>Precio:</strong> ${book.precio}
                    </p>
                    <p className="stock">
                        <strong>Stock:</strong> {book.stock} unidades disponibles
                    </p>
                    <p>
                        <strong>Fecha de Publicación:</strong> {book.fecha_publicacion || 'Desconocida'}
                    </p>
                    <p>
                        <strong>ISBN:</strong> {book.isbn || 'No disponible'}
                    </p>
                    <p>{book.descripcion || 'Sin descripción disponible.'}</p>
                    <Button variant="success">Agregar al Carrito</Button>
                </Col>
            </Row>
        </Container>
    );
}

export default BookDetails;