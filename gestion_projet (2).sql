-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Jeu 02 Avril 2026 à 01:42
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `encadrant`
--

INSERT INTO `encadrant` (`Id_Encadrant`, `Nom`, `Prenom`, `email`, `PASSWORD`, `photo`) VALUES
(1, 'Ahmed', 'Sejad', 'ahmedsejad@example.com', '123rere7', 'sjad.jpeg'),
(2, 'Fatimetou', 'zeyn', 'fatimetouzeyn@example.com', '123rere7', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `etape`
--

CREATE TABLE IF NOT EXISTS `etape` (
  `Id_etape` int(11) NOT NULL AUTO_INCREMENT,
  `Nom_etape` varchar(50) NOT NULL,
  PRIMARY KEY (`Id_etape`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Contenu de la table `etape`
--

INSERT INTO `etape` (`Id_etape`, `Nom_etape`) VALUES
(1, 'Compte rendu 1'),
(2, 'Compte rendu 2'),
(3, 'Presentation');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Contenu de la table `etudiant`
--

INSERT INTO `etudiant` (`Id`, `Matricule`, `Nom`, `Prenom`, `email`, `Id_group`, `password`) VALUES
(1, 24570, 'Ali', 'Ahmed', 'ali@exemple.com', NULL, '123rrr6'),
(2, 24506, 'Aichetou', 'Ndaw', 'aichetoundaw@exemple.com', NULL, '123rrr6'),
(3, 24518, 'Aminata', 'Athié', 'aminataathie@exemple.com', NULL, '123rrr6'),
(4, 24576, 'Fatimetou', 'deyin', 'fatimetoudeyin@exemple.com', NULL, '123rrr6'),
(5, 24579, 'Emel', 'Med', 'emelmed@exemple.com', NULL, '123rrr6'),
(6, 24572, 'Houda', 'moulay', 'houdamoulay@exemple.com', NULL, '123rrr6'),
(7, 24575, 'Vayze', 'Mohamed', 'vayzemed@exemple.com', NULL, '123rrr6'),
(8, 24571, 'Khadija', 'Ali', 'khadija@exemple.com', NULL, '123rrr6'),
(9, 24573, 'Bilal', 'Salem', 'bilal@exemple.com', NULL, '123rrr6'),
(10, 24574, 'Sara', 'Ahmed', 'sara@exemple.com', NULL, '123rrr6');

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
  PRIMARY KEY (`Id_Evaluation`),
  KEY `Id_etape` (`Id_etape`),
  KEY `Id_Encadrant` (`Id_Encadrant`),
  KEY `Id_group` (`Id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `groupe`
--

CREATE TABLE IF NOT EXISTS `groupe` (
  `Id_group` int(11) NOT NULL AUTO_INCREMENT,
  `nom_group` varchar(50) NOT NULL,
  `Id_projet` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id_group`),
  KEY `Id_projet` (`Id_projet`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `livrable`
--

CREATE TABLE IF NOT EXISTS `livrable` (
  `Id_fichier` int(11) NOT NULL AUTO_INCREMENT,
  `nom_fichier` varchar(255) DEFAULT NULL,
  `Id_group` int(11) DEFAULT NULL,
  `Id_etape` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id_fichier`),
  KEY `Id_group` (`Id_group`),
  KEY `Id_etape` (`Id_etape`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `projet`
--

CREATE TABLE IF NOT EXISTS `projet` (
  `Id_projet` int(11) NOT NULL AUTO_INCREMENT,
  `Nom_projet` varchar(50) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `Id_Encadrant` int(11) NOT NULL,
  PRIMARY KEY (`Id_projet`),
  KEY `Id_Encadrant` (`Id_Encadrant`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `etudiant`
--
ALTER TABLE `etudiant`
  ADD CONSTRAINT `etudiant_ibfk_1` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`);

--
-- Contraintes pour la table `evaluation`
--
ALTER TABLE `evaluation`
  ADD CONSTRAINT `evaluation_ibfk_1` FOREIGN KEY (`Id_etape`) REFERENCES `etape` (`Id_etape`),
  ADD CONSTRAINT `evaluation_ibfk_2` FOREIGN KEY (`Id_Encadrant`) REFERENCES `encadrant` (`Id_Encadrant`),
  ADD CONSTRAINT `evaluation_ibfk_3` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`);

--
-- Contraintes pour la table `groupe`
--
ALTER TABLE `groupe`
  ADD CONSTRAINT `groupe_ibfk_1` FOREIGN KEY (`Id_projet`) REFERENCES `projet` (`Id_projet`);

--
-- Contraintes pour la table `livrable`
--
ALTER TABLE `livrable`
  ADD CONSTRAINT `livrable_ibfk_1` FOREIGN KEY (`Id_group`) REFERENCES `groupe` (`Id_group`),
  ADD CONSTRAINT `livrable_ibfk_2` FOREIGN KEY (`Id_etape`) REFERENCES `etape` (`Id_etape`);

--
-- Contraintes pour la table `projet`
--
ALTER TABLE `projet`
  ADD CONSTRAINT `projet_ibfk_1` FOREIGN KEY (`Id_Encadrant`) REFERENCES `encadrant` (`Id_Encadrant`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
