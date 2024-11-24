import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import BookDetails from './pages/BookDetails';
import SearchResults from './pages/SearchResults';
import Header from './components/header';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/libros/:id_libro" element={<BookDetails />} />
        <Route path="/buscar" element={<SearchResults />} />
      </Routes>
    </Router>
  );
}

export default App;
