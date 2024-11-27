import React, { useEffect, useState } from "react";
import { fetchBooks } from "../api";
import { Link } from "react-router-dom";
import Footer from "../components/Footer";

function BookList() {
    const [books, setBooks] = useState([]);

    useEffect(() => {
        fetchBooks()
            .then((response) => setBooks(response.data))
            .catch((error) => console.error(error));
    }, []);

    return (
        <div className="container mt-5">
            <h1>Lista de libros</h1>
            <ul className="list-group">
                {books.map(book => (
                    <li key={book.id_libro} className="list-group-item">
                        <Link to={`/libros/${book.id_libro}`}>{book.título}</Link>
                    </li>
                ))}
            </ul>
            <Footer />
        </div>
    );
}

export default BookList;