-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 20 août 2023 à 16:23
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `codim_db`
--
CREATE DATABASE IF NOT EXISTS `codim_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `codim_db`;

-- --------------------------------------------------------

--
-- Structure de la table `corpus`
--

DROP TABLE IF EXISTS `corpus`;
CREATE TABLE IF NOT EXISTS `corpus` (
  `id_corpus` varchar(255) NOT NULL,
  `publisher_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `author_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `type_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `description_corpus` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`id_corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `corpus`
--
DROP TRIGGER IF EXISTS `before_insert_corpus_description`;
DELIMITER $$
CREATE TRIGGER `before_insert_corpus_description` BEFORE INSERT ON `corpus` FOR EACH ROW BEGIN
  IF LENGTH(NEW.description_corpus) > 65535 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for description_corpus. It should not exceed 65535 characters.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_corpus_type`;
DELIMITER $$
CREATE TRIGGER `before_insert_corpus_type` BEFORE INSERT ON `corpus` FOR EACH ROW BEGIN
  IF NEW.type_corpus NOT IN ('ecrit','écrit', 'oral', 'numérique', 'numerique', 'digital') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for type_corpus. It should be ecrit, écrit, oral, numérique, numerique or digital.';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `dm`
--

DROP TABLE IF EXISTS `dm`;
CREATE TABLE IF NOT EXISTS `dm` (
  `id_dm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `form_dm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id_dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `dm`
--
DROP TRIGGER IF EXISTS `before_insert_dm_form`;
DELIMITER $$
CREATE TRIGGER `before_insert_dm_form` BEFORE INSERT ON `dm` FOR EACH ROW BEGIN
  IF LENGTH(NEW.form_dm) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for form_dm. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `dm_utterance`
--

DROP TABLE IF EXISTS `dm_utterance`;
CREATE TABLE IF NOT EXISTS `dm_utterance` (
  `id_dm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_utterance` varchar(255) NOT NULL,
  `position` int NOT NULL,
  KEY `dm_utt_id_utterance_foreign` (`id_utterance`),
  KEY `dm_utt_id_dm_foreign` (`id_dm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `speaker`
--

DROP TABLE IF EXISTS `speaker`;
CREATE TABLE IF NOT EXISTS `speaker` (
  `id_speaker` varchar(255) NOT NULL,
  `name_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `age_speaker` int DEFAULT NULL,
  `gender_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `profession_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `birth_place_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `education_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `french_status_speaker` tinyint(1) DEFAULT NULL,
  `notes_speaker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id_speaker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `speaker`
--
DROP TRIGGER IF EXISTS `before_insert_speaker_age`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_age` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF NEW.age_speaker IS NOT NULL AND (NEW.age_speaker <= 0 OR NEW.age_speaker > 100) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for age_speaker. It should be a positive integer less than 100, or NULL value.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_speaker_birth_place`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_birth_place` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF LENGTH(NEW.birth_place_speaker) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for birth_place_speaker. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_speaker_education`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_education` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF LENGTH(NEW.education_speaker) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for education_speaker. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_speaker_french_status`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_french_status` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF NEW.french_status_speaker IS NOT NULL AND NEW.french_status_speaker NOT IN (0, 1) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for french_status_speaker. It should be 0 or 1.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_speaker_name`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_name` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF LENGTH(NEW.name_speaker) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for name_speaker. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_speaker_notes`;
DELIMITER $$
CREATE TRIGGER `before_insert_speaker_notes` BEFORE INSERT ON `speaker` FOR EACH ROW BEGIN
  IF LENGTH(NEW.notes_speaker) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for notes_speaker. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `speaker_utterance`
--

DROP TABLE IF EXISTS `speaker_utterance`;
CREATE TABLE IF NOT EXISTS `speaker_utterance` (
  `id_speaker` varchar(255) NOT NULL,
  `id_utterance` varchar(255) NOT NULL,
  KEY `id_speaker` (`id_speaker`),
  KEY `id_utterance` (`id_utterance`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `sub_corpus`
--

DROP TABLE IF EXISTS `sub_corpus`;
CREATE TABLE IF NOT EXISTS `sub_corpus` (
  `id_sub_corpus` varchar(255) NOT NULL,
  `id_corpus` varchar(255) NOT NULL,
  `link_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `date_sub_corpus` date DEFAULT NULL,
  `description_sub_corpus` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `author_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `type_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `right_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `duration_sub_corpus` decimal(10,0) DEFAULT NULL,
  `acoustic_quality_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `place_sub_corpus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id_sub_corpus`),
  KEY `transcription_id_corpus_foreign` (`id_corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `sub_corpus`
--
DROP TRIGGER IF EXISTS `before_insert_sub_corpus_acoustic_quality`;
DELIMITER $$
CREATE TRIGGER `before_insert_sub_corpus_acoustic_quality` BEFORE INSERT ON `sub_corpus` FOR EACH ROW BEGIN
  IF LENGTH(NEW.acoustic_quality_sub_corpus) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for acoustic_quality_sub_corpus. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_sub_corpus_date`;
DELIMITER $$
CREATE TRIGGER `before_insert_sub_corpus_date` BEFORE INSERT ON `sub_corpus` FOR EACH ROW BEGIN
  IF NEW.date_sub_corpus IS NOT NULL AND NEW.date_sub_corpus > CURRENT_DATE THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for date_sub_corpus. It should be a date on or before the current date.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_sub_corpus_duration`;
DELIMITER $$
CREATE TRIGGER `before_insert_sub_corpus_duration` BEFORE INSERT ON `sub_corpus` FOR EACH ROW BEGIN
  IF NEW.duration_sub_corpus IS NOT NULL AND NEW.duration_sub_corpus < 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for duration_sub_corpus. It should be a positive decimal or NULL.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_sub_corpus_place`;
DELIMITER $$
CREATE TRIGGER `before_insert_sub_corpus_place` BEFORE INSERT ON `sub_corpus` FOR EACH ROW BEGIN
  IF LENGTH(NEW.place_sub_corpus) > 255 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for place_sub_corpus. It should not exceed 255 characters.';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `utterance`
--

DROP TABLE IF EXISTS `utterance`;
CREATE TABLE IF NOT EXISTS `utterance` (
  `id_utterance` varchar(255) NOT NULL,
  `id_sub_corpus` varchar(255) NOT NULL,
  `text_utterance` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `start_utterance` decimal(10,6) DEFAULT NULL,
  `end_utterance` decimal(10,6) DEFAULT NULL,
  PRIMARY KEY (`id_utterance`),
  KEY `utterance_id_transcription_foreign` (`id_sub_corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déclencheurs `utterance`
--
DROP TRIGGER IF EXISTS `before_insert_utterance_start_end`;
DELIMITER $$
CREATE TRIGGER `before_insert_utterance_start_end` BEFORE INSERT ON `utterance` FOR EACH ROW BEGIN
  IF NEW.start_utterance IS NOT NULL AND (NEW.start_utterance < 0 OR NEW.start_utterance > 999999.999999) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for start_utterance. It should be a non-negative decimal with up to 6 decimal places.';
  END IF;
  
  IF NEW.end_utterance IS NOT NULL AND (NEW.end_utterance < 0 OR NEW.end_utterance > 999999.999999) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for end_utterance. It should be a non-negative decimal with up to 6 decimal places.';
  END IF;
  
  IF NEW.start_utterance IS NOT NULL AND NEW.end_utterance IS NOT NULL AND NEW.start_utterance > NEW.end_utterance THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'start_utterance cannot be greater than end_utterance.';
  END IF;
END
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `before_insert_utterance_text`;
DELIMITER $$
CREATE TRIGGER `before_insert_utterance_text` BEFORE INSERT ON `utterance` FOR EACH ROW BEGIN
  IF LENGTH(NEW.text_utterance) > 65535 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid value for text_utterance. It should not exceed 65535 characters.';
  END IF;
END
$$
DELIMITER ;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `dm_utterance`
--
ALTER TABLE `dm_utterance`
  ADD CONSTRAINT `dm_utt_id_dm_foreign` FOREIGN KEY (`id_dm`) REFERENCES `dm` (`id_dm`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `dm_utt_id_utterance_foreign` FOREIGN KEY (`id_utterance`) REFERENCES `utterance` (`id_utterance`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Contraintes pour la table `speaker_utterance`
--
ALTER TABLE `speaker_utterance`
  ADD CONSTRAINT `speaker_utterance_ibfk_1` FOREIGN KEY (`id_speaker`) REFERENCES `speaker` (`id_speaker`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `speaker_utterance_ibfk_2` FOREIGN KEY (`id_utterance`) REFERENCES `utterance` (`id_utterance`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `sub_corpus`
--
ALTER TABLE `sub_corpus`
  ADD CONSTRAINT `transcription_id_corpus_foreign` FOREIGN KEY (`id_corpus`) REFERENCES `corpus` (`id_corpus`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `utterance`
--
ALTER TABLE `utterance`
  ADD CONSTRAINT `utterance_id_transcription_foreign` FOREIGN KEY (`id_sub_corpus`) REFERENCES `sub_corpus` (`id_sub_corpus`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
