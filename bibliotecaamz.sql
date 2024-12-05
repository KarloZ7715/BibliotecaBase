-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-12-2024 a las 08:19:18
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
(4, 'James Fenimore Cooper', 'James Fenimore Cooper fue un prolífico y popular escritor estadounidense de principios del siglo XIX. Se le recuerda mejor como un novelista que escribió numerosas historias marinas y novelas históricas conocidas como Leatherstocking Tales, protagonizadas por el hombre de la frontera Natty Bumppo.', '1789-09-15'),
(5, 'Robert Greene', 'Robert Greene (nacido el 14 de mayo de 1959) es un autor estadounidense conocido por sus libros sobre estrategia, poder y seducción. Ha escrito seis bestsellers internacionales: Las 48 leyes del poder, El arte de la seducción, Las 33 estrategias de la guerra, La ley 50 (con el rapero 50 Cent), Maestría y Las leyes de la naturaleza humana.', '1959-04-14'),
(6, 'Morgan Housel', '', '1999-10-01'),
(7, 'George R. R. Martin', 'George Raymond Richard Martin (nacido el 20 de septiembre de 1948), a veces denominado GRRM, es un autor y guionista estadounidense de fantasía, terror y ciencia ficción. Es mejor conocido por su serie de novelas de fantasía épica Canción de hielo y fuego.\n\nLos críticos han descrito el trabajo de Martin como oscuro y cínico. Su primera novela, La muerte de la luz,\nmarcó la pauta para la mayor parte de su trabajo futuro; está ubicado en un planeta mayoritariamente abandonado que poco a poco se está volviendo inhabitable a medida que se aleja de su sol.', '1948-09-20'),
(8, 'Rithvik Singh', '', '1975-06-21'),
(9, 'Robert T. Kiyosaki', '', '1947-03-08'),
(10, 'Gregory Maguire', '', '1962-04-13'),
(11, 'H. D. Cartlon', '', '1983-06-17'),
(12, 'Patrick King', '', '1972-03-21'),
(13, 'Paulo Coelho', 'Paulo Coelho, nacido y criado en Río de Janeiro, Brasil, es un novelista brasileño conocido por emplear un rico simbolismo en sus descripciones de los viajes, a menudo espiritualmente motivados, de sus personajes. Coelho abandonó la facultad de derecho en 1970 y viajó por América del Sur, México, el norte de África y Europa.\nEn 1972 regresó a casa y comenzó a escribir letras de música pop y rock con Raúl Seixas, un conocido cantante y compositor brasileño. Trabajó para Polygram y CBS Records hasta 1980, cuando emprendió nuevos viajes por Europa y África.', '1947-08-24'),
(14, 'Franz Kafka', 'Franz Kafka es uno de los escritores de ficción más importantes e influyentes de principios del siglo XX; novelista y escritor de cuentos cuyas obras, sólo después de su muerte, llegaron a ser consideradas como uno de los mayores logros de la literatura del siglo XX.', '1883-07-03'),
(15, 'Walter Isaacson', 'Walter Isaacson, director ejecutivo del Instituto Aspen, ha sido presidente de CNN y editor en jefe de la revista Time. Es el autor de Steve Jobs; Einstein: su vida y universo; Benjamin Franklin: una vida americana; y Kissinger: una biografía, y coautor de The Wise Men: Six Friends and the World They Made. Vive en Washington, DC.', '1952-04-20'),
(16, 'Madeline Miller', 'Madeline Miller nació en Boston y creció en la ciudad de Nueva York y Filadelfia. Asistió a la Universidad de Brown, donde obtuvo su licenciatura y maestría en Clásicos. Durante los últimos diez años ha estado enseñando y dando clases particulares de latín, griego y Shakespeare a estudiantes de secundaria. También estudió en el departamento de Dramaturgia de la Escuela de Drama de Yale.\ndonde se centró en la adaptación de textos clásicos a formas modernas. Actualmente vive cerca de Filadelfia, PA. La Canción de Aquiles es su primera novela. Su segunda novela, Circe, se publicará en abril de 2018.', '1978-07-24'),
(17, 'Aldous Huxley', 'Aldous Leonard Huxley (26 de julio de 1894 - 22 de noviembre de 1963) fue un escritor y filósofo inglés. Escribió casi 50 libros, tanto novelas como obras de no ficción, así como una amplia variedad de ensayos, narrativas y poemas.', '1894-06-26'),
(18, 'Leonardo da Vinci', 'Leonardo di ser Piero da Vinci  escuchar (Vinci, 15 de abril de 14522​-Amboise, 2 de mayo de 1519), más conocido como Leonardo da Vinci, fue un polímata florentino del Renacimiento italiano. Fue a la vez pintor, anatomista, arquitecto, paleontólogo,3​ botánico, escritor, escultor, filósofo, ingeniero, inventor, músico, poeta y urbanista.', '1452-03-15'),
(19, 'Michael Pollan', 'Michael Pollan es un autor, periodista, activista y profesor de periodismo estadounidense en la Escuela de Periodismo de UC Berkeley. Escribe sobre los lugares donde se cruzan la naturaleza y la cultura: en nuestros platos, en nuestras granjas y jardines, y en el entorno construido.', '1955-02-06');

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

--
-- Volcado de datos para la tabla `carrito`
--

INSERT INTO `carrito` (`id_carrito`, `id_usuario`, `id_libro`, `cantidad`, `fecha_agregado`) VALUES
(18, 1, 10, 1, '2024-11-26 23:29:19'),
(47, 7, 26, 1, '2024-12-03 01:21:16');

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
(12, 'Auto-ayuda'),
(15, 'Biografías'),
(4, 'Ciencia'),
(16, 'Cocina'),
(11, 'Economía'),
(9, 'Educativo'),
(13, 'Fantasía'),
(2, 'Ficción'),
(10, 'Filosofía'),
(6, 'Historia'),
(8, 'Política'),
(7, 'Psicología'),
(14, 'Romance'),
(5, 'Tecnología'),
(3, 'Thriller');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detallepedido`
--

CREATE TABLE `detallepedido` (
  `id_detallepedido` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_libro` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detallepedido`
--

INSERT INTO `detallepedido` (`id_detallepedido`, `id_pedido`, `id_libro`, `cantidad`, `precio_unitario`) VALUES
(1, 4, 10, 1, 80000.00),
(3, 6, 4, 2, 28000.00),
(4, 7, 3, 1, 45000.00),
(5, 11, 1, 1, 55000.00),
(6, 12, 15, 1, 92000.00),
(7, 13, 22, 1, 17000.00),
(8, 14, 16, 1, 24000.00),
(9, 15, 25, 1, 73000.00),
(10, 16, 24, 1, 85000.00),
(11, 16, 23, 1, 159000.00),
(12, 17, 29, 1, 23000.00),
(13, 17, 17, 1, 17000.00),
(14, 18, 21, 1, 88000.00),
(15, 19, 26, 1, 42700.00);

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
(1, 'Not without laughter', 'Esta es la historia de la mayoría de edad de un niño afroamericano en un pequeño pueblo de Kansas.', 55000.00, 5, 1, 2, 'https://ia800505.us.archive.org/view_archive.php?archive=/10/items/m_covers_0011/m_covers_0011_68.zip&file=0011688085-M.jpg', '1963-01-15', '2796618430'),
(2, 'DIGITAL FORTRESS', 'Digital Fortress es una novela de suspenso escrita por el autor estadounidense Dan Brown y publicada en 1998 por St. Martin\'s Press. El libro explora el tema de la vigilancia gubernamental de la información almacenada electrónicamente sobre la vida privada de los ciudadanos, y las posibles libertades civiles y las implicaciones éticas del uso de dicha tecnología.', 35000.00, 7, 2, 3, 'https://covers.openlibrary.org/b/id/14542864-M.jpg', '2005-06-12', '9780593057445'),
(3, 'The Dark Secret', 'Como todos los dragoncitos del destino, Starflight siempre ha querido ver su hogar, pero también ha tenido miedo de sus compañeros NightWings. Starflight no tiene poderes para leer la mente como su tribu y no entiende por qué son tan reservados. Nadie ha visto nunca a la reina NightWing.', 45000.00, 3, 3, 2, 'https://covers.openlibrary.org/b/id/7436616-M.jpg', '2013-03-13', '545349214'),
(4, 'L\'ultimo dei Mohicani', 'La historia clásica de Hawkeye, Natty Bumppo, el explorador fronterizo que le dio la espalda a la \"civilización\" y su amistad con un guerrero mohicano mientras escoltan a dos hermanas a través del peligroso desierto del país indio en la frontera de Estados Unidos.', 28000.00, 8, 4, 2, 'https://covers.openlibrary.org/b/id/12139938-M.jpg', '1994-09-02', '8879836854'),
(9, 'The 48 laws of power', 'Amoral, astuto, despiadado e instructivo, este bestseller del New York Times, con millones de copias, es el manual definitivo para cualquier persona interesada en obtener, observar o defenderse del control definitivo, del autor de Las leyes de la naturaleza humana.', 65000.00, 15, 5, 10, 'https://covers.openlibrary.org/b/id/9573841-M.jpg', '1998-09-13', '25418275'),
(10, 'La psicología del dinero', 'Lecciones eternas sobre la riqueza, la codicia y la felicidad. Hacer bien el dinero no tiene que ver necesariamente con lo que sabes. Se trata de cómo te comportas. Y el comportamiento es difícil de enseñar, incluso a personas realmente inteligentes. Por lo general, se considera que cómo administrar el dinero, invertirlo y tomar decisiones comerciales implica muchos cálculos matemáticos.\ndonde los datos y las fórmulas nos dicen exactamente qué hacer. Pero en el mundo real, la gente no toma decisiones financieras en una hoja de cálculo. Los preparan en la mesa o en una sala de reuniones, donde se mezclan la historia personal, su visión única del mundo, el ego, el orgullo, el marketing y los incentivos extraños.', 80000.00, 5, 6, 11, 'https://covers.openlibrary.org/b/id/14653525-M.jpg', '2020-09-08', '0857197681'),
(11, 'A Game of Thrones', 'Hace mucho tiempo, en una época olvidada, un acontecimiento sobrenatural desequilibró las estaciones. En una tierra donde los veranos pueden durar décadas y los inviernos toda una vida, se están gestando problemas. El frío está regresando, y en los páramos helados al norte de Invernalia, fuerzas siniestras y sobrenaturales se están concentrando más allá del Muro protector del reino.\nEn el centro del conflicto se encuentran los Stark de Winterfell, una familia tan dura e inflexible como la tierra en la que nacieron. Desde una tierra de frío brutal hasta un lejano reino estival de abundancia epicúrea, aquí hay una historia de señores y damas, soldados y hechiceros, asesinos y bastardos, que se unen en una época de sombríos augurios.', 65000.00, 12, 7, 1, 'https://covers.openlibrary.org/b/id/14826720-M.jpg', '2002-05-28', '553381687'),
(12, 'Tormenta de espadas', 'De los cinco contendientes por el poder, uno está muerto, otro en desgracia, y las guerras continúan mientras se hacen y rompen alianzas. Joffrey se sienta en el Trono de Hierro, el incómodo gobernante de los Siete Reinos. Su rival más acérrimo, Lord Stannis, está derrotado y deshonrado, víctima de la hechicera que lo tiene esclavizado.\nEl joven Robb todavía gobierna el Norte desde la fortaleza de Aguasdulces. Mientras tanto, atravesando un continente empapado de sangre se encuentra la reina exiliada, Daenerys, dueña de los únicos tres dragones que aún quedan en el mundo.', 24000.00, 25, 7, 2, 'https://covers.openlibrary.org/b/id/10668976-M.jpg', '2012-06-15', '9786073108652'),
(13, 'Furtună pe Windhaven', 'George R. R. Martin ha emocionado a una generación de lectores con sus obras épicas de la imaginación, más recientemente la saga más vendida del New York Times, aclamada por la crítica, contada en las novelas Juego de tronos, Choque de reyes y Tormenta de espadas. Lisa Tuttle ha sido aclamada por los fanáticos de la ciencia ficción, el terror y la fantasía por igual.\nmás recientemente por su inquietante novela The Pillow Friend. Ahora, juntos, regalan a los lectores esta historia clásica de un mundo brillantemente representado de tradición férrea, donde un alma rebelde busca demostrar el poder de un sueño. El planeta Windhaven no era originalmente un hogar para los humanos, pero se convirtió en uno después del accidente. de una nave espacial colonial.\nEs un mundo de pequeñas islas, clima severo y mares infestados de monstruos. La comunicación entre los asentamientos dispersos era prácticamente imposible hasta que se descubrió que, gracias a la ligera gravedad y a una atmósfera densa, los humanos podían volar con la ayuda de alas de metal hechas con trozos de la nave espacial canibalizada. Muchas generaciones después,\nEntre las islas dispersas que conforman el mundo acuático de Windhaven, nadie tiene más prestigio que los voladores de alas plateadas, que traen noticias, chismes, canciones e historias.', 98000.00, 5, 7, 13, 'https://covers.openlibrary.org/b/id/11931715-M.jpg', '2013-01-18', '6065796182'),
(14, 'I Don\'t Love You Anymore', 'Estimado lector,\n\nEspero que este libro te parezca un cálido abrazo. Escribí este libro para aquellos que sienten todo demasiado profundamente. Tienes razón, escribí este libro para ti. Este libro estaba destinado a encontrarte si alguna vez amaste a alguien que no te amaba, si alguna vez invertiste demasiado en las personas equivocadas o si te cuesta dejarlo ir.\nYa no te amo es un libro que te hará sentir como en casa. Te prometo que te abrazará suavemente en tus peores días.\n\nCon amor, Rithvik', 41500.00, 14, 8, 14, 'https://covers.openlibrary.org/b/id/14638562-M.jpg', '2024-04-02', '9780143469131'),
(15, 'Padre rico, padre pobre para jóvenes', 'Una guía apropiada para la edad fomenta el desarrollo de habilidades monetarias seguras y responsables, brindando ejemplos de casos, recuadros y recomendaciones de actitudes que demuestran cómo lograr seguridad en el desafiante mercado laboral actual.Si bien muchas cosas en nuestro mundo están cambiando a gran velocidad, las lecciones sobre el dinero y los principios de Padre Rico, Padre Pobre, no han cambiado. Hoy en día, mientras el dinero sigue desempeñando un papel clave en nuestra vida diaria, los mensajes del bestseller internacional de Robert Kiyosaki son más oportunos e importantes que nunca.', 92000.00, 28, 9, 11, 'https://covers.openlibrary.org/b/id/10523471-M.jpg', '2010-01-23', '9708120103'),
(16, 'Wicked', 'Una fábula para adultos sobre el tema del destino y el libre albedrío de un escritor de libros para niños. Cuenta la historia de Elphaba antes de convertirse en la Bruja Malvada del Oeste en la tierra de Oz. La novela narra su carrera como monja, enfermera, activista a favor de la democracia y defensora de los derechos de los animales.', 24000.00, 9, 10, 14, 'https://covers.openlibrary.org/b/id/10822929-M.jpg', '2007-12-03', '8408072374'),
(17, 'Haunting Adeline', 'The Manipulator\n\nI can manipulate the emotions of anyone who lets me.\n\nI will make you hurt, make you cry, make you laugh and sigh.\n\nBut my words don\'t affect him. Especially not when I plead for him to leave.\n\nHe\'s always there, watching and waiting.\n\nAnd I can never look away.\n\nNot when I want him to come closer.\n\nThe Shadow\n\nI didn\'t mean to fall in love.\n\nBut now that I have, I can\'t stay away.\n\nI\'m mesmerized by her smile, by her eyes, and the way she moves.\n\nThe way she undresses...\n\nI\'ll keep watching and waiting. Until I can make her mine.\n\nAnd once she is, I\'ll never let her go.\n\nNot even when she begs me to.', 17000.00, 56, 11, 14, 'https://covers.openlibrary.org/b/id/12992962-M.jpg', '2023-02-23', '8419421898'),
(18, 'Read People Like a Book', 'Lee rápidamente a las personas, descifra el lenguaje corporal, detecta mentiras y comprende la naturaleza humana.\n¿Es posible analizar a las personas sin que digan una palabra? Sí, lo es. Aprenda cómo convertirse en un “lector de mentes” y forjar conexiones profundas.\nCómo meterse en la cabeza de las personas sin que lo sepan.\nRead People Like a Book no es un libro normal sobre el lenguaje corporal y las expresiones faciales. Sí, incluye todas esas cosas, así como nuevas técnicas sobre cómo detectar verdaderamente mentiras en la vida cotidiana, pero este libro trata más sobre la comprensión de la psicología y la naturaleza humanas. Somos quienes somos por nuestras experiencias y pasados,\ny esto guía nuestros hábitos y comportamientos más que cualquier otra cosa. Partes de este libro se leen como el libro de texto de psicología más interesante y aplicable que jamás haya leído. ¡Mira dentro de ti y de los demás!', 28000.00, 6, 12, 7, 'https://covers.openlibrary.org/b/id/11983442-M.jpg', '2020-12-19', '1647432235'),
(19, 'Alchemik', 'Combinando magia, misticismo, sabiduría y asombro en una inspiradora historia de autodescubrimiento, The Alchemist se ha convertido en un clásico moderno, vendiendo millones de copias en todo el mundo y transformando las vidas de innumerables lectores a lo largo de generaciones.\n\nLa obra maestra de Paulo Coelho cuenta la historia mística de Santiago,\nun pastor andaluz que anhela viajar en busca de un tesoro mundano. Su búsqueda lo llevará a riquezas muy diferentes (y mucho más satisfactorias) de lo que jamás imaginó. El viaje de Santiago nos enseña la sabiduría esencial de escuchar nuestro corazón, de reconocer las oportunidades y aprender a leer los presagios esparcidos por el camino de la vida, y,\nlo más importante, seguir nuestros sueños.', 76000.00, 19, 13, 2, 'https://covers.openlibrary.org/b/id/8501951-M.jpg', '1995-12-05', '8391723917'),
(20, 'Eleven minutes', 'Once Minutos es la historia de María, una joven de un pueblo brasileño, cuyos primeros inocentes roces con el amor la dejan desconsolada. A temprana edad, se convence de que nunca encontrará el amor verdadero, creyendo en cambio que \"el amor es algo terrible que te hará sufrir...\". Un encuentro casual en Río la lleva a Ginebra,\ndonde sueña con encontrar fama y fortuna. La desesperada visión que María tiene del amor se pone a prueba cuando conoce a un joven y apuesto pintor. En esta odisea de autodescubrimiento,\nMaría tiene que elegir entre seguir un camino de oscuridad (el placer sexual por sí mismo) o arriesgarlo todo para encontrar su propia \"luz interior\" y la posibilidad del sexo sagrado, el sexo en el contexto del amor.', 56000.00, 23, 13, 14, 'https://covers.openlibrary.org/b/id/11625598-M.jpg', '2003-04-07', '0007712987'),
(21, 'The Winner Stands Alone', 'El querido y exitoso autor internacional de El alquimista regresa con otra novela inquietante: un emocionante viaje a nuestra constante fascinación por los mundos de la fama, la fortuna y la celebridad. Una profunda meditación sobre el poder personal y los sueños inocentes que el éxito manipula o deshace.\nThe Winner Stands Alone está ambientado en los apasionantes mundos de la moda y el cine. A lo largo de veinticuatro horas durante el Festival de Cine de Cannes, es la historia de Igor, un emprendedor ruso exitoso y motivado que hará todo lo posible para recuperar un amor perdido: su ex esposa, Ewa.\nCreyendo que su vida con Ewa estaba divinamente ordenada, Igor le dijo una vez que destruiría mundos enteros para recuperarla. Surge el conflicto entre una fuerza maligna individual y la sociedad y, a medida que se desarrolla la novela, la moralidad se descarrila. Conozca a los actores y farsantes detrás de escena de Cannes: la \"superclase\" de productores, actores y diseñadores\ny supermodelos, así como aspirantes a estrellas, ex estrellas y parásitos hastiados.donde sueña con encontrar fama y fortuna. La desesperada visión que María tiene del amor se pone a prueba cuando conoce a un joven y apuesto pintor. En esta odisea de autodescubrimiento,\nMaría tiene que elegir entre seguir un camino de oscuridad (el placer sexual por sí mismo) o arriesgarlo todo para encontrar su propia \"luz interior\" y la posibilidad del sexo sagrado, el sexo en el contexto del amor.', 88000.00, 9, 13, 2, 'https://covers.openlibrary.org/b/id/6397555-M.jpg', '2009-07-09', '9780061872549'),
(22, 'El Don supremo', 'Esta edición aún no tiene una descripción.', 17000.00, 7, 13, 6, 'https://covers.openlibrary.org/b/id/8962595-M.jpg', '2015-01-02', '8408132822'),
(23, 'La Metamorfosis', 'Metamorfosis (alemán: Die Verwandlung) es una novela escrita por Franz Kafka que se publicó por primera vez en 1915. Una de las obras más conocidas de Kafka, Metamorfosis cuenta la historia del vendedor Gregor Samsa, quien se despierta una mañana y se encuentra inexplicablemente transformado en un enorme insecto (alemán: ungeheueres Ungeziefer, iluminado.\n\"alimañas monstruosas\") y posteriormente lucha por adaptarse a esta nueva condición. La novela corta ha sido ampliamente discutida entre los críticos literarios, ofreciéndose diferentes interpretaciones. En la cultura popular y en las adaptaciones de la novela, el insecto se representa comúnmente como una cucaracha.', 159000.00, 5, 14, 13, 'https://covers.openlibrary.org/b/id/7994058-M.jpg', '1991-10-02', '9681500512'),
(24, 'El Castillo/ The Castle', 'El castillo (título original: \"Das Schloß\") es la historia de K., el agrimensor no deseado que nunca será admitido en el castillo ni aceptado en el pueblo y, sin embargo, no puede regresar a casa. Al encontrarse con dualidades de certeza y duda, esperanza y miedo, razón y sinsentido, las luchas de K. en el absurdo,\nEl mundo laberíntico en el que se encuentra parecen revelar una verdad inexplicable sobre la naturaleza de la existencia. Kafka comenzó El castillo en 1922 y nunca lo terminó; sin embargo, ésta, la última de sus tres grandes novelas, llega a conclusiones fascinantes que la hacen sentir extrañamente completa.', 85000.00, 9, 14, 2, 'https://covers.openlibrary.org/b/id/5266416-M.jpg', '2003-06-30', '8437616093'),
(25, 'El Proceso', 'El famoso inicio del relato reza \"Alguien debió de haber calumniado a Josef K., porque sin haber hecho nada malo, una mañana fue detenido\". Un par de funcionarios detienen al gerente bancario Josef K., limitándose a decirle que se encuentra procesado. Desde ese momento Josef K. es sujeto de un asfixiante procedimiento judicial que poco a poco se apodera de su vida; es interrogado en infectas dependencias de tribunales decadentes, instalados en buhardillas de la periferia; es espectador de extrañas situaciones relacionadas con los burócratas que le rodean y conoce a personajes que parecen querer ayudarle, pero son tan impotentes como él frente a las muchas instancias y niveles del poder judicial.', 73000.00, 15, 14, 10, 'https://covers.openlibrary.org/b/id/12724240-M.jpg', '1925-02-13', '8497592816'),
(26, 'Steve Jobs', 'Del autor de las biografías más vendidas de Benjamin Franklin y Albert Einstein, esta es la biografía exclusiva de Steve Jobs. Basado en más de cuarenta entrevistas con Jobs realizadas durante dos años, así como entrevistas con más de cien familiares, amigos, adversarios, competidores y colegas,\nWalter Isaacson ha escrito una historia fascinante sobre la vida en montaña rusa y la personalidad tremendamente intensa de un emprendedor creativo cuya pasión por la perfección y su impulso feroz revolucionaron seis industrias: computadoras personales, películas animadas, música, teléfonos, tabletas y publicaciones digitales.', 42700.00, 3, 15, 15, 'https://covers.openlibrary.org/b/id/12178173-M.jpg', '2011-02-16', '6047703739'),
(27, 'The Song of Achilles', 'Patroclo, un joven príncipe torpe, sigue a Aquiles a la guerra, sin saber que los años siguientes pondrán a prueba todo lo que han aprendido, todo lo que aprecian. Y que, antes de estar preparado, se verá obligado a entregar a su amigo en manos del Destino. Ambientada durante la Guerra de Troya.', 61000.00, 12, 16, 6, 'https://covers.openlibrary.org/b/id/9249299-M.jpg', '2012-06-28', '0062060619'),
(28, 'Brave New World', 'Publicada originalmente en 1932, esta destacada obra literaria es hoy más crucial y relevante que nunca. Clonación, drogas para sentirse bien, programas antienvejecimiento y control social total a través de la política, la programación y los medios: ¿Aldous Huxley ha predicho con precisión nuestro futuro? Con el genio de un narrador,\nTeje estas controversias éticas en una narrativa convincente que comienza en el año 632 AF (después de Ford, la deidad). Cuando Lenina y Bernard visitan una reserva salvaje, experimentamos cómo la utopía puede destruir a la humanidad. Una poderosa obra de ficción especulativa que ha cautivado y aterrorizado a los lectores durante generaciones.\nUn mundo feliz es a la vez una advertencia a la que hay que prestar atención y un entretenimiento que invita a la reflexión pero que satisface. - Contenedor.', 53000.00, 24, 17, 4, 'https://covers.openlibrary.org/b/id/10993168-M.jpg', '1979-10-21', '37076932'),
(29, 'Leonardo.', 'Bill Gates compró al Codex Leicester un cuaderno con las observaciones y teorías científicas de Leonardo da Vinci en 1994 de la propiedad de Armand Hammer por 30,8 millones de dólares. El año pasado, Gates prestó la obra al Powerhouse Museum de Australia, que preparó este complemento para su exposición. Ya no está en forma de códice (las páginas fueron encuadernadas en el siglo XVII,\npero Gates hizo desmantelar la encuadernación para su reproducción digital), el manuscrito abarca temas que van desde los fósiles hasta la astronomía. Cada anverso de esta edición reproduce una de las páginas de Leonardo, escrita en italiano espejo con bocetos anotados en los márgenes; aparece una discusión (pero no una traducción) en el reverso.\nIncluye una introducción a la vida de Leonardo, pero ningún índice.', 23000.00, 12, 18, 4, 'https://covers.openlibrary.org/b/id/12156182-M.jpg', '1975-07-02', '0810902621'),
(30, 'Cooked', '\"Fuego, agua, aire, tierra: nuestro experto en alimentos de mayor confianza cuenta la historia de su educación culinaria. En Cooked, Michael Pollan explora el territorio previamente inexplorado de su propia cocina. Aquí descubre el poder duradero de los cuatro elementos clásicos. -fuego, agua, aire y tierra--\ntransformar las cosas de la naturaleza en cosas deliciosas para comer y beber. Como aprendiz de una sucesión de maestros culinarios, Pollan aprende a asar con fuego, cocinar con líquido, hornear pan y fermentar de todo, desde queso hasta cerveza. En el transcurso de su viaje, descubre que el cocinero ocupa un lugar especial en el mundo,\nsituándose directamente entre la naturaleza y la cultura. Ambos reinos se transforman al cocinar y, en el proceso, el cocinero también. Cada sección de Cooked sigue el esfuerzo de Pollan por dominar una única receta clásica utilizando uno de los cuatro elementos.^', 60200.00, 26, 19, 16, 'https://covers.openlibrary.org/b/id/8322590-M.jpg', '2013-09-23', '1594204217');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_pedido` datetime DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'En proceso'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_usuario`, `total`, `fecha_pedido`, `estado`) VALUES
(4, 6, 80000.00, '2024-11-27 07:57:42', 'Completado'),
(6, 6, 56000.00, '2024-11-27 07:59:48', 'Completado'),
(7, 6, 45000.00, '2024-11-27 08:17:37', 'Completado'),
(8, 6, 55000.00, '2024-11-27 08:55:57', 'En proceso'),
(9, 6, 55000.00, '2024-11-27 08:55:57', 'En proceso'),
(10, 6, 55000.00, '2024-11-27 08:55:57', 'En proceso'),
(11, 6, 55000.00, '2024-11-27 10:06:41', 'En proceso'),
(12, 6, 92000.00, '2024-12-03 03:36:35', 'En proceso'),
(13, 6, 17000.00, '2024-12-03 03:36:35', 'En proceso'),
(14, 6, 24000.00, '2024-12-03 03:36:35', 'En proceso'),
(15, 6, 73000.00, '2024-12-03 03:36:35', 'En proceso'),
(16, 6, 244000.00, '2024-12-03 03:36:35', 'En proceso'),
(17, 6, 40000.00, '2024-12-03 03:36:35', 'En proceso'),
(18, 6, 88000.00, '2024-12-03 04:38:29', 'En proceso'),
(19, 7, 42700.00, '2024-12-03 06:18:59', 'En proceso');

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
(31, 1, 'Actualización', 'Autor Tui T. Sutherland actualizado', '2024-11-23 00:00:00', '16:22:28'),
(32, 1, 'Inserción', 'Categoría Historia agregada correctamente', '2024-11-24 00:00:00', '02:01:29'),
(33, 1, 'Inserción', 'Categoría Psicología agregada correctamente', '2024-11-24 00:00:00', '02:01:53'),
(34, 1, 'Inserción', 'Categoría Política agregada correctamente', '2024-11-24 00:00:00', '02:02:14'),
(35, 1, 'Inserción', 'Categoría Educativo agregada correctamente', '2024-11-24 00:00:00', '02:02:36'),
(36, 1, 'Inserción', 'Categoría Filosofía agregada correctamente', '2024-11-24 00:00:00', '02:03:15'),
(37, 1, 'Inserción', 'Autor Robert Greene agregado correctamente', '2024-11-24 00:00:00', '02:04:07'),
(38, 1, 'Eliminación', 'Libro [8, \'The 48 laws of power\', \'Amoral, astuto, despiadado e instructivo, este bestseller del New York Times, con millones de ejemplares, es el manual definitivo para cualquier persona interesada en obtener, observar o defenderse contra el control definitivo, del autor de Las leyes de la naturaleza humana.\', \'Robert Greene\', \'Filosofía\', \'65000.00\', 15, \'https://covers.openlibrary.org/b/id/9573841-M.jpg\', \'1998-09-13\', 25418275] eliminado correctamente', '2024-11-24 00:00:00', '02:16:26'),
(39, 1, 'Eliminación', 'Libro [7, \'The 48 laws of power\', \'Amoral, astuto, despiadado e instructivo, este bestseller del New York Times, con millones de ejemplares, es el manual definitivo para cualquier persona interesada en obtener, observar o defenderse contra el control definitivo, del autor de Las leyes de la naturaleza humana.\', \'Robert Greene\', \'Filosofía\', \'65000.00\', 15, \'https://covers.openlibrary.org/b/id/9573841-M.jpg\', \'1998-09-13\', 25418275] eliminado correctamente', '2024-11-24 00:00:00', '02:16:30'),
(40, 1, 'Eliminación', 'Libro [6, \'The 48 laws of power\', \'Amoral, astuto, despiadado e instructivo, este bestseller del New York Times, con millones de ejemplares, es el manual definitivo para cualquier persona interesada en obtener, observar o defenderse contra el control definitivo, del autor de Las leyes de la naturaleza humana.\', \'Robert Greene\', \'Filosofía\', \'65000.00\', 15, \'https://covers.openlibrary.org/b/id/9573841-M.jpg\', \'1998-09-13\', 25418275] eliminado correctamente', '2024-11-24 00:00:00', '02:16:32'),
(41, 1, 'Eliminación', 'Libro [5, \'The 48 laws of power\', \'Amoral, astuto, despiadado e instructivo, este bestseller del New York Times, con millones de ejemplares, es el manual definitivo para cualquier persona interesada en obtener, observar o defenderse contra el control definitivo, del autor de Las leyes de la naturaleza humana.\', \'Robert Greene\', \'Filosofía\', \'65000.00\', 15, \'https://covers.openlibrary.org/b/id/9573841-M.jpg\', \'1998-09-13\', 25418275] eliminado correctamente', '2024-11-24 00:00:00', '02:16:39'),
(42, 1, 'Inserción', 'Categoría Economía agregada correctamente', '2024-11-24 00:00:00', '02:20:00'),
(43, 1, 'Inserción', 'Autor Morgan Housel agregado correctamente', '2024-11-24 00:00:00', '02:20:46'),
(44, 1, 'Actualización', 'Estado del pedido 4 actualizado', '2024-11-27 00:00:00', '03:47:51'),
(45, 1, 'Actualización', 'Estado del pedido 6 actualizado', '2024-11-27 00:00:00', '03:47:55'),
(46, 1, 'Actualización', 'Estado del pedido 6 actualizado', '2024-11-27 00:00:00', '03:48:01'),
(47, 1, 'Actualización', 'Estado del pedido 7 actualizado', '2024-11-27 00:00:00', '03:48:04'),
(48, 1, 'Inserción', 'Categoría Auto-ayuda agregada correctamente', '2024-12-02 00:00:00', '21:52:50'),
(49, 1, 'Inserción', 'Autor George R. R. Martin agregado correctamente', '2024-12-02 00:00:00', '21:54:19'),
(50, 1, 'Actualización', 'Autor George R. R. Martin actualizado', '2024-12-02 00:00:00', '21:54:35'),
(51, 1, 'Actualización', 'Libro A Game of Thrones actualizado correctamente', '2024-12-02 00:00:00', '21:56:48'),
(52, 1, 'Inserción', 'Categoría Fantasía agregada correctamente', '2024-12-02 00:00:00', '22:00:33'),
(53, 1, 'Inserción', 'Autor Rithvik Singh agregado correctamente', '2024-12-02 00:00:00', '22:04:34'),
(54, 1, 'Inserción', 'Categoría Romance agregada correctamente', '2024-12-02 00:00:00', '22:25:23'),
(55, 1, 'Actualización', 'Libro I Don\'t Love You Anymore actualizado correctamente', '2024-12-02 00:00:00', '22:25:36'),
(56, 1, 'Inserción', 'Autor Robert T. Kiyosaki agregado correctamente', '2024-12-02 00:00:00', '22:28:08'),
(57, 1, 'Inserción', 'Libro Padre rico, padre pobre para jóvenes agregado correctamente', '2024-12-02 00:00:00', '22:30:19'),
(58, 1, 'Actualización', 'Libro Not without laughter actualizado correctamente', '2024-12-02 00:00:00', '22:30:37'),
(59, 1, 'Inserción', 'Autor Gregory Maguire agregado correctamente', '2024-12-02 00:00:00', '22:32:11'),
(60, 1, 'Inserción', 'Libro Wicked agregado correctamente', '2024-12-02 00:00:00', '22:33:00'),
(61, 1, 'Inserción', 'Autor H. D. Cartlon agregado correctamente', '2024-12-02 00:00:00', '22:34:25'),
(62, 1, 'Inserción', 'Libro Haunting Adeline agregado correctamente', '2024-12-02 00:00:00', '22:35:29'),
(63, 1, 'Inserción', 'Autor Sun Tzu agregado correctamente', '2024-12-02 00:00:00', '22:44:12'),
(64, 1, 'Actualización', 'Autor Sun Tzu actualizado', '2024-12-02 00:00:00', '22:44:26'),
(65, 1, 'Actualización', 'Autor Sun Tzu actualizado', '2024-12-02 00:00:00', '22:44:56'),
(66, 1, 'Actualización', 'Autor Patrick King actualizado', '2024-12-02 00:00:00', '22:46:03'),
(67, 1, 'Inserción', 'Libro Read People Like a Book agregado correctamente', '2024-12-02 00:00:00', '22:47:15'),
(68, 1, 'Inserción', 'Autor Paulo Coelho agregado correctamente', '2024-12-02 00:00:00', '22:48:06'),
(69, 1, 'Inserción', 'Libro Alchemik agregado correctamente', '2024-12-02 00:00:00', '22:49:07'),
(70, 1, 'Inserción', 'Libro Eleven minutes agregado correctamente', '2024-12-02 00:00:00', '22:52:29'),
(71, 1, 'Inserción', 'Libro The Winner Stands Alone agregado correctamente', '2024-12-02 00:00:00', '22:54:01'),
(72, 1, 'Inserción', 'Libro El Don supremo agregado correctamente', '2024-12-02 00:00:00', '22:55:33'),
(73, 1, 'Inserción', 'Autor Franz Kafka agregado correctamente', '2024-12-02 00:00:00', '22:57:01'),
(74, 1, 'Inserción', 'Libro La Metamorfosis agregado correctamente', '2024-12-02 00:00:00', '22:58:12'),
(75, 1, 'Inserción', 'Libro El Castillo/ The Castle agregado correctamente', '2024-12-02 00:00:00', '22:59:28'),
(76, 1, 'Inserción', 'Libro El Proceso agregado correctamente', '2024-12-02 00:00:00', '23:01:38'),
(77, 1, 'Inserción', 'Categoría Biografías agregada correctamente', '2024-12-02 00:00:00', '23:06:19'),
(78, 1, 'Inserción', 'Autor Walter Isaacson agregado correctamente', '2024-12-02 00:00:00', '23:08:12'),
(79, 1, 'Inserción', 'Autor Madeline Miller agregado correctamente', '2024-12-02 00:00:00', '23:08:39'),
(80, 1, 'Inserción', 'Libro Steve Jobs agregado correctamente', '2024-12-02 00:00:00', '23:10:14'),
(81, 1, 'Inserción', 'Libro The Song of Achilles agregado correctamente', '2024-12-02 00:00:00', '23:12:49'),
(82, 1, 'Inserción', 'Autor Aldous Huxley agregado correctamente', '2024-12-02 00:00:00', '23:14:32'),
(83, 1, 'Inserción', 'Libro Brave New World agregado correctamente', '2024-12-02 00:00:00', '23:15:53'),
(84, 1, 'Inserción', 'Autor Leonardo da Vinci agregado correctamente', '2024-12-02 00:00:00', '23:17:46'),
(85, 1, 'Inserción', 'Libro Leonardo. agregado correctamente', '2024-12-02 00:00:00', '23:18:55'),
(86, 1, 'Inserción', 'Autor Michael Pollan agregado correctamente', '2024-12-02 00:00:00', '23:19:36'),
(87, 1, 'Inserción', 'Libro Cooked agregado correctamente', '2024-12-02 00:00:00', '23:20:40'),
(88, 1, 'Inserción', 'Categoría Cocina agregada correctamente', '2024-12-02 00:00:00', '23:20:47'),
(89, 1, 'Actualización', 'Libro Cooked actualizado correctamente', '2024-12-02 00:00:00', '23:21:11');

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

--
-- Volcado de datos para la tabla `tarjetas`
--

INSERT INTO `tarjetas` (`id_tarjeta`, `id_usuario`, `numero_tarjeta`, `fecha_expiracion`, `tipo`, `nombre_titular`) VALUES
(1, 1, '1111111111122222', '2026-08-01', 'Crédito', 'Admin'),
(2, 1, '52341341', '2033-05-01', 'Débito', 'Admin'),
(3, 6, '1111111111111111', '2030-11-01', 'Crédito', 'Juan'),
(4, 7, '1234126834562945', '2030-09-01', 'Crédito', 'Kevin C');

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
(1, 'admin', 'Admin', 'exp@exp.com', '123456', 'Cl6 #6-667', '555222666', '2024-11-21 00:27:14'),
(4, 'admin', 'Luis', 'ejemplo@exp.com', '123455', '22 #2-32', '551112223', '2024-11-23 15:43:28'),
(5, 'cliente', 'aaaaa', 'aa@aa.com', '123456', '2222', '2222', '2024-11-26 03:21:19'),
(6, 'cliente', 'Juan', 'juan@correo.com', '123456', '22#22', '3151456142', '2024-11-26 02:48:20'),
(7, 'cliente', 'Kevin', 'kevin@hotmail.com', '123456', '55 #6-20', '3619469103', '2024-12-03 00:39:59');

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
-- Volcado de datos para la tabla `valoraciones`
--

INSERT INTO `valoraciones` (`id_valoracion`, `id_libro`, `id_usuario`, `valoracion`, `fecha_valoracion`) VALUES
(2, 4, 6, 4, '2024-11-27 08:55:57'),
(3, 10, 6, 5, '2024-11-27 08:55:57'),
(4, 3, 6, 5, '2024-11-27 08:55:57'),
(5, 15, 6, 5, '2024-12-03 03:36:35'),
(6, 22, 6, 4, '2024-12-03 03:36:35'),
(7, 16, 6, 2, '2024-12-03 03:36:35'),
(8, 25, 6, 5, '2024-12-03 03:36:35'),
(9, 23, 6, 5, '2024-12-03 03:36:35'),
(10, 24, 6, 4, '2024-12-03 03:36:35'),
(11, 17, 6, 3, '2024-12-03 03:36:35'),
(12, 21, 6, 5, '2024-12-03 04:38:29');

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
-- Indices de la tabla `detallepedido`
--
ALTER TABLE `detallepedido`
  ADD PRIMARY KEY (`id_detallepedido`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_libro` (`id_libro`);

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
  MODIFY `id_autor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `detallepedido`
--
ALTER TABLE `detallepedido`
  MODIFY `id_detallepedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarjetas`
--
ALTER TABLE `tarjetas`
  MODIFY `id_tarjeta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  MODIFY `id_valoracion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

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
-- Filtros para la tabla `detallepedido`
--
ALTER TABLE `detallepedido`
  ADD CONSTRAINT `detallepedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE CASCADE,
  ADD CONSTRAINT `detallepedido_ibfk_2` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`) ON DELETE CASCADE;

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
