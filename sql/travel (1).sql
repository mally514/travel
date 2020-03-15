-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 15, 2020 at 09:50 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel`
--

-- --------------------------------------------------------

--
-- Table structure for table `joins`
--

CREATE TABLE `joins` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `wish_item_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `joins`
--

INSERT INTO `joins` (`id`, `user_id`, `wish_item_id`, `created_at`) VALUES
(8, 7, 7, '2020-03-15 07:50:16'),
(10, 7, 7, '2020-03-15 08:04:09'),
(13, 5, 8, '2020-03-15 08:18:42'),
(14, 5, 7, '2020-03-15 08:40:11');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_hired` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `password`, `date_hired`, `created_at`, `updated_at`) VALUES
(5, 'Mark', 'mark', 'password', '2020-03-12 00:00:00', '2020-03-15 07:42:20', '2020-03-15 07:42:20'),
(6, 'steve', 'steve', 'password', '2020-03-05 00:00:00', '2020-03-15 07:42:48', '2020-03-15 07:42:48'),
(7, 'brian', 'brian', 'password', '0000-00-00 00:00:00', '2020-03-15 07:43:06', '2020-03-15 07:43:06');

-- --------------------------------------------------------

--
-- Table structure for table `wish_items`
--

CREATE TABLE `wish_items` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `item_product` varchar(225) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `wish_items`
--

INSERT INTO `wish_items` (`id`, `user_id`, `item_product`, `created_at`, `updated_at`) VALUES
(7, 6, 'iphone', '2020-03-15 07:49:59', '2020-03-15 07:49:59'),
(8, 5, 'computer', '2020-03-15 08:15:11', '2020-03-15 08:15:11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `joins`
--
ALTER TABLE `joins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wish_items`
--
ALTER TABLE `wish_items`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `joins`
--
ALTER TABLE `joins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `wish_items`
--
ALTER TABLE `wish_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
