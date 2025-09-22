-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 22 sep. 2025 à 12:52
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `achat_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `message_contact`
--

DROP TABLE IF EXISTS `message_contact`;
CREATE TABLE IF NOT EXISTS `message_contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contenu` text NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `message_contact`
--

INSERT INTO `message_contact` (`id`, `nom`, `prenom`, `email`, `contenu`, `date`) VALUES
(1, 'Gladisse', 'Gloire', 'gladisse@gmail.com', 'Salut', '2025-08-19 15:14:30'),
(2, 'Virgine', 'koubaka', 'virginie@gmail.com', 'Bonjour ! je souhaitais m\'informer au sujet de l\'avancement de mon projet, elle se trouve à quel niveau présentement ?', '2025-08-19 21:13:29'),
(3, 'Founa', 'Mercier', 'Founa@gmail.com', 'J\'ai compris', '2025-08-24 12:45:03'),
(4, 'Founa', 'Mercier', 'Founa@gmail.com', 'Rien', '2025-08-25 18:23:57'),
(5, 'Founa', 'Peyroche', 'fplacide66@gmail.com', 'Sisi', '2025-08-25 18:57:28'),
(6, 'Founa', 'Mercier', 'Founamercier1@gmail.com', 'DFGHN?', '2025-08-25 20:34:23'),
(7, 'Gaga', 'Lione', 'gaga@gmail.com', 'Bonjour !', '2025-08-28 18:40:43');

-- --------------------------------------------------------

--
-- Structure de la table `order`
--

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `items` varchar(500) NOT NULL,
  `total_price` float NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `order`
--

INSERT INTO `order` (`id`, `name`, `address`, `items`, `total_price`, `date`) VALUES
(18, 'Mercier Founa', '4 rue donatello, 92400', 'Savon en boîte (15€)', 15, '2025-08-11 21:16:06'),
(17, 'Tada Beya', '5 valle 92400', 'Savon en boîte (15€)', 15, '2025-08-11 00:38:58'),
(16, 'Tada Beya', '5 valle 92400', 'Savon noir en boite (15€)', 15, '2025-08-10 21:50:05'),
(13, 'Peyroche Founa', '4 Rue Donatello, Courbevoie, France', 'Savon noir en bouteille (18€)', 18, '2025-08-10 19:06:42'),
(14, 'placide Mata', '5 valle 92400', '', 0, '2025-08-10 19:39:04'),
(15, 'placide Mata', '5 valle 92400', 'Savon noir en boite (15€)', 15, '2025-08-10 19:39:26'),
(19, 'Mercier Founa', '4 rue donatello, 92400', 'Savon en boîte (15€)', 15, '2025-08-15 19:37:15'),
(20, 'Mercier Founa', '4 rue donatello, 92400', 'Savon en bouteille (18€)', 18, '2025-08-15 19:39:37'),
(21, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€)', 15, '2025-08-17 13:27:09'),
(22, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€)', 15, '2025-08-17 21:19:05'),
(23, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€), Savon en boîte (15€), Savon en boîte (15€), Savon en boîte (15€), Savon en boîte (15€)', 75, '2025-08-23 00:18:04'),
(24, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€)', 15, '2025-08-23 00:54:01'),
(25, 'bjama Kade', '6 rue Baba', 'Savon en boîte (15€), Savon en bouteille (18€)', 33, '2025-08-24 15:05:41'),
(26, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€), Savon en boîte (15€), Savon en boîte (15€)', 45, '2025-08-25 20:33:43'),
(27, 'Peyroche Founa', '4 rue Donatello, Thiais, France', '', 0, '2025-08-25 20:33:46'),
(28, 'Peyroche Founa', '4 rue Donatello, Thiais, France', '', 0, '2025-08-25 20:33:49'),
(29, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 22:10:44'),
(30, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 22:10:44'),
(31, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 22:55:57'),
(32, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 22:55:58'),
(33, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 23:03:42'),
(34, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-25 23:03:42'),
(35, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-26 21:43:28'),
(36, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-26 22:06:43'),
(37, 'Jean Dupont', '123 rue de Paris', 'Savon noir (15€)', 15, '2025-08-26 23:18:56'),
(38, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€)', 15, '2025-08-28 18:36:45'),
(39, 'Peyroche Founa', '4 rue Donatello, Thiais, France', 'Savon en boîte (15€)', 15, '2025-08-29 11:18:19'),
(40, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€)', 15, '2025-09-03 11:22:31'),
(41, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€)', 15, '2025-09-05 15:58:37'),
(42, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€)', 15, '2025-09-05 15:58:40'),
(43, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€)', 15, '2025-09-08 20:23:43'),
(44, 'Mercier Founa', '4 rue DONATELLO', 'Savon en boîte (15€)', 15, '2025-09-10 07:49:09');

-- --------------------------------------------------------

--
-- Structure de la table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
CREATE TABLE IF NOT EXISTS `order_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantite` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `description` text,
  `prix` decimal(10,2) NOT NULL,
  `stock` int DEFAULT '0',
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `product`
--

INSERT INTO `product` (`id`, `nom`, `description`, `prix`, `stock`, `image`) VALUES
(1, 'Savon en boîte', NULL, 15.00, 10, 'savon_en_boite.png'),
(2, 'Savon en bouteille', NULL, 18.00, 8, 'savon_en_bouteille.png');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `motdepasse` varchar(255) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `nom`, `email`, `motdepasse`, `adresse`) VALUES
(1, 'Mercier Founa', 'ana@gmail.com', 'scrypt:32768:8:1$pZ4XaaGhCA1CNf69$37db7188265223598e56abfdbe45b644da950a4f641f69c5d1e39e225e182f2d0a440ab629202674e54b93a448955e277c3b7fa447b391a0f7fba3435a35b745', '4 rue DONATELLO'),
(2, 'Kaka', 'kak@gmail.com', 'scrypt:32768:8:1$GqUA7uc4Eh8kHrRK$2005a43c1e6d843f07ba1934b81e00c4af93ed3515ba9419ea96069dec76ff26347c1f92bd0e2884714725cfef61dcaca80ca28b5237383a8e36dc5dfeff1e65', '4 rue Pamelo'),
(3, 'Lili', 'Lili@gmail.com', 'scrypt:32768:8:1$3wpHPvjHUmLaMaRR$f088672153b0087478a9b79681f9eef5b3809d727b24a2ab452fa98f6292fd753f33d17a6385aaaa8da94ebe9aeb0a544d7033e599078d437e47fc5804c6d297', '15 rue Vila'),
(4, 'Anais', 'Anais@gmail.com', 'scrypt:32768:8:1$NWh1mGWVEWrLQ2lq$fa8509a9cd2c712399d1a3ab0c7cc630ee4bd94f83411a85ee1d569c7a35dcac91d76430641a0087cc5cc0149896a330d26df40709088b11f448f1b541d151f5', '4 rue Pamelo'),
(5, 'Galia', 'galia@contact.fr', 'scrypt:32768:8:1$dt0iScJDmGLVrlJy$ef661b99b355b90342e1bb85faab5ec4eacef80b4452e2e4b442e906df95456aa81e44cb431b7efcc08abf67da5075bd478424b3d987e30a8aed7b5f2946e851', '4 rue Donatello, Thiais, France'),
(6, 'ginette', 'ginette@gmail.com', 'scrypt:32768:8:1$vistC5CWier5VroK$20e5353981d26d763c1ad2d48e5524928cc1ee77f770605f37ce3ed0e09dc9a3304e9f4d4851fbcb37ad3d401f7c5a2a07a0aaecb72fffd5d3abd12aff6ff268', '5 rue Xaco'),
(7, 'ferdinand', 'ferdinand@gmail.com', 'scrypt:32768:8:1$2Vr04mRX8a4pLn1e$634295ac2f85796864aa95b031fca2d1d54a40bc7010a41d71aac4ccb2af393a0a94c939de82c9c042db8ec42feae692f49fcf86d621fe65f733e641bb0bb562', '45 rue Lili'),
(8, 'Bibiche', 'bibiche@gmail.com', 'scrypt:32768:8:1$MShyrpKd0VcfKE2j$826b3817f7d7ac7a8a5aa861be833a7e4cf6224222be6ce721604dfbd2d928603edb31bdfe634361395498b13060b534d320634a9440f0ef0f3661c642b1df00', '57 rue Bala'),
(9, 'Gladisse', 'gladisse@gmail.com', 'scrypt:32768:8:1$5E7LG9OWpTcarPye$5d7d4d617d232ea7c4d98688fdf74708b59773ab06193d47d7b6bdda867697721545546518e429b211467917eff8269a7f132285314e4a555885553dcc2d8237', '67 rue Kalipa'),
(10, 'josephine', 'jose@gmail.com', 'scrypt:32768:8:1$JB1FgIBGpWadUluH$26cb93e29175fc7d40ca6b7974cda326678516f00b005791edcbee99fbeaa9493edd5d5c34bb1427309841fabf635198d8b5f5c8bb023c5fd814d828865fb9b6', '8 rue mali'),
(11, 'Lala', 'lala@gmail.com', 'scrypt:32768:8:1$XoTA5FEnfg16uHuc$b6fb4cb8466aba4c496abd4c8b80240fb783a4c02d97f7f2af83ee66b5f958eb66a1fa8a5a7ed7eb33c50e28e6daa6dcec1084b78be9608b5255073b2d3999f1', '56 rue Bola'),
(12, 'Tata', 'Tata@gmail.com', 'scrypt:32768:8:1$Ubrw59Q14QGdbvND$5e976a491d2db4f11655215c99c5ee15be72ada09fee2b3da5b35f402f7a15adcc2431478c0f465ede2f5ad697ab582381f14825cb73b0aabb066f2ca115780a', '56 rue Bola'),
(13, 'Dafa', 'dafa@gmail.com', 'scrypt:32768:8:1$Q4YaMD0czryw7oYc$3c5b5202f35618bc4b000089725a886a5c6a322da735092c0c68a7b6d3f7f59163092bf505131ac3b1b2aa7aae83b4edb69739d16a0457f6d89ea5c3c29284fe', '34 rue difi'),
(14, 'Data', 'data@gmail.com', 'scrypt:32768:8:1$VCtMvwwtqpM4p5jK$a20bf6fc7ea8f5a4fe43cfc53eaa54a53e81f4560a38774eb47fe7eecfe3c493133a7f4f0085cc4f1676130a3aff388827b333fa7978a3c9dc86c0db3210d30f', '4 rue data');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
