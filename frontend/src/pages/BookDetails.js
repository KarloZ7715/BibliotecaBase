import React, { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Container,
  Row,
  Col,
  Image,
  Button,
  Spinner,
  Alert,
  Modal,
  Form,
} from "react-bootstrap";
import { CartContext } from "../contexts/CartContext";
import { AuthContext } from "../contexts/AuthContext";
import ReactStars from "react-stars";
import axios from "axios";
import { motion } from "framer-motion";
import "../styles/BookDetails.css";
import Footer from "../components/Footer";

function BookDetails() {
  const { id } = useParams();
  const { addToCart } = useContext(CartContext);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [valoraciones, setValoraciones] = useState([]);
  const [promedioValoracion, setPromedioValoracion] = useState(0);
  const [userValoracion, setUserValoracion] = useState(null);
  const [canRate, setCanRate] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [ratingValue, setRatingValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const fetchBookDetails = async () => {
      try {
        const bookResponse = await axios.get(
          `http://localhost:8000/libros/${id}`
        );
        setBook(bookResponse.data);

        const valoracionesResponse = await axios.get(
          `http://localhost:8000/valoraciones/libro/${id}`
        );
        setValoraciones(valoracionesResponse.data);

        if (valoracionesResponse.data.length > 0) {
          const suma = valoracionesResponse.data.reduce(
            (acc, val) => acc + val.valoracion,
            0
          );
          const promedio = suma / valoracionesResponse.data.length;
          setPromedioValoracion(promedio);
        } else {
          setPromedioValoracion(0);
        }

        if (user) {
          const pedidosResponse = await axios.get(
            "http://localhost:8000/pedidos/",
            { withCredentials: true }
          );

          const haComprado = pedidosResponse.data.some(
            (pedido) =>
              pedido.detallepedido?.some(
                (detalle) => Number(detalle.id_libro) === Number(id)
              ) || false
          );
          setCanRate(haComprado);

          if (haComprado) {
            const valoracionUsuario = valoracionesResponse.data.find(
              (val) => val.id_usuario === user.id_usuario
            );
            setUserValoracion(valoracionUsuario || null);
          }
        }
      } catch (err) {
        console.error(err);
        setError("Error al cargar los detalles del libro");
      } finally {
        setLoading(false);
      }
    };
    fetchBookDetails();
  }, [id, user]);

  const handleAddToCart = () => {
    addToCart(book);
  };

  const handleBuyNow = () => {
    addToCart(book);
    navigate("/carrito");
  };

  const openRatingModal = () => {
    if (userValoracion) {
      setRatingValue(userValoracion.valoracion);
      setIsEditing(true);
    } else {
      setRatingValue(0);
      setIsEditing(false);
    }
    setShowRatingModal(true);
  };

  const closeRatingModal = () => {
    setShowRatingModal(false);
    setRatingValue(0);
    setIsEditing(false);
  };

  const handleRatingChange = (newRating) => {
    setRatingValue(newRating);
  };

  const submitRating = async () => {
    if (ratingValue < 1 || ratingValue > 5) {
      alert("La valoración debe estar entre 1 y 5 estrellas.");
      return;
    }

    try {
      if (isEditing && userValoracion) {
        await axios.put(
          `http://localhost:8000/valoraciones/${userValoracion.id_valoracion}`,
          {
            id_libro: parseInt(id),
            valoracion: ratingValue,
          },
          { withCredentials: true }
        );
        setValoraciones((prev) =>
          prev.map((val) =>
            val.id_valoracion === userValoracion.id_valoracion
              ? { ...val, valoracion: ratingValue }
              : val
          )
        );
        setUserValoracion({ ...userValoracion, valoracion: ratingValue });
      } else {
        const response = await axios.post(
          "http://localhost:8000/valoraciones/",
          {
            id_libro: parseInt(id),
            valoracion: ratingValue,
          },
          { withCredentials: true }
        );
        setValoraciones((prev) => [...prev, response.data]);
        setUserValoracion(response.data);
      }

      const suma =
        (isEditing
          ? valoraciones.reduce((acc, val) => acc + val.valoracion, 0) -
            userValoracion.valoracion
          : valoraciones.reduce((acc, val) => acc + val.valoracion, 0)) +
        ratingValue;
      const count = isEditing ? valoraciones.length : valoraciones.length + 1;
      setPromedioValoracion(suma / count);

      closeRatingModal();
    } catch (err) {
      console.error(err);
      alert("Error al enviar la valoración.");
    }
  };

  const deleteRating = async () => {
    if (!userValoracion) return;

    try {
      await axios.delete(
        `http://localhost:8000/valoraciones/${userValoracion.id_valoracion}`,
        { withCredentials: true }
      );
      setValoraciones((prev) =>
        prev.filter((val) => val.id_valoracion !== userValoracion.id_valoracion)
      );
      setUserValoracion(null);

      const suma =
        valoraciones.reduce((acc, val) => acc + val.valoracion, 0) -
        userValoracion.valoracion;
      const count = valoraciones.length - 1;
      setPromedioValoracion(count > 0 ? suma / count : 0);

      closeRatingModal();
    } catch (err) {
      console.error(err);
      alert("Error al eliminar la valoración.");
    }
  };

  if (loading) return <Spinner animation="border" />;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (!book) return <Alert variant="info">Libro no encontrado</Alert>;

  return (
    <div>
      <Container className="book-details-page mt-4">
        <Row>
          <Col md={4}>
            <Image
              src={book.imagen_url || "/assets/images/placeholder.jpg"}
              alt={book.titulo}
              fluid
            />

            <div className="valoraciones image-valoraciones mt-4">
              <h4>Valoraciones</h4>
              <div className="d-flex align-items-center mb-2">
                <ReactStars
                  count={5}
                  value={promedioValoracion}
                  size={24}
                  color2={"#ffd700"}
                  edit={false}
                />
                <span className="ms-2">
                  {promedioValoracion.toFixed(2)} ({valoraciones.length}{" "}
                  valoraciones)
                </span>
              </div>

              {valoraciones.length > 0 ? (
                valoraciones.slice(0, 3).map((val) => (
                  <div key={val.id_valoracion} className="mb-3">
                    <div className="d-flex align-items-center">
                      <strong>{val.usuario.nombre}</strong>
                      <ReactStars
                        count={5}
                        value={val.valoracion}
                        size={20}
                        color2={"#ffd700"}
                        edit={false}
                      />
                    </div>
                    <small className="text-muted">
                      {new Date(val.fecha_valoracion).toLocaleDateString()}
                    </small>
                  </div>
                ))
              ) : (
                <p>No hay valoraciones para este libro.</p>
              )}

              {valoraciones.length > 3 && (
                <Button
                  variant="link"
                  onClick={() => navigate(`/libros/${id}/valoraciones`)}
                >
                  Ver todas las valoraciones
                </Button>
              )}

              {user && canRate && (
                <Button
                  variant="outline-primary"
                  onClick={openRatingModal}
                  className="mt-3 add-rating-btn"
                >
                  {userValoracion ? "Editar Valoración" : "Agregar Valoración"}
                </Button>
              )}
            </div>
          </Col>
          <Col md={8}>
            <h2>{book.titulo}</h2>
            <p>
              <strong>Autor:</strong>{" "}
              {book.autor ? book.autor.nombre : "Autor Desconocido"}
            </p>
            <p>
              <strong>Descripción:</strong>{" "}
              {book.descripcion || "No descripción disponible"}
            </p>
            <div className="book-details">
              <p>
                <strong>Categoría:</strong>{" "}
                {book.categoria
                  ? book.categoria.nombre_categoria
                  : "Sin categoría"}
              </p>
              <p className="price">
                <strong>Precio:</strong> ${book.precio.toFixed(2)}
              </p>
              <p className="stock">
                <strong>Stock:</strong>{" "}
                {book.stock > 0 ? (
                  <span style={{ color: "green", fontSize: "0.8rem" }}>
                    Disponible
                  </span>
                ) : (
                  <span style={{ color: "red", fontSize: "0.8rem" }}>
                    Agotado
                  </span>
                )}
              </p>
              <p>
                <strong>Fecha de Publicación:</strong>{" "}
                {book.fecha_publicacion || "Desconocida"}
              </p>
              <p>
                <strong>ISBN:</strong> {book.isbn || "No disponible"}
              </p>
            </div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="motion-div-btn"
            >
              <Button
                variant="success"
                onClick={handleAddToCart}
                className="shop_btn mt-4"
              >
                Agregar al Carrito
              </Button>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="motion-div-btn mt-3"
            >
              <Button
                variant="primary"
                onClick={handleBuyNow}
                className="shop_btn"
              >
                Comprar Ahora
              </Button>
            </motion.div>
          </Col>
        </Row>

        <Modal show={showRatingModal} onHide={closeRatingModal} centered>
          <Modal.Header closeButton>
            <Modal.Title>
              {isEditing ? "Editar Valoración" : "Agregar Valoración"}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group controlId="rating">
                <Form.Label>Tu Valoración</Form.Label>
                <ReactStars
                  count={5}
                  value={ratingValue}
                  size={40}
                  half={false}
                  color2={"#ffd700"}
                  onChange={handleRatingChange}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            {isEditing && (
              <Button
                variant="danger"
                onClick={deleteRating}
                className="delete-rating-btn"
              >
                Eliminar Valoración
              </Button>
            )}
            <Button
              variant="secondary"
              onClick={closeRatingModal}
              className="cancel-rating-btn"
            >
              Cancelar
            </Button>
            <Button
              variant="primary"
              onClick={submitRating}
              className="submit-rating-btn"
            >
              {isEditing ? "Guardar Cambios" : "Enviar Valoración"}
            </Button>
          </Modal.Footer>
        </Modal>
      </Container>
      <Footer />
    </div>
  );
}

export default BookDetails;
