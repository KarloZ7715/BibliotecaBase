import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { FaFacebookF, FaTwitter, FaInstagram } from 'react-icons/fa';
import '../styles/Home.css';

function Footer() {
    return (
        <footer className="footer-section">
            <Container>
                <Row>
                    <Col md={3} sm={6}>
                        <h5>Conócenos</h5>
                        <ul>
                            <li><a href="#">Sobre Nosotros</a></li>
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
    );
}

export default Footer;