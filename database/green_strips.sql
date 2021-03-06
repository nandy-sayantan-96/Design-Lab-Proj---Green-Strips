-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2019 at 08:30 PM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.1.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `green_strips`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `password`) VALUES
(2, 'admin1', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `purchase_type` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `o_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `u_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `total_amount` int(20) NOT NULL,
  `purchase_type` int(11) NOT NULL,
  `deliveryandpayment` varchar(50) NOT NULL DEFAULT 'yet to be done'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_details`
--

INSERT INTO `order_details` (`o_id`, `p_id`, `u_id`, `qty`, `total_amount`, `purchase_type`, `deliveryandpayment`) VALUES
(1, 1, 14, 3, 18, 0, 'yet to be done'),
(1, 1, 14, 4, 20, 1, 'yet to be done');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(50) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `image` varchar(50) NOT NULL,
  `price_ad` int(11) NOT NULL,
  `price_buy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`p_id`, `p_name`, `description`, `image`, `price_ad`, `price_buy`) VALUES
(1, 'Book Store Bag', 'SIZE : 12.5\" x 10\"\r\nSTRENGTH : Holds upto 3.5 kg.\r\nLIFE SPAN  : 2 months', '1.jpg', 5, 1),
(2, 'Medical Store Bag', 'SIZE : 9.5\" x 7\"\r\nSTRENGTH : Holds upto 2 kg.\r\nLIFE SPAN  : 2 months', '2.jpg', 4, 1),
(3, 'Pamphlets', 'SIZE : 7.5\" x 9\"\r\nMATERIAL : Eco - friendly paper.\r\nLIFE SPAN  : 6 months', '3.jpg', 3, 0);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `u_id` int(11) NOT NULL,
  `review` varchar(1000) NOT NULL,
  `p_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `f_name` varchar(20) NOT NULL,
  `l_name` varchar(20) NOT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `phone` int(11) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `f_name`, `l_name`, `organization`, `address`, `email`, `phone`, `password`) VALUES
(1, 'Sayantan', 'Nandy', 'asdasd', 'SAYANTAN NANDY,, P-111/B, C.I.T. ROAD, BELEGHATA,, Kolkata,, West Bengal,, pincode: 700010', 'xyz@abc.com', 2147483647, 'e034fb6b66aacc1d48f445ddfb08da98'),
(14, 'Sayantan', 'Nandy', 'dsad', 'SAYANTAN NANDY,, P-111/B, C.I.T. ROAD, BELEGHATA,, Kolkata,, West Bengal,, pincode: 700010', 'red@john.com', 703354841, '202cb962ac59075b964b07152d234b70');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_item_id`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD KEY `p_id` (`p_id`),
  ADD KEY `u_id` (`u_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD KEY `p_id` (`p_id`),
  ADD KEY `u_id` (`u_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`,`email`,`phone`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `products` (`p_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`u_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `products` (`p_id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`u_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
