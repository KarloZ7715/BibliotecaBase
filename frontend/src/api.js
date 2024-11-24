import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const fetchRandomBooks = async (limit) => {
    try {
        const response = await fetch(`http://localhost:8000/libros/random?limit=${limit}`);
        if (!response.ok) {
            throw new Error('Error al obtener libros aleatorios');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        throw error;
    }
};