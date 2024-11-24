import React, { useState } from 'react';
import { Form, FormControl, Button } from 'react-bootstrap';
import { FaSearch, FaShoppingCart, FaUser } from 'react-icons/fa';
import '../styles/SearchBar.css';
import { useNavigate } from 'react-router-dom';

function SearchBar() {
    const [filter, setFilter] = useState('Todo');
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

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
                    <Button variant="outline-success" className="search-button">
                        <FaSearch />
                    </Button>
                </div>
            </Form>
            <div className="d-flex">
                <Button variant="outline-secondary" className="me-2 btn-white">
                    <FaShoppingCart />
                </Button>
                <Button variant="outline-secondary" className="btn-white">
                    <FaUser />
                </Button>
            </div>
        </div>
    );
}

export default SearchBar;