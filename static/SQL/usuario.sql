-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-09-2024 a las 23:50:14
-- Versión del servidor: 5.7.44-log
-- Versión de PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cineo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `correo` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `clave` varchar(200) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fechareg` datetime NOT NULL,
  `perfil` char(1) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'U'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `clave`, `fechareg`, `perfil`) VALUES
(1, 'emiliano', 'gatitaloli69@gmail.com', 'scrypt:32768:8:1$xBoXuUO69ykuK8bu$5761fdc3f86e28ca123562f648328a0ecb89d08218b4515b42c2fd2ab096acec75e4a07a84e73eb70700cdbe1f1477bcbec7355892301e6a2f95fcc821b053ee', '2024-09-17 17:24:23', 'U');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
