import React, { useEffect, useState } from 'react';
import { Button, Container, Row, Col, Card, Spinner, Alert, Image } from 'react-bootstrap';
import { fetchRandomBooks } from '../api';
import BookCarousel from '../components/BookCarousel';
import HeroBanner from '../components/HeroBanner';
import Categories from '../components/Categories';
import Footer from '../components/Footer';
import '../styles/Home.css';
import { useNavigate } from 'react-router-dom';
import AOS from 'aos';
import 'aos/dist/aos.css';

function Home() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchRandomBooks(5)
            .then(data => {
                setBooks(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error al obtener libros aleatorios:', error);
                setLoading(false);
            });

        AOS.init({
            duration: 1000,
            once: true,
        });
    }, []);

    return (
        <div className="home-background">
            {/* Banner Principal */}
            <HeroBanner />

            {/* Libros Destacados */}
            <section className="featured-books-section" data-aos="fade-up">
                <h2 className="section-title">Libros Destacados</h2>
                {loading ? (
                    <div className="loading-spinner">
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden">Cargando...</span>
                        </Spinner>
                    </div>
                ) : (
                    <Row>
                        {books.map(book => (
                            <Col key={book.id_libro} md={4} sm={6} className="mb-4" data-aos="zoom-in">
                                <Card className="fade-in">
                                    <Card.Img variant="top" src={book.imagen_url || '/assets/images/placeholder.jpg'} className="card-img-top" />
                                    <Card.Body>
                                        <Card.Title className="card-title">{book.titulo}</Card.Title>
                                        <Card.Text className="card-text">
                                            Autor: {book.autor ? book.autor.nombre : 'Autor Desconocido'}
                                        </Card.Text>
                                        <Card.Text className="card-text">
                                            Precio: ${book.precio.toFixed(2)}
                                        </Card.Text>
                                        <Button variant="success" className="btn-shop" onClick={() => navigate(`/libros/${book.id_libro}`)}>
                                            Comprar Ahora
                                        </Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                        ))}
                    </Row>
                )}
            </section>

            {/* Nuevas Llegadas */}
            <Container className="mt-5">
                <h2 className="section-title">Nuevas Llegadas</h2>
                <Row>
                    <Col md={3} sm={6} className="new-arrival-card">
                        <img src="ruta/a/nuevollegada1.jpg" alt="Nuevo Libro 1" className="new-arrival-image" />
                        <h5>Título del Libro 1</h5>
                        <p>Autor del Libro 1</p>
                        <Button variant="success">Agregar al Carrito</Button>
                    </Col>
                    <Col md={3} sm={6} className="new-arrival-card">
                        <img src="ruta/a/nuevollegada2.jpg" alt="Nuevo Libro 2" className="new-arrival-image" />
                        <h5>Título del Libro 2</h5>
                        <p>Autor del Libro 2</p>
                        <Button variant="success">Agregar al Carrito</Button>
                    </Col>
                    <Col md={3} sm={6} className="new-arrival-card">
                        <img src="ruta/a/nuevollegada3.jpg" alt="Nuevo Libro 3" className="new-arrival-image" />
                        <h5>Título del Libro 3</h5>
                        <p>Autor del Libro 3</p>
                        <Button variant="success">Agregar al Carrito</Button>
                    </Col>
                    <Col md={3} sm={6} className="new-arrival-card">
                        <img src="ruta/a/nuevollegada4.jpg" alt="Nuevo Libro 4" className="new-arrival-image" />
                        <h5>Título del Libro 4</h5>
                        <p>Autor del Libro 4</p>
                        <Button variant="success">Agregar al Carrito</Button>
                    </Col>
                </Row>
            </Container>

            {/* Componentes de Carrusel de Libros */}
            <BookCarousel title="Otro Set de Libros Destacados" limit={5} />

            {/* Categorías */}
            <Categories />

            {/* Footer */}
            <Footer />
        </div>
    );
}

export default Home;
