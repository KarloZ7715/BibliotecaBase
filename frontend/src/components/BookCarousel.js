import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import { Card, Spinner, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { fetchRandomBooks } from '../api';
import '../styles/BookCarousel.css';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function BookCarousel({ title, limit = 6 }) {
    const [libros, setLibros] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchLibros = async () => {
            try {
                const data = await fetchRandomBooks(limit);
                setLibros(data);
            } catch (err) {
                setError('Error al cargar libros');
            } finally {
                setLoading(false);
            }
        };
        fetchLibros();
    }, [limit]);

    if (loading)
        return (
            <div className="d-flex justify-content-center my-4">
                <Spinner animation="border" />
            </div>
        );

    if (error)
        return (
            <Alert variant="danger" className="text-center my-4">
                {error}
            </Alert>
        );

    if (libros.length === 0)
        return (
            <Alert variant="info" className="text-center my-4">
                No hay libros para mostrar.
            </Alert>
        );

    const settings = {
        dots: false,
        infinite: true,
        speed: 300,
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: true,
        nextArrow: <SampleNextArrow />,
        prevArrow: <SamplePrevArrow />,
    };

    return (
        <div className="book-carousel">
            {title && <h2 className="book-section-title">{title}</h2>}
            <Slider {...settings}>
                {libros.map((libro) => (
                    <div key={libro.id_libro} className="slick-slide">
                        <Card className="carousel-card">
                            <Link to={`/libros/${libro.id_libro}`} className="carousel-link">
                                <Card.Img
                                    variant="top"
                                    src={libro.imagen_url || '/assets/images/placeholder.jpg'}
                                    alt={libro.titulo}
                                    className="carousel-img"
                                />
                                <Card.Body>
                                    <Card.Title>{libro.titulo}</Card.Title>
                                    <Card.Text>
                                        Por {libro.autor ? libro.autor.nombre : 'Autor Desconocido'}
                                    </Card.Text>
                                </Card.Body>
                            </Link>
                        </Card>
                    </div>
                ))}
            </Slider>
        </div>
    );
}

function SampleNextArrow(props) {
    const { className, style, onClick } = props;
    return (
        <div
            className={className}
            style={{ ...style, display: "block", right: "50px", zIndex: 1 }}
            onClick={onClick}
        />
    );
}

function SamplePrevArrow(props) {
    const { className, style, onClick } = props;
    return (
        <div
            className={className}
            style={{ ...style, display: "block", left: "50px", zIndex: 1 }}
            onClick={onClick}
        />
    );
}

export default BookCarousel;