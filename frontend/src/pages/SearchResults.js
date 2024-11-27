import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import queryString from 'query-string';
import Footer from '../components/Footer';

function useQuery() {
    return queryString.parse(useLocation().search);
}

function SearchResults() {
    const { filter, query } = useQuery();
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await fetch(`http://localhost:8000/libros/buscar?filter=${filter}&query=${encodeURIComponent(query)}`);
                if (!response.ok) {
                    throw new Error('Error al obtener resultados');
                }
                const data = await response.json();
                setResults(data);
            } catch (error) {
                setError('Error al obtener resultados');
            } finally {
                setLoading(false);
            }
        };
        fetchResults();
    }, [filter, query]);

    if (loading) return <Spinner animation="border" />;
    if (error) return <Alert variant="danger">{error}</Alert>;
    if (results.length === 0) return <Alert variant="info">No se encontraron resultados</Alert>;

    return (
        <div>
            <Container className="mt-4">
                <h2>Resultados de búsqueda</h2>
                <Row>
                    {results.map((book) => (
                        <Col key={book.id_libro} md={4} sm={6} className="mb-4">
                            <Link to={`/libros/${book.id_libro}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                <Card>
                                    <Card.Img
                                        variant="top"
                                        src={book.imagen_url || '/assets/images/placeholder.jpg'}
                                        alt={book.titulo}
                                    />
                                    <Card.Body>
                                        <Card.Title>{book.titulo}</Card.Title>
                                        <Card.Text>Por {book.autor ? book.autor.nombre : 'Autor Desconocido'}</Card.Text>
                                        <Card.Text>Categoría: {book.categoria ? book.categoria.nombre_categoria : 'Sin categoría'}</Card.Text>
                                    </Card.Body>
                                </Card>
                            </Link>
                        </Col>
                    ))}
                </Row>
            </Container>
            <Footer />
        </div>
    );
}

export default SearchResults;