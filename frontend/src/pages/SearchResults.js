import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import queryString from 'query-string';

function useQuery() {
    return queryString.parse(useLocation().search);
}

function SearchResults() {
    const { filter, query } = useQuery();
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await fetch(`http://localhost:8000/libros/buscar?filter=${filter}&query=${encodeURIComponent(query)}`);
                const data = await response.json();
                setResults(data);
            } catch (error) {
                console.error('Error al obtener resultados:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchResults();
    }, [filter, query]);

    if (loading) {
        return <Spinner animation="border" />;
    }

    return (
        <Container className="mt-4">
            <h2>Resultados de búsqueda</h2>
            {results.length === 0 ? (
                <Alert variant="info">No se encontraron resultados.</Alert>
            ) : (
                <Row>
                    {results.map((libro) => (
                        <Col key={libro.id_libro} md={3} sm={6} className="mb-4">
                            <Card>
                                <Card.Img
                                    variant="top"
                                    src={libro.imagen_url || '/assets/images/placeholder.jpg'}
                                    alt={libro.titulo}
                                />
                                <Card.Body>
                                    <Card.Title>{libro.titulo}</Card.Title>
                                    <Card.Text>Autor: {libro.autor?.nombre || 'Desconocido'}</Card.Text>
                                </Card.Body>
                            </Card>
                        </Col>
                    ))}
                </Row>
            )}
        </Container>
    );
}

export default SearchResults;