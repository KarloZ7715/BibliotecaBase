import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import SearchBar from './SearchBar';
import { Link } from 'react-router-dom';

function Header() {
    return (
        <Navbar bg="primary" expand="lg" className="shadow-sm mb-4">
            <Container className="d-flex justify-content-between align-items-center">
                <Navbar.Brand as={Link} to="/" className="text-white">
                    Biblioteca Virtual
                </Navbar.Brand>
                <SearchBar />
            </Container>
        </Navbar>
    );
}

export default Header;