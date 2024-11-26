import React, { useEffect, useState } from 'react';
import { Button, Container, Row, Col } from 'react-bootstrap';
import { FaFacebookF, FaTwitter, FaInstagram } from 'react-icons/fa';
import { fetchRandomBooks } from '../api';
import BookCarousel from '../components/BookCarousel';
import HeroBanner from '../components/HeroBanner';
import Categories from '../components/Categories';
import '../styles/Home.css';


function Home() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchRandomBooks(5) // Se obtienen 5 libros aleatorios
            .then(data => {
                setBooks(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error al obtener libros aleatorios:', error);
                setLoading(false);
            });
    }, []);

    return (
        <div className="home-background">
            {/* Banner Principal */}
            <HeroBanner />

            {/* Libros Destacados */}
            <Container className="mt-5">
                <h2 className="section-title">Libros Destacados</h2>
                {loading ? (
                    <p>Cargando libros destacados...</p>
                ) : (
                    <Row>
                        {books.map(book => (
                            <Col key={book.id_libro} md={4} sm={6} className="mb-4">
                                <div className="card h-100">
                                    <img
                                        src={book.imagen_url || '/assets/images/placeholder.jpg'}
                                        alt={book.titulo}
                                        className="card-img-top"
                                    />
                                    <div className="card-body">
                                        <h5 className="card-title">{book.titulo}</h5>
                                        <p className="card-text">{book.descripcion || 'No hay descripción disponible.'}</p>
                                    </div>
                                </div>
                            </Col>
                        ))}
                    </Row>
                )}
            </Container>

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
            <footer className="footer-section">
                <Container>
                    <Row>
                        <Col md={3} sm={6}>
                            <h5>Conócenos</h5>
                            <ul>
                                <li><a href="#">Sobre Nosotros</a></li>
                                <li><a href="#">Historia</a></li>
                                <li><a href="#">Nuestro Equipo</a></li>
                                <li><a href="#">Carreras</a></li>
                            </ul>
                        </Col>
                        <Col md={3} sm={6}>
                            <h5>Servicio al Consumidor</h5>
                            <ul>
                                <li><a href="#">Contacto</a></li>
                                <li><a href="#">FAQ</a></li>
                                <li><a href="#">Envíos</a></li>
                                <li><a href="#">Devoluciones</a></li>
                            </ul>
                        </Col>
                        <Col md={3} sm={6}>
                            <h5>Redes Sociales</h5>
                            <ul>
                                <li><a href="#"><FaFacebookF /> Facebook</a></li>
                                <li><a href="#"><FaTwitter /> Twitter</a></li>
                                <li><a href="#"><FaInstagram /> Instagram</a></li>
                            </ul>
                        </Col>
                        <Col md={3} sm={6}>
                            <h5>Mi Cuenta</h5>
                            <ul>
                                <li><a href="/login">Iniciar Sesión</a></li>
                                <li><a href="/register">Registrarse</a></li>
                                <li><a href="/carrito">Carrito</a></li>
                            </ul>
                        </Col>
                    </Row>
                    <hr />
                    <Row>
                        <Col className="text-center">
                            <p>&copy; {new Date().getFullYear()} Biblioteca Virtual. Todos los derechos reservados.</p>
                        </Col>
                    </Row>
                </Container>
            </footer>
        </div>
    );
}

export default Home;

