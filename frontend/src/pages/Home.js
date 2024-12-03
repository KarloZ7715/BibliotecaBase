import React, { useEffect, useState } from "react";
import {
  Button,
  Container,
  Row,
  Col,
  Card,
  Spinner,
  Alert,
} from "react-bootstrap";
import { fetchFeaturedBooks, fetchBooksByGenre } from "../api";
import BookCarousel from "../components/BookCarousel";
import HeroBanner from "../components/HeroBanner";
import Categories from "../components/Categories";
import Footer from "../components/Footer";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";
import AOS from "aos";
import "aos/dist/aos.css";

function Home() {
  const [featuredBooks, setFeaturedBooks] = useState([]);
  const [loadingFeatured, setLoadingFeatured] = useState(true);
  const [loadingGenres, setLoadingGenres] = useState({
    Ficción: true,
    Romance: true,
    Biografías: true,
  });
  const [booksByGenre, setBooksByGenre] = useState({
    Ficción: [],
    Romance: [],
    Biografías: [],
  });
  const navigate = useNavigate();

  useEffect(() => {
    fetchFeaturedBooks()
      .then((data) => {
        setFeaturedBooks(data);
        setLoadingFeatured(false);
      })
      .catch((error) => {
        console.error("Error al obtener libros destacados:", error);
        setLoadingFeatured(false);
      });

    const genres = ["Ficción", "Romance", "Biografías"];
    genres.forEach((genre) => {
      fetchBooksByGenre(genre)
        .then((data) => {
          setBooksByGenre((prev) => ({ ...prev, [genre]: data.slice(0, 3) }));
          setLoadingGenres((prev) => ({ ...prev, [genre]: false }));
        })
        .catch((error) => {
          console.error(`Error al obtener libros de ${genre}:`, error);
          setLoadingGenres((prev) => ({ ...prev, [genre]: false }));
        });
    });

    AOS.init({
      duration: 1000,
      once: true,
    });
  }, []);

  const handleCardClick = (id_libro) => {
    navigate(`/libros/${id_libro}`);
  };

  const renderGenreSection = (genre) => (
    <section
      className="recommended-books-section"
      data-aos="fade-up"
      key={genre}
    >
      <h2 className="section-title">{genre}</h2>
      {loadingGenres[genre] ? (
        <div className="loading-spinner">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Cargando...</span>
          </Spinner>
        </div>
      ) : booksByGenre[genre].length > 0 ? (
        <Row>
          {booksByGenre[genre].map((book) => (
            <Col
              key={book.id_libro}
              md={4}
              sm={6}
              className="mb-4"
              data-aos="zoom-in"
            >
              <Card
                className="fade-in recommended-card"
                onClick={() => handleCardClick(book.id_libro)}
              >
                <Card.Img
                  variant="top"
                  src={book.imagen_url || "/assets/images/placeholder.jpg"}
                  className="card-img-top"
                />
                <Card.Body>
                  <Card.Title className="card-title">{book.titulo}</Card.Title>
                  <Card.Text className="card-text">
                    Autor:{" "}
                    {book.autor ? book.autor.nombre : "Autor Desconocido"}
                  </Card.Text>
                  <Card.Text className="card-text">
                    Precio: ${book.precio.toFixed(2)}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      ) : (
        <Alert variant="info" className="text-center my-4">
          No hay libros para mostrar en este género.
        </Alert>
      )}
    </section>
  );

  return (
    <div className="home-background">
      {/* Banner Principal */}
      <HeroBanner />

      {/* Libros Destacados */}
      <section className="featured-books-section" data-aos="fade-up">
        <h2 className="section-title">Libros Destacados</h2>
        {loadingFeatured ? (
          <div className="loading-spinner">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Cargando...</span>
            </Spinner>
          </div>
        ) : (
          <Row>
            {featuredBooks.map((book) => (
              <Col
                key={book.id_libro}
                md={3}
                sm={6}
                className="mb-4"
                data-aos="zoom-in"
              >
                <Card
                  className="fade-in featured-card"
                  onClick={() => handleCardClick(book.id_libro)}
                >
                  <Card.Img
                    variant="top"
                    src={book.imagen_url || "/assets/images/placeholder.jpg"}
                    className="card-img-top"
                  />
                  <Card.Body>
                    <Card.Title className="card-title">
                      {book.titulo}
                    </Card.Title>
                    <Card.Text className="card-text">
                      Autor:{" "}
                      {book.autor ? book.autor.nombre : "Autor Desconocido"}
                    </Card.Text>
                    <Card.Text className="card-text">
                      Precio: ${book.precio.toFixed(2)}
                    </Card.Text>
                    <Button
                      variant="success"
                      className="btn-shop"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCardClick(book.id_libro);
                      }}
                    >
                      Comprar Ahora
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </section>

      {/* Libros Recomendados por Género */}
      {["Ficción", "Romance", "Biografías"].map((genre) =>
        renderGenreSection(genre)
      )}

      {/* Componentes de Carrusel de Libros */}
      <BookCarousel title="¿Quieres más libros?" limit={20} />

      {/* Categorías */}
      <Categories />

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default Home;
