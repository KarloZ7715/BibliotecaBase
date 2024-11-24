import React, { useEffect, useState } from 'react';
import { Navbar, Button, Container, Row, Col, Carousel } from 'react-bootstrap';
import { FaFacebookF, FaTwitter, FaInstagram } from 'react-icons/fa';
import BookCarousel from '../components/BookCarousel';
import '../styles/Home.css';
import { fetchRandomBooks } from '../api';

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
            <section className="hero-section">
                <Carousel>
                    <Carousel.Item>
                        <img
                            className="d-block w-100"
                            src="ruta/a/tu/imagen1.jpg"
                            alt="Primera promoción"
                        />
                        <Carousel.Caption>
                            <h3>Nueva Colección de Fantasía</h3>
                            <p>Descubre los mundos mágicos más recientes.</p>
                            <Button variant="primary">Explorar</Button>
                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item>
                        <img
                            className="d-block w-100"
                            src="ruta/a/tu/imagen2.jpg"
                            alt="Segunda promoción"
                        />
                        <Carousel.Caption>
                            <h3>Best Sellers del Mes</h3>
                            <p>Los libros más vendidos que no te puedes perder.</p>
                            <Button variant="primary">Ver Más</Button>
                        </Carousel.Caption>
                    </Carousel.Item>
                </Carousel>
            </section>

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

            {/* Categorías */}
            <Container className="mt-5">
                <h2 className="section-title">Categorías</h2>
                <Row>
                    <Col md={3} sm={6} className="category-card">
                        <img src="ruta/a/categoria1.jpg" alt="Categoría 1" className="category-image" />
                        <h5>Ficción</h5>
                    </Col>
                    <Col md={3} sm={6} className="category-card">
                        <img src="ruta/a/categoria2.jpg" alt="Categoría 2" className="category-image" />
                        <h5>Acción</h5>
                    </Col>
                    <Col md={3} sm={6} className="category-card">
                        <img src="ruta/a/categoria3.jpg" alt="Categoría 3" className="category-image" />
                        <h5>Biografías</h5>
                    </Col>
                    <Col md={3} sm={6} className="category-card">
                        <img src="ruta/a/categoria4.jpg" alt="Categoría 4" className="category-image" />
                        <h5>Ciencia</h5>
                    </Col>
                </Row>
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

            <BookCarousel title="Otro Set de Libros Destacados" limit={5} />

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
                                <li><a href="#">Iniciar Sesión</a></li>
                                <li><a href="#">Registrarse</a></li>
                                <li><a href="#">Carrito</a></li>
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

