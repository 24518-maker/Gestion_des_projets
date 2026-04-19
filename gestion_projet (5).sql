-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Dim 19 Avril 2026 à 21:49
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `gestion_projet`
--

-- --------------------------------------------------------

--
-- Structure de la table `encadrant`
--

CREATE TABLE IF NOT EXISTS `encadrant` (
  `Id_Encadrant` int(11) NOT NULL AUTO_INCREMENT,
  `Nom` varchar(50) NOT NULL,
  `Prenom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `PASSWORD` varchar(50) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id_Encadrant`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Contenu de la table `encadrant`
--

INSERT INTO `encadrant` (`Id_Encadrant`, `Nom`, `Prenom`, `email`, `PASSWORD`, `photo`) VALUES
(1, 'Ahmed', 'Sejad', 'ahmedsejad@example.com', '123rere7', 'sjad.jpeg'),
(2, 'Fatimetou', 'zeyn', 'fatimetouzeyn@example.com', '123rere7', 'ftt.jpg'),
(3, 'debagh', '', 'debagh@example.com', '123rere7', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `etape`
--

CREATE TABLE IF NOT EXISTS `etape` (
  `Id_etape` int(11) NOT NULL AUTO_INCREMENT,
  `Nom_etape` varchar(50) NOT NULL,
  `Id_projet` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id_etape`),
  KEY `fk_etape_projet` (`Id_projet`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=30 ;

--
-- Contenu de la table `etape`
--

INSERT INTO `etape` (`Id_etape`, `Nom_etape`, `Id_projet`) VALUES
(18, 'Creation des offres de stage', 21),
(19, 'Affectation des étudiants', 21),
(20, 'suivi et evaluation du stage', 21),
(21, 'creation des disscussions et sujet', 22),
(22, 'interaction et moderation', 22),
(23, 'planification des formations ', 23),
(24, 'inscription des participants', 23),
(25, 'planfication du projet', 24),
(26, 'suivi et developpement', 24),
(27, 'evaluation ', 24),
(28, 'conception et modelisation', 25),
(29, 'Développement et test', 25);

-- --------------------------------------------------------

--
-- Structure de la table `etudiant`
--

CREATE TABLE IF NOT EXISTS `etudiant` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Matricule` int(11) NOT NULL DEFAULT '0',
  `Nom` varchar(50) NOT NULL,
  `Prenom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `Id_group` int(11) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Id_group` (`Id_group`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;

--
-- Contenu de la table `etudiant`
--

INSERT INTO `etudiant` (`Id`, `Matricule`, `Nom`, `Prenom`, `email`, `Id_group`, `password`) VALUES
(1, 24570, 'Ali', 'Ahmed', 'ali@exemple.com', 1, '123rrr6'),
(2, 24506, 'Aichetou', 'Ndaw', 'aichetoundaw@exemple.com', 1, '123rrr6'),
(3, 24518, 'Aminata', 'Athié', 'aminataathie@exemple.com', 1, '123rrr6'),
(4, 24576, 'Fatimetou', 'deyin', 'fatimetoudeyin@exemple.com', 2, '123rrr6'),
(5, 24579, 'Emel', 'Med', 'emelmed@exemple.com', 2, '123rrr6'),
(6, 24572, 'Houda', 'moulay', 'houdamoulay@exemple.com', 2, '123rrr6'),
(7, 24575, 'Vayze', 'Mohamed', 'vayzemed@exemple.com', 3, '123rrr6'),
(8, 24571, 'Khadija', 'Ali', 'khadija@exemple.com', 3, '123rrr6'),
(9, 24573, 'Bilal', 'Salem', 'bilal@exemple.com', 4, '123rrr6'),
(10, 24574, 'Sara', 'Ahmed', 'sara@exemple.com', 4, '123rrr6'),
(11, 24529, 'sidahmed', 'mohamed', 'sidahmed@example.com', 3, '123r6'),
(13, 24530, 'tkber', 'sidi', 'tkb@example.com', 4, '123rrr6'),
(14, 24566, 'mohamed', 'zeyni', 'zeyni@example.cpm', 5, '123r6'),
(15, 24564, 'vadel', 'ndaw', 'vadel@example.com', 5, '123r6'),
(16, 24565, 'enne', 'hafoudh', 'enne@example.com', 5, '123r6');

-- --------------------------------------------------------

--
-- Structure de la table `evaluation`
--

CREATE TABLE IF NOT EXISTS `evaluation` (
  `Id_Evaluation` int(11) NOT NULL AUTO_INCREMENT,
  `Note` decimal(4,2) NOT NULL,
  `Remarque` varchar(255) DEFAULT NULL,
  `Id_etape` int(11) NOT NULL,
  `Id_Encadrant` int(11) NOT NULL,
  `Id_group` int(11) NOT NULL,
  `date_evaluation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_Evaluation`),
  KEY `Id_etape` (`Id_etape`),
  KEY `Id_Encadrant` (`Id_Encadrant`),
  KEY `Id_group` (`Id_group`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=21 ;

--
-- Contenu de la table `evaluation`
--

INSERT INTO `evaluation` (`Id_Evaluation`, `Note`, `Remarque`, `Id_etape`, `Id_Encadrant`, `Id_group`, `date_evaluation`) VALUES
(16, '15.00', 'bon', 20, 1, 1, '2026-04-19 16:10:19'),
(17, '17.00', 'tres bien effort', 19, 1, 1, '2026-04-19 16:11:09'),
(18, '16.00', 'bien organiser', 18, 1, 1, '2026-04-19 16:13:44'),
(19, '12.00', 'vous pouvez faite mieux', 23, 1, 1, '2026-04-19 17:19:36'),
(20, '15.00', 'planification acceptable', 25, 2, 3, '2026-04-19 18:25:49');

-- --------------------------------------------------------

--
-- Structure de la table `groupe`
--

CREATE TABLE IF NOT EXISTS `groupe` (
  `Id_group` int(11) NOT NULL AUTO_INCREMENT,
  `nom_group` varchar(50) NOT NULL,
  `Id_Encadrant` int(11) NOT NULL,
  PRIMARY KEY (`Id_group`),
  KEY `FK_encadrant` (`Id_Encadrant`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Contenu de la table `groupe`
--

INSERT INTO `groupe` (`Id_group`, `nom_group`, `Id_Encadrant`) VALUES
(1, 'Groupe A1', 1),
(2, 'Groupe A2', 1),
(3, 'Groupe B1', 2),
(4, 'Groupe B2', 2),
(5, 'GROUPE C', 3);

-- --------------------------------------------------------

--
-- Structure de la table `livrable`
--

CREATE TABLE IF NOT EXISTS `livrable` (
  `Id_fichier` int(11) NOT NULL AUTO_INCREMENT,
  `nom_fichier` varchar(255) DEFAULT NULL,
  `Id_group` int(11) DEFAULT NULL,
  `Id_etape` int(11) DEFAULT NULL,
  `date_upload` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_fichier`),
  KEY `Id_group` (`Id_group`),
  KEY `Id_etape` (`Id_etape`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Contenu de la table `livrable`
--

INSERT INTO `livrable` (`Id_fichier`, `nom_fichier`, `Id_group`, `Id_etape`, `date_upload`) VALUES
(3, 'file_s1.xml', 1, 18, '2026-04-19 16:01:16'),
(4, 'file_s2.xml', 1, 19, '2026-04-19 16:02:58'),
(5, 'file_s3.xml', 1, 20, '2026-04-19 16:03:53'),
(6, 'file_g1.xml', 1, 23, '2026-04-19 16:07:45'),
(7, 'Doc2.docx', 3, 25, '2026-04-19 19:23:58');

-- --------------------------------------------------------

--
-- Structure de la table `projet`
--

CREATE TABLE IF NOT EXISTS `projet` (
  `Id_projet` int(11) NOT NULL AUTO_INCREMENT,
  `Nom_projet` varchar(50) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `Id_group` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id_projet`),
  KEY `fk_projet_groupe` (`Id_group`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=26 ;

--
-- Contenu de la table `projet`
--

INSERT INTO `projet` (`Id_projet`, `Nom_projet`, `date_debut`, `date_fin`, `Id_group`) VALUES
(21, 'Gestion de stage', '2026-04-01', '2026-05-10', 1),
(22, 'Forum Electronique cas GP', '2026-05-10', '2026-05-31', 1),
(23, 'Gestion des formations et certifications', '2026-04-01', '2026-05-15', 1),
(24, 'Gestion de projet', '2026-04-01', '2026-05-01', 3),
(25, 'systeme de gestion du transport public', '2026-04-01', '2026-04-18', 4);

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `etape`
--
ALTER TABLE `etape`
  ADD CONSTRAINT `fk_etape_projet` FOREIGN KEY (`Id_projet`) REFERENCES `projet` (`Id_projet`) ON DELETE CASCADE;

--
-- Contraintes pour la table `etudiant`
--
ALTER TABLE `etudiant`
  ADD CONSTRAINT `etudiant_ibfk_1` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`);

--
-- Contraintes pour la table `evaluation`
--
ALTER TABLE `evaluation`
  ADD CONSTRAINT `evaluation_ibfk_1` FOREIGN KEY (`Id_etape`) REFERENCES `etape` (`Id_etape`) ON DELETE CASCADE,
  ADD CONSTRAINT `evaluation_ibfk_2` FOREIGN KEY (`Id_Encadrant`) REFERENCES `encadrant` (`Id_Encadrant`),
  ADD CONSTRAINT `evaluation_ibfk_3` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`);

--
-- Contraintes pour la table `groupe`
--
ALTER TABLE `groupe`
  ADD CONSTRAINT `FK_encadrant` FOREIGN KEY (`Id_Encadrant`) REFERENCES `encadrant` (`Id_Encadrant`);

--
-- Contraintes pour la table `livrable`
--
ALTER TABLE `livrable`
  ADD CONSTRAINT `livrable_ibfk_2` FOREIGN KEY (`Id_etape`) REFERENCES `etape` (`Id_etape`) ON DELETE CASCADE,
  ADD CONSTRAINT `livrable_ibfk_1` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`);

--
-- Contraintes pour la table `projet`
--
ALTER TABLE `projet`
  ADD CONSTRAINT `fk_projet_groupe` FOREIGN KEY (`id_group`) REFERENCES `groupe` (`Id_group`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
