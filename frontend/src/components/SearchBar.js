import React, { useState, useContext } from 'react';
import { Form, FormControl, Button } from 'react-bootstrap';
import { FaSearch, FaShoppingCart, FaUser } from 'react-icons/fa';
import '../styles/SearchBar.css';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { CartContext } from '../contexts/CartContext';
import { motion, AnimatePresence } from 'framer-motion';

function SearchBar() {
    const [filter, setFilter] = useState('Todo');
    const [query, setQuery] = useState('');
    const navigate = useNavigate();
    const { cartItems } = useContext(CartContext);
    const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
    const { isAuthenticated } = useContext(AuthContext);
    const handleSubmit = (e) => {
        e.preventDefault();
        navigate(`/buscar?filter=${filter}&query=${encodeURIComponent(query)}`)
    };

    return (
        <div className="d-flex align-items-center justify-content-center w-100">
            <Form className="d-flex mx-auto" style={{ maxWidth: '600px', width: '100%' }} onSubmit={handleSubmit}>
                <div className="input-group">
                    <Form.Select
                        aria-label="Filtro de búsqueda"
                        className="filter-select"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option>Todo</option>
                        <option>Título</option>
                        <option>Autor</option>
                        <option>Género</option>
                    </Form.Select>
                    <FormControl
                        type="search"
                        placeholder="Buscar libros..."
                        aria-label="Search"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <Button variant="outline-success" className="search-button" type="submit">
                        <FaSearch />
                    </Button>
                </div>
            </Form>
            <div className="d-flex">
                <Link to="/carrito" className="cart-link" aria-label={`Carrito de compras con ${totalItems} ítems`}>
                    <Button variant="outline-secondary" className="me-2 btn-cart">
                        <FaShoppingCart />
                        <AnimatePresence>
                            {totalItems > 0 && (
                                <motion.span
                                    className="cart-badge"
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    exit={{ scale: 0 }}
                                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                                >
                                    {totalItems}
                                </motion.span>
                            )}
                        </AnimatePresence>
                    </Button>
                </Link>
                {isAuthenticated ? (
                    <Link to="/perfil">
                        <Button variant="outline-secondary" className="btn-user">
                            <FaUser />
                        </Button>
                    </Link>
                ) : (
                    <Link to="/login">
                        <Button variant="outline-secondary" className="btn-user">
                            <FaUser />
                        </Button>
                    </Link>
                )}
            </div>
        </div>
    );
}

export default SearchBar;