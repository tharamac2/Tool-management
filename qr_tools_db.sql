-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 11, 2026 at 11:46 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qr_tools_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alert`
--

CREATE TABLE `alert` (
  `type` varchar(255) NOT NULL,
  `severity` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` varchar(255) NOT NULL,
  `tool_id` int(11) DEFAULT NULL,
  `site` varchar(255) DEFAULT NULL,
  `date` datetime NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `is_resolved` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alert`
--

INSERT INTO `alert` (`type`, `severity`, `title`, `message`, `tool_id`, `site`, `date`, `is_read`, `is_resolved`, `id`) VALUES
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Aerial Roller for Earthwire (AE0226UJ001)', 1, '', '2026-02-24 11:54:44', 0, 0, 1),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Articulator Joints (AR0125HO002)', 2, '', '2026-02-24 12:00:06', 0, 0, 2),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Articulator Joints – 10T (AR0723TA003)', 3, '', '2026-02-24 14:45:59', 0, 0, 3),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Automatic Clamp for Earthwire – 7/3.66mm (AU1025TH004)', 4, '', '2026-02-24 14:48:36', 0, 0, 4),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: D-Shackles – 5T Cap (DX1124UJ005)', 5, '', '2026-02-24 14:50:45', 0, 0, 5),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Turn Table E/W – 5 Ton Cap (TU0126IR006)', 6, '', '2026-02-24 14:54:01', 0, 0, 6),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Conductor Drum Lifting Jacks (Manual) – 10T (CO0525SU007)', 7, '', '2026-02-25 11:03:26', 0, 0, 7),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Turn Table E/W – 5 Ton Cap (TU0126VI008)', 8, '', '2026-02-25 11:08:35', 0, 0, 8),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Winch Machine – 5T (With Mechanical Clamp) (WI0924UJ009)', 9, '', '2026-02-25 11:13:10', 0, 0, 9),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Chain Pulley – 10T Capacity (CH0625TA010)', 10, '', '2026-02-25 11:19:54', 0, 0, 10),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Aerial Roller for Earthwire (AE0226UJ001).', 1, 'Madurai', '2026-02-25 11:23:49', 0, 0, 11),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Articulator Joints (AR0125HO002).', 2, 'Coimbatore', '2026-02-25 11:26:22', 0, 0, 12),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Articulator Joints (AR0125HO002).', 2, 'Coimbatore', '2026-02-25 11:28:10', 0, 0, 13),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Articulator Joints – 10T (AR0723TA003).', 3, '', '2026-02-25 11:32:59', 0, 0, 14),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Automatic Clamp for Earthwire – 7/3.66mm (AU1025TH004).', 4, 'Trichy', '2026-02-25 11:37:02', 0, 0, 15),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for D-Shackles – 5T Cap (DX1124UJ005).', 5, 'Thoothukudi', '2026-02-25 11:40:34', 0, 0, 16),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Turn Table E/W – 5 Ton Cap (TU0126IR006).', 6, 'Kanyakumari', '2026-02-25 11:48:01', 0, 0, 17),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Conductor Drum Lifting Jacks (Manual) – 10T (CO0525SU007).', 7, 'Salem', '2026-02-25 11:54:18', 0, 0, 18),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Turn Table E/W – 5 Ton Cap (TU0126VI008).', 8, 'Theni', '2026-02-25 12:03:44', 0, 0, 19),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Winch Machine – 5T (With Mechanical Clamp) (WI0924UJ009).', 9, 'Hosur', '2026-02-25 12:04:24', 0, 0, 20),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Chain Pulley – 10T Capacity (CH0625TA010).', 10, 'Kanchipuram', '2026-02-25 12:05:46', 1, 0, 21),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Automatic Clamp for Earthwire – 7/3.66mm (AU1025TH004).', 4, 'Scrap Yard', '2026-02-25 12:17:41', 1, 0, 22),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Double sleeve open Pulley (DO0326IR007)', 11, '', '2026-03-23 16:11:56', 0, 0, 23),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Double sleeve open Pulley (DO0326TH007)', 12, '', '2026-03-23 16:17:26', 0, 0, 24),
('new-tool', 'info', 'New Tool Added', 'New tool has been added to the inventory: Articulator Joints – 10T (AR0326TH009)', 13, '', '2026-03-30 12:34:04', 0, 0, 25),
('tool-update', 'info', 'Tool Updated', 'Tool details updated for Articulator Joints – 10T (AR0723TA003).', 3, 'Coimbatore', '2026-04-08 11:08:12', 0, 0, 26),
('new-user', 'info', 'New User Created', 'New user created: Manager (admin)', NULL, 'Chennai', '2026-04-10 18:38:38', 0, 0, 27),
('new-user', 'info', 'New User Created', 'New user created: Tamil (store)', NULL, 'Chennai', '2026-04-11 13:49:31', 0, 0, 28),
('new-user', 'info', 'New User Created', 'New user created: Manoj (store)', NULL, 'Coimbatore', '2026-04-11 13:54:13', 0, 0, 29),
('new-user', 'info', 'New User Created', 'New user created: santhosh (store)', NULL, 'Thoothukudi', '2026-04-11 13:56:23', 0, 0, 30);

-- --------------------------------------------------------

--
-- Table structure for table `inspection`
--

CREATE TABLE `inspection` (
  `tool_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `result` varchar(255) NOT NULL,
  `usability_percentage` float DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `photos` varchar(255) DEFAULT NULL,
  `inspector_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inspection`
--

INSERT INTO `inspection` (`tool_id`, `date`, `result`, `usability_percentage`, `remarks`, `photos`, `inspector_id`, `id`) VALUES
(1, '2026-02-25 06:36:31', 'pass', NULL, 'Tool is in good working condition', '', 3, 1),
(2, '2026-02-09 18:30:00', 'pass', NULL, 'Minor wear and tear, safe to use', '', 1, 2),
(4, '2026-02-25 06:37:47', 'fail', NULL, 'Scrapped', '', 1, 3),
(5, '2026-02-01 18:30:00', 'pass', NULL, 'Tool is in good working condition', '', 1, 4),
(6, '2026-02-25 06:39:29', 'fail', NULL, 'Scrapped', '', 1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `movementhistory`
--

CREATE TABLE `movementhistory` (
  `tool_id` int(11) NOT NULL,
  `from_site` varchar(255) DEFAULT NULL,
  `to_site` varchar(255) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movementhistory`
--

INSERT INTO `movementhistory` (`tool_id`, `from_site`, `to_site`, `timestamp`, `remarks`, `user_id`, `id`) VALUES
(1, '', 'Madurai', '2026-02-25 11:23:49', 'Issued to Sub-Contractor. Tools is in Good Condition ', 1, 1),
(2, '', 'Coimbatore', '2026-02-25 11:26:22', 'Transferred to Site: Coimbatore. Tool Transferred from Main Store to Coimbatore Site', 1, 2),
(4, '', 'Trichy', '2026-02-25 11:37:02', 'Issued to Sub-Contractor. ', 1, 3),
(5, '', 'Thoothukudi', '2026-02-25 11:40:34', 'Issued to Sub-Contractor. ', 1, 4),
(6, '', 'Kanyakumari', '2026-02-25 11:48:01', 'Issued to Sub-Contractor. ', 1, 5),
(7, '', 'Salem', '2026-02-25 11:54:18', 'Issued to Sub-Contractor. ', 2, 6),
(8, '', 'Theni', '2026-02-25 12:03:44', 'Issued to Sub-Contractor. ', 2, 7),
(9, '', 'Hosur', '2026-02-25 12:04:24', 'Issued to Sub-Contractor. ', 2, 8),
(10, '', 'Kanchipuram', '2026-02-25 12:05:46', 'Issued to Sub-Contractor. ', 2, 9),
(4, 'Trichy', 'Scrap Yard', '2026-02-25 12:17:41', 'Sent to Scrap Dealer: Kamalesh (SD - 0001). ', 1, 10),
(3, '', 'Coimbatore', '2026-04-08 11:08:12', 'Transferred to Site: Coimbatore. ', 2, 11);

-- --------------------------------------------------------

--
-- Table structure for table `tool`
--

CREATE TABLE `tool` (
  `description` varchar(255) NOT NULL,
  `make` varchar(255) NOT NULL,
  `capacity` varchar(255) NOT NULL,
  `safe_working_load` varchar(255) NOT NULL,
  `tool_type` varchar(255) NOT NULL,
  `purchaser_name` varchar(255) DEFAULT NULL,
  `purchaser_contact` varchar(255) DEFAULT NULL,
  `supplier_code` varchar(255) DEFAULT NULL,
  `test_certificate` varchar(255) DEFAULT NULL,
  `date_of_supply` datetime DEFAULT NULL,
  `last_inspection_date` datetime DEFAULT NULL,
  `inspection_result` varchar(255) NOT NULL,
  `usability_percentage` float DEFAULT NULL,
  `validity_period` int(11) DEFAULT NULL,
  `subcontractor_name` varchar(255) DEFAULT NULL,
  `subcontractor_code` varchar(255) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `previous_site` varchar(255) DEFAULT NULL,
  `current_site` varchar(255) DEFAULT NULL,
  `next_site` varchar(255) DEFAULT NULL,
  `job_code` varchar(255) DEFAULT NULL,
  `job_description` varchar(255) DEFAULT NULL,
  `qr_code` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `expiry_date` datetime DEFAULT NULL,
  `debit_to` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tool`
--

INSERT INTO `tool` (`description`, `make`, `capacity`, `safe_working_load`, `tool_type`, `purchaser_name`, `purchaser_contact`, `supplier_code`, `test_certificate`, `date_of_supply`, `last_inspection_date`, `inspection_result`, `usability_percentage`, `validity_period`, `subcontractor_name`, `subcontractor_code`, `remarks`, `previous_site`, `current_site`, `next_site`, `job_code`, `job_description`, `qr_code`, `status`, `expiry_date`, `debit_to`, `id`) VALUES
('Aerial Roller for Earthwire', '2026', '5 Tonnes', '5 Tonnes', 'Erection Tools', 'UJ Enterprises', '9445438846', '001', '/uploads/e30af80c-7561-43b5-a86c-60513a5b0e18.pdf', '2026-02-10 00:00:00', '2026-02-25 06:36:31', 'usable', NULL, 3, 'Praveen', 'SC - 0001', 'Issued to Sub-Contractor. Tools is in Good Condition ', '', 'Madurai', '', 'JOB - 1', 'Tower ', 'AE0226UJ001', 'usable', '2029-02-10 00:00:00', NULL, 1),
('Articulator Joints', '2025', '3 Tonnes', '3 Tonnes', 'Erection Tools', 'Horizon Enterprises', '9123585284', '002', '/uploads/0b02fd20-051a-413e-90ba-9bd043a70455.pdf', '2025-01-10 00:00:00', '2026-02-09 18:30:00', 'usable', NULL, 3, 'Ranjith', 'SC - 0002', 'Issued to Sub-Contractor. Tool Transferred from Main Store to Coimbatore Site', 'Coimbatore', 'Coimbatore', '', 'JOB - 2', 'Bridge Construction', 'AR0125HO002', 'usable', '2028-01-10 00:00:00', NULL, 2),
('Articulator Joints – 10T', '2023', '4 Tonnes', '4 Tonnes', 'Erection Tools', 'TATA Steel', '7639762965', '003', '/uploads/c7febc2c-d079-4040-a6dc-445071c2d289.pdf', '2023-07-20 00:00:00', NULL, 'usable', NULL, 3, NULL, NULL, 'Transferred to Site: Coimbatore. ', '', 'Coimbatore', '', 'JOB - 3', 'Metro Construction', 'AR0723TA003', 'missing', '2026-07-20 00:00:00', '', 3),
('Automatic Clamp for Earthwire – 7/3.66mm', '2025', '2 Tonnes', '2 Tonnes', 'Erection Tools', 'Tharamac Enterprises', '9123585284', '004', '/uploads/2150799e-95e6-4683-922f-3d02b3cb7849.pdf', '2025-10-08 00:00:00', '2026-02-25 06:37:47', 'not-usable', NULL, 3, 'Kamalesh', 'SD - 0001', 'Sent to Scrap Dealer: Kamalesh (SD - 0001). ', 'Trichy', 'Scrap Yard', '', 'JOB - 4', 'Tower Construction', 'AU1025TH004', 'scrapped', '2028-10-08 00:00:00', NULL, 4),
('D-Shackles – 5T Cap', '2024', '6 Tonnes', '6 Tonnes', 'Erection Tools', 'UJT Enterprises', '9080174157', '005', '', '2024-11-20 00:00:00', '2026-02-01 18:30:00', 'usable', NULL, 3, 'Aravind', 'SC - 0005', 'Issued to Sub-Contractor. ', '', 'Thoothukudi', '', 'JOB - 5', 'Tower Construction', 'DX1124UJ005', 'usable', '2027-11-20 00:00:00', NULL, 5),
('Turn Table E/W – 5 Ton Cap', '2026', '5 Tonnes', '5 Tonnes', 'Erection Tools', 'IRT Enterprises', '9445438846', '006', '/uploads/92883994-aad3-4332-a85a-9bc2c5400f69.pdf', '2026-01-05 00:00:00', '2026-02-25 06:39:29', 'not-usable', NULL, 3, 'Nirmal Kumar', 'SC - 0006', 'Issued to Sub-Contractor. ', '', 'Kanyakumari', '', 'JOB - 6', 'Metro Construction', 'TU0126IR006', 'scrap', '2029-01-05 00:00:00', NULL, 6),
('Conductor Drum Lifting Jacks (Manual) – 10T', '2025', '10 Tonnes', '10 Tonnes', 'Erection Tools', 'Suriyan Enterprises', '9444454667', '007', '/uploads/12b33896-ffc3-438b-82db-92f40627da2b.pdf', '2025-05-15 00:00:00', NULL, 'usable', NULL, 3, 'Sathya', 'SC - 0007', 'Issued to Sub-Contractor. ', '', 'Salem', '', 'JOB - 7', 'Road Construction', 'CO0525SU007', 'usable', '2028-05-15 00:00:00', NULL, 7),
('Turn Table E/W – 5 Ton Cap', '2026', '5 Tonnes', '5 Tonnes', 'Erection Tools', 'Vijay enterprises', '9342798547', '008', '/uploads/c8eda9fa-a10a-49b4-8da6-b14cd0bb3fe4.pdf', '2026-01-20 00:00:00', NULL, 'usable', NULL, 3, 'Premkumar', 'SC - 0008', 'Issued to Sub-Contractor. ', '', 'Theni', '', 'JOB - 8', 'Tower Construction', 'TU0126VI008', 'usable', '2029-01-20 00:00:00', NULL, 8),
('Winch Machine – 5T (With Mechanical Clamp)', '2024', '5 Tonnes', '5 Tonnes', 'Erection Tools', 'UJT Enterprises', '9876543210', '009', '/uploads/8951f368-af64-479b-846c-aa2c71825a96.pdf', '2024-09-16 00:00:00', NULL, 'usable', NULL, 3, 'Jayaprakash', 'SC - 0009', 'Issued to Sub-Contractor. ', '', 'Hosur', '', 'JOB - 9', 'Tower Construction', 'WI0924UJ009', 'usable', '2027-09-16 00:00:00', NULL, 9),
('Chain Pulley – 10T Capacity', '2025', '10 Tonnes', '10 Tonnes', 'Erection Tools', 'TATA Enterprises', '9123456780', '010', '', '2025-06-10 00:00:00', NULL, 'usable', NULL, 3, 'Sekar', 'SC - 0010', 'Issued to Sub-Contractor. ', '', 'Kanchipuram', '', 'JOB - 10', 'Metro Construction', 'CH0625TA010', 'usable', '2028-06-10 00:00:00', NULL, 10),
('Double sleeve open Pulley', '2026', '4 Tonnes', '3 Tonnes', 'Erection Tools', 'IRT', '9123585284', '007', '', '2026-03-04 00:00:00', NULL, 'usable', NULL, 3, '', NULL, NULL, '', '', '', 'JOB - 6', 'Bridge Construction', 'DO0326IR007', 'usable', '2029-03-04 00:00:00', NULL, 11),
('Double sleeve open Pulley', '2026', '3 Tonnes', '3 Tonnes', 'Erection Tools', 'Tharamac', '9445438846', '007', '', '2026-03-05 00:00:00', NULL, 'usable', NULL, 3, '', NULL, NULL, '', '', '', 'JOB - 1', 'Tower ', 'DO0326TH007', 'usable', '2029-03-05 00:00:00', NULL, 12),
('Articulator Joints – 10T', '2026', '3 Tonnes', '3 Tonnes', 'Erection Tools', 'Tharamac', '9940180382', '009', '', '2026-03-30 00:00:00', NULL, 'usable', NULL, 3, '', NULL, NULL, '', '', '', 'JOB - 9', 'Bridge Construction', 'AR0326TH009', 'usable', '2029-03-30 00:00:00', NULL, 13);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `role` varchar(255) NOT NULL,
  `site` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `id` int(11) NOT NULL,
  `hashed_password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `email`, `full_name`, `role`, `site`, `phone`, `status`, `id`, `hashed_password`) VALUES
('admin', 'admin@example.com', 'Admin', 'admin', NULL, NULL, 'active', 1, '$2b$12$uTDQoH1QLtcZe3xdYL90seTfrA8Yn.VSZW0q9s22HjFhNfnibp4Uq'),
('store', 'store@example.com', 'Store Manager', 'store', 'Main Store', NULL, 'active', 2, '$2b$12$WdVrmbtwNmDIa22fDEo0ruzV8brJorThxK7P.tEIVNZRRvIkFN5jS'),
('inspector', 'inspector@example.com', NULL, 'inspector', NULL, NULL, 'active', 3, '$2b$12$36qgEveF74vPu.MHDKNtquYB0165XiGeMVnP0lU6uQvUsxQxLZ.Tu'),
('management', 'management@example.com', NULL, 'management', NULL, NULL, 'active', 4, '$2b$12$wtP2PnMmbboNRxKJ.VuuzuZvoQdUjnPKOwe0KHvSdVxb7ZIGV6MA6'),
('tamil@gmail.com', 'tamil@gmail.com', 'Chennai Site', 'store', 'Chennai', '9876543210', 'active', 6, '$2b$12$x4V4U7xkqmriOsHJWoHI7.ACoLDq7fH5Obi39iQTj6Xqni/fKEh/W'),
('manoj@gmail.com', 'manoj@gmail.com', 'Coimbatore Site', 'store', 'Coimbatore', '9876543210', 'active', 7, '$2b$12$CL1QTco1fYuyMnL8JhYiQOlkBul1fmCDT0onXcs6kBK9qBXEsfeNq');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alert`
--
ALTER TABLE `alert`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tool_id` (`tool_id`);

--
-- Indexes for table `inspection`
--
ALTER TABLE `inspection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tool_id` (`tool_id`),
  ADD KEY `inspector_id` (`inspector_id`);

--
-- Indexes for table `movementhistory`
--
ALTER TABLE `movementhistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tool_id` (`tool_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tool`
--
ALTER TABLE `tool`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_tool_qr_code` (`qr_code`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_user_username` (`username`),
  ADD UNIQUE KEY `ix_user_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alert`
--
ALTER TABLE `alert`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `inspection`
--
ALTER TABLE `inspection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `movementhistory`
--
ALTER TABLE `movementhistory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `tool`
--
ALTER TABLE `tool`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `alert`
--
ALTER TABLE `alert`
  ADD CONSTRAINT `alert_ibfk_1` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`);

--
-- Constraints for table `inspection`
--
ALTER TABLE `inspection`
  ADD CONSTRAINT `inspection_ibfk_1` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`),
  ADD CONSTRAINT `inspection_ibfk_2` FOREIGN KEY (`inspector_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `movementhistory`
--
ALTER TABLE `movementhistory`
  ADD CONSTRAINT `movementhistory_ibfk_1` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`id`),
  ADD CONSTRAINT `movementhistory_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
