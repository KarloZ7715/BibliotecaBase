-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-11-2024 a las 23:14:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bibliotecaamz`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `registrar_accion` (IN `p_id_usuario` INT, IN `p_accion` VARCHAR(255), IN `p_detalles` TEXT)   BEGIN
    INSERT INTO registros (id_usuario, accion, fecha, hora, detalles)
    VALUES (p_id_usuario, p_accion, CURDATE(), CURTIME(), p_detalles);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autores`
--

CREATE TABLE `autores` (
  `id_autor` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `biografia` text DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `autores`
--

INSERT INTO `autores` (`id_autor`, `nombre`, `biografia`, `fecha_nacimiento`) VALUES
(1, 'Langston Hughes', 'Langston Hughes alcanzó fama como poeta durante el florecimiento de las artes conocido como el Renacimiento de Harlem, pero quienes lo etiquetan como \"un poeta del Renacimiento de Harlem\" han restringido su fama a un solo género y década.', '1902-02-01'),
(2, 'Dan Brown', 'Dan Brown es un autor estadounidense de ficción de suspenso, mejor conocido por la novela más vendida de 2003, El Código Da Vinci. Las novelas de Brown, que son búsquedas del tesoro ambientadas en un período de 24 horas, presentan temas recurrentes de criptografía, claves, símbolos, códigos y teorías de conspiración.', '1964-06-22'),
(3, 'Tui T. Sutherland', 'Tui T. Sutherland nació el 31 de julio de 1978 en Caracas, Venezuela. Su madre, que es de Nueva Zelanda, le puso el nombre del tui, un ave originaria de ese país. Sutherland vivió en Asunción, Paraguay; Miami, Florida; y Santo Domingo, República Dominicana; antes de mudarse a Nueva Jersey en la escuela secundaria. Mientras estaba en la escuela secundaria comenzó a hacer teatro,\nque consistió principalmente en trabajo detrás del escenario.', '1978-07-31'),
(4, 'James Fenimore Cooper', 'James Fenimore Cooper fue un prolífico y popular escritor estadounidense de principios del siglo XIX. Se le recuerda mejor como un novelista que escribió numerosas historias marinas y novelas históricas conocidas como Leatherstocking Tales, protagonizadas por el hombre de la frontera Natty Bumppo.', '1789-09-15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id_carrito` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_libro` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT 1,
  `fecha_agregado` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`) VALUES
(1, 'Acción'),
(4, 'Ciencia'),
(2, 'Ficción'),
(5, 'Tecnología'),
(3, 'Thriller');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `id_autor` int(11) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `isbn` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `descripcion`, `precio`, `stock`, `id_autor`, `id_categoria`, `imagen_url`, `fecha_publicacion`, `isbn`) VALUES
(1, 'Not without laughter', 'Esta es la historia de la mayoría de edad de un niño afroamericano en un pequeño pueblo de Kansas.', 55000.00, 5, 1, 2, 'https://ia800505.us.archive.org/view_archive.php?archive=/10/items/m_covers_0011/m_covers_0011_68.zip&file=0011688085-M.jpg', '1963-01-15', '00000000'),
(2, 'DIGITAL FORTRESS', 'Digital Fortress es una novela de suspenso escrita por el autor estadounidense Dan Brown y publicada en 1998 por St. Martin\'s Press. El libro explora el tema de la vigilancia gubernamental de la información almacenada electrónicamente sobre la vida privada de los ciudadanos, y las posibles libertades civiles y las implicaciones éticas del uso de dicha tecnología.', 35000.00, 7, 2, 3, 'https://covers.openlibrary.org/b/id/14542864-M.jpg', '2005-06-12', '9780593057445'),
(3, 'The Dark Secret', 'Como todos los dragoncitos del destino, Starflight siempre ha querido ver su hogar, pero también ha tenido miedo de sus compañeros NightWings. Starflight no tiene poderes para leer la mente como su tribu y no entiende por qué son tan reservados. Nadie ha visto nunca a la reina NightWing.', 45000.00, 3, 3, 2, 'https://covers.openlibrary.org/b/id/7436616-M.jpg', '2013-03-13', '545349214'),
(4, 'L\'ultimo dei Mohicani', 'La historia clásica de Hawkeye, Natty Bumppo, el explorador fronterizo que le dio la espalda a la \"civilización\" y su amistad con un guerrero mohicano mientras escoltan a dos hermanas a través del peligroso desierto del país indio en la frontera de Estados Unidos.', 28000.00, 8, 4, 2, 'https://covers.openlibrary.org/b/id/12139938-M.jpg', '1994-09-02', '8879836854');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_pedido` datetime DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_usuario`, `total`, `fecha_pedido`, `estado`) VALUES
(1, 1, 55000.00, '2024-11-21 00:00:00', 'Completado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros`
--

CREATE TABLE `registros` (
  `id_registro` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `accion` varchar(255) DEFAULT NULL,
  `detalles` text DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `hora` time DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `registros`
--

INSERT INTO `registros` (`id_registro`, `id_usuario`, `accion`, `detalles`, `fecha`, `hora`) VALUES
(1, 1, 'Actualización', 'Usuario Carlos actualizado', '2024-11-21 00:00:00', '14:06:07'),
(2, 1, 'Inserción', 'Categoría Ciencia agregada correctamente', '2024-11-21 00:00:00', '14:21:05'),
(3, 1, 'Inserción', 'Categoría Tecnología agregada correctamente', '2024-11-21 00:00:00', '14:21:28'),
(4, 1, 'Actualización', 'Estado del pedido 1 actualizado', '2024-11-22 00:00:00', '14:22:55'),
(5, 1, 'Actualización', 'Libro DIGITAL FORTRESS actualizado correctamente', '2024-11-21 00:00:00', '14:23:22'),
(6, 1, 'Actualización', 'Usuario Admin actualizado', '2024-11-21 00:00:00', '14:24:47'),
(7, 1, 'Inserción', 'Usuario Vicky agregado', '2024-11-21 00:00:00', '14:48:21'),
(8, 1, 'Actualización', 'Usuario Vicky actualizado', '2024-11-21 00:00:00', '14:49:44'),
(9, 1, 'Inserción', 'Autor Tui T. Sutherland agregado correctamente', '2024-11-21 00:00:00', '15:07:32'),
(10, 1, 'Inserción', 'Libro The Dark Secret agregado correctamente', '2024-11-24 00:00:00', '15:08:48'),
(11, 1, 'Actualización', 'Libro The Dark Secret actualizado correctamente', '2024-11-22 00:00:00', '15:10:41'),
(12, 1, 'Actualización', 'Estado del pedido 1 actualizado', '2024-11-21 00:00:00', '15:14:53'),
(13, 1, 'Actualización', 'Autor Tui T. Sutherland actualizado', '2024-11-21 00:00:00', '15:16:02'),
(14, 1, 'Actualización', 'Autor Tui T. Sutherland actualizado', '2024-11-22 00:00:00', '15:16:28'),
(15, 1, 'Actualización', 'Autor Tui T. Sutherland actualizado', '2024-11-21 00:00:00', '15:16:34'),
(16, 1, 'Actualización', 'Usuario Vicky actualizado', '2024-11-21 00:00:00', '21:32:55'),
(17, 1, 'Actualización', 'Estado del pedido 1 actualizado', '2024-11-21 00:00:00', '21:54:48'),
(18, 1, 'Actualización', 'Usuario Vicky actualizado', '2024-11-26 00:00:00', '22:54:06'),
(19, 1, 'Actualización', 'Usuario Maria actualizado', '2024-11-21 00:00:00', '22:58:42'),
(20, 1, 'Actualización', 'Usuario Admin actualizado', '2024-11-21 00:00:00', '23:08:18'),
(21, 1, 'Actualización', 'Usuario Maria actualizado', '2024-11-21 00:00:00', '23:08:39'),
(22, 1, 'Eliminación', 'Usuario Maria eliminado', '2024-11-21 00:00:00', '23:08:53'),
(23, 1, 'Actualización', 'Usuario Admin actualizado', '2024-11-21 00:00:00', '23:21:23'),
(24, 1, 'Actualización', 'Usuario Admin actualizado', '2024-11-23 00:00:00', '14:26:24'),
(25, 1, 'Actualización', 'Estado del pedido 1 actualizado', '2024-11-23 00:00:00', '14:30:30'),
(26, 1, 'Inserción', 'Usuario Luis agregado', '2024-11-23 00:00:00', '15:43:28'),
(27, 1, 'Inserción', 'Autor James Fenimore Cooper agregado correctamente', '2024-11-23 00:00:00', '15:45:33'),
(28, 1, 'Actualización', 'Libro Not without laughter actualizado correctamente', '2024-11-23 00:00:00', '15:47:20'),
(29, 1, 'Actualización', 'Libro L\'ultimo dei Mohicani actualizado correctamente', '2024-11-23 00:00:00', '15:47:58'),
(30, 1, 'Actualización', 'Libro L\'ultimo dei Mohicani actualizado correctamente', '2024-11-23 00:00:00', '15:48:08'),
(31, 1, 'Actualización', 'Autor Tui T. Sutherland actualizado', '2024-11-23 00:00:00', '16:22:28');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarjetas`
--

CREATE TABLE `tarjetas` (
  `id_tarjeta` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `numero_tarjeta` varchar(20) DEFAULT NULL,
  `fecha_expiracion` date DEFAULT NULL,
  `tipo` varchar(10) DEFAULT NULL,
  `nombre_titular` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `rol` enum('admin','cliente') NOT NULL DEFAULT 'cliente',
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `direccion` text DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `rol`, `nombre`, `correo`, `contraseña`, `direccion`, `telefono`, `fecha_registro`) VALUES
(1, 'admin', 'Admin', 'exp@exp.com', '1234', 'Cl6 #6-667', '555222666', '2024-11-21 00:27:14'),
(4, 'admin', 'Luis', 'ejemplo@exp.com', '12345', '22 #2-32', '551112223', '2024-11-23 15:43:28');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `valoraciones`
--

CREATE TABLE `valoraciones` (
  `id_valoracion` int(11) NOT NULL,
  `id_libro` int(11) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `valoracion` int(11) DEFAULT NULL CHECK (`valoracion` between 1 and 5),
  `fecha_valoracion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `autores`
--
ALTER TABLE `autores`
  ADD PRIMARY KEY (`id_autor`);

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id_carrito`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_libro` (`id_libro`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`),
  ADD UNIQUE KEY `nombre_categoria` (`nombre_categoria`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`),
  ADD KEY `id_autor` (`id_autor`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `registros`
--
ALTER TABLE `registros`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `tarjetas`
--
ALTER TABLE `tarjetas`
  ADD PRIMARY KEY (`id_tarjeta`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  ADD PRIMARY KEY (`id_valoracion`),
  ADD KEY `id_libro` (`id_libro`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `autores`
--
ALTER TABLE `autores`
  MODIFY `id_autor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarjetas`
--
ALTER TABLE `tarjetas`
  MODIFY `id_tarjeta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  MODIFY `id_valoracion` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`);

--
-- Filtros para la tabla `libros`
--
ALTER TABLE `libros`
  ADD CONSTRAINT `libros_ibfk_1` FOREIGN KEY (`id_autor`) REFERENCES `autores` (`id_autor`),
  ADD CONSTRAINT `libros_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `registros`
--
ALTER TABLE `registros`
  ADD CONSTRAINT `registros_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `tarjetas`
--
ALTER TABLE `tarjetas`
  ADD CONSTRAINT `tarjetas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  ADD CONSTRAINT `valoraciones_ibfk_1` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`),
  ADD CONSTRAINT `valoraciones_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
