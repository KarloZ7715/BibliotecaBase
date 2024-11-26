import axios from 'axios';

const API_URL = 'http://localhost:8000';

const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});

export const loginUsuario = async ({ correo, contraseña }) => {
    try {
        const response = await axiosInstance.post('/auth/login', { correo, contraseña });
        return response.data;
    } catch (error) {
        console.error('Error en loginUsuario:', error);
        throw error;
    }
};

export const registrarUsuario = async ({ nombre, correo, contraseña, direccion, telefono }) => {
    try {
        const response = await axiosInstance.post('/auth/registrar', { nombre, correo, contraseña, direccion, telefono });
        return response.data;
    } catch (error) {
        console.error('Error en registrarUsuario:', error);
        throw error;
    }
};

export const obtenerUsuarioActual = async () => {
    try {
        const response = await axiosInstance.get('/auth/me');
        return response.data;
    } catch (error) {
        console.error('Error al obtener usuario actual:', error);
        throw error;
    }
};

export const logoutUsuario = async () => {
    try {
        const response = await axiosInstance.post('/auth/logout');
        return response.data;
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        throw error;
    }
};

export const fetchRandomBooks = async (limit) => {
    try {
        const response = await axiosInstance.get(`/libros/random?limit=${limit}`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener libros aleatorios:', error);
        throw error;
    }
};