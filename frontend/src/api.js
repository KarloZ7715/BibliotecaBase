import axios from "axios";

const API_URL = "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

export const loginUsuario = async ({ correo, contraseña }) => {
  try {
    const response = await axiosInstance.post("/auth/login", {
      correo,
      contraseña,
    });
    return response.data;
  } catch (error) {
    console.error("Error en loginUsuario:", error);
    throw error;
  }
};

export const registrarUsuario = async ({
  nombre,
  correo,
  contraseña,
  direccion,
  telefono,
}) => {
  try {
    const response = await axiosInstance.post("/auth/registrar", {
      nombre,
      correo,
      contraseña,
      direccion,
      telefono,
    });
    return response.data;
  } catch (error) {
    console.error("Error en registrarUsuario:", error);
    throw error;
  }
};

export const obtenerUsuarioActual = async () => {
  try {
    const response = await axiosInstance.get("/auth/me");
    return response.data;
  } catch (error) {
    console.error("Error al obtener usuario actual:", error);
    throw error;
  }
};

export const logoutUsuario = async () => {
  try {
    const response = await axiosInstance.post("/auth/logout");
    return response.data;
  } catch (error) {
    console.error("Error al cerrar sesión:", error);
    throw error;
  }
};

export const obtenerCarrito = async () => {
  const response = await axiosInstance.get("/carrito/");
  return response.data;
};

export const agregarAlCarrito = async (id_libro) => {
  const response = await axiosInstance.post("/carrito/agregar", null, {
    params: { id_libro },
  });
  return response.data;
};

export const actualizarCantidadCarrito = async (id_libro, cantidad) => {
  const response = await axiosInstance.put("/carrito/actualizar", null, {
    params: { id_libro, cantidad },
  });
  return response.data;
};

export const eliminarDelCarrito = async (id_libro) => {
  const response = await axiosInstance.delete("/carrito/eliminar", {
    params: { id_libro },
  });
  return response.data;
};

export const vaciarCarrito = async () => {
  const response = await axiosInstance.delete("/carrito/vaciar");
  return response.data;
};

export const fetchRandomBooks = async (limit) => {
  try {
    const response = await axiosInstance.get(`/libros/random?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener libros aleatorios:", error);
    throw error;
  }
};

export const fetchFeaturedBooks = async () => {
  try {
    const response = await axiosInstance.get("/libros/destacados");
    return response.data;
  } catch (error) {
    console.error("Error al obtener libros destacados:", error);
    throw error;
  }
};

export const fetchBooksByGenre = async (genre) => {
  try {
    const response = await axiosInstance.get("/libros/buscar", {
      params: { query: genre, filter: "Género" },
    });
    return response.data;
  } catch (error) {
    console.error(`Error al obtener libros de ${genre}:`, error);
    throw error;
  }
};
