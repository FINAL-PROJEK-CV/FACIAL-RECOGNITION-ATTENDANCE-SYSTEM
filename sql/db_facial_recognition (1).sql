-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 11, 2022 at 02:39 PM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_facial_recognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE `log` (
  `id` int(11) NOT NULL,
  `log` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `log`
--

INSERT INTO `log` (`id`, `log`, `timestamp`) VALUES
(1, 'Login', '2022-05-20 15:43:47'),
(2, 'validasi error', '2022-05-20 15:43:47'),
(3, 'Login', '2022-05-20 15:43:49'),
(4, 'validasi error', '2022-05-20 15:43:49'),
(5, 'Login', '2022-05-20 15:43:54'),
(6, 'validasi error', '2022-05-20 15:43:54'),
(7, 'Login', '2022-05-20 15:43:54'),
(8, 'validasi error', '2022-05-20 15:43:54'),
(9, 'Login', '2022-05-20 15:43:55'),
(10, 'validasi error', '2022-05-20 15:43:55'),
(11, 'Login', '2022-05-20 15:43:59'),
(12, 'validasi error', '2022-05-20 15:43:59'),
(13, 'Login', '2022-05-20 15:44:00'),
(14, 'validasi error', '2022-05-20 15:44:00'),
(15, 'Login', '2022-05-20 15:44:12'),
(16, 'validasi error', '2022-05-20 15:44:14'),
(17, 'Login', '2022-05-20 15:44:15'),
(18, 'validasi error', '2022-05-20 15:44:15'),
(19, 'Login', '2022-05-20 15:44:15'),
(20, 'validasi error', '2022-05-20 15:44:15'),
(21, 'Login', '2022-05-20 15:44:15'),
(22, 'validasi error', '2022-05-20 15:44:15'),
(23, 'Login', '2022-05-20 15:44:15'),
(24, 'validasi error', '2022-05-20 15:44:15'),
(25, 'Login', '2022-05-20 15:44:48'),
(26, 'validasi error', '2022-05-20 15:44:48'),
(27, 'Login', '2022-05-20 15:44:49'),
(28, 'validasi error', '2022-05-20 15:44:49'),
(29, 'Login', '2022-05-20 15:44:50'),
(30, 'validasi error', '2022-05-20 15:44:50'),
(31, 'Login', '2022-05-20 15:47:39'),
(32, 'Login', '2022-05-20 15:47:42'),
(33, 'Log out', '2022-05-20 15:47:48'),
(34, 'Log out', '2022-05-20 15:47:51'),
(35, 'Login', '2022-06-07 03:47:34'),
(36, 'Lihat data', '2022-06-07 03:47:41'),
(37, 'TAKE IMAGE|', '2022-06-07 03:51:23'),
(38, 'TrainingImage', '2022-06-07 03:51:35'),
(39, 'Proses Train Berhasil', '2022-06-07 03:51:40'),
(40, 'Lihat data', '2022-06-07 03:51:45'),
(41, 'Presensi dimulai', '2022-06-07 03:51:55'),
(42, 'presensi|3|hadir', '2022-06-07 03:52:16'),
(43, 'presensi|1|hadir', '2022-06-07 03:52:16'),
(44, 'Presensi dimulai', '2022-06-07 03:53:03'),
(45, 'Lihat data', '2022-06-07 03:53:44'),
(46, 'Presensi dimulai', '2022-06-07 03:57:22'),
(47, 'Log out', '2022-06-07 03:59:05'),
(48, 'Login', '2022-06-07 04:01:25'),
(49, 'Lihat data', '2022-06-07 04:02:31'),
(50, 'Waktu Presensi Diperbaharui', '2022-06-07 04:03:59'),
(51, 'Presensi dimulai', '2022-06-07 04:04:03'),
(52, 'Waktu Presensi Diperbaharui', '2022-06-07 04:05:23'),
(53, 'Waktu Presensi Diperbaharui', '2022-06-07 04:06:06'),
(54, 'Log out', '2022-06-07 04:07:39'),
(55, 'Log out', '2022-06-07 07:21:22'),
(56, 'Login', '2022-06-09 05:50:59'),
(57, 'Lihat data', '2022-06-09 05:51:07'),
(58, 'Presensi dimulai', '2022-06-09 05:51:21'),
(59, 'presensi|1|terlambat', '2022-06-09 05:51:44'),
(60, 'presensi|3|terlambat', '2022-06-09 05:51:44'),
(61, 'presensi|987|terlambat', '2022-06-09 05:51:45'),
(62, 'Log out', '2022-06-09 06:36:14'),
(63, 'Log out', '2022-06-09 08:17:12');

-- --------------------------------------------------------

--
-- Table structure for table `tb_admin`
--

CREATE TABLE `tb_admin` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(300) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_telp` varchar(100) NOT NULL,
  `alamat` text NOT NULL,
  `deskripsi` text NOT NULL,
  `img` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_admin`
--

INSERT INTO `tb_admin` (`id`, `username`, `password`, `nama`, `jabatan`, `email`, `no_telp`, `alamat`, `deskripsi`, `img`, `role`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'ganang', 'Direktur', 'ganangsaputro38@gmail.com', '08989861169', 'Jl Aku Suka Kamu No 3 Tersesat', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.11111111111', '20220428clockin1.jpg', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `tb_camera`
--

CREATE TABLE `tb_camera` (
  `id` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_controls`
--

CREATE TABLE `tb_controls` (
  `id` int(11) NOT NULL,
  `automation` int(1) NOT NULL,
  `start` int(10) NOT NULL,
  `stop` int(10) NOT NULL,
  `train` int(10) NOT NULL,
  `destroy` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_controls`
--

INSERT INTO `tb_controls` (`id`, `automation`, `start`, `stop`, `train`, `destroy`) VALUES
(1, 1, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_mlx90614`
--

CREATE TABLE `tb_mlx90614` (
  `id` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `ambient_temp` varchar(10) NOT NULL,
  `object_temp` varchar(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_presensi`
--

CREATE TABLE `tb_presensi` (
  `id` int(11) NOT NULL,
  `enrollment` int(120) NOT NULL,
  `nama` varchar(300) NOT NULL,
  `tanggal` date NOT NULL,
  `clockin` varchar(120) NOT NULL,
  `c_in` varchar(120) NOT NULL,
  `clockout` varchar(120) NOT NULL,
  `c_out` varchar(120) NOT NULL,
  `img_in` varchar(300) NOT NULL,
  `img_out` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_presensi`
--

INSERT INTO `tb_presensi` (`id`, `enrollment`, `nama`, `tanggal`, `clockin`, `c_in`, `clockout`, `c_out`, `img_in`, `img_out`) VALUES
(1, 3, 'Ganang Ganang', '2022-06-07', '10:52:16', '', '', '', 'GanangGanang20220607clockin.jpg', ''),
(2, 1, 'herryan', '2022-06-07', '10:52:16', '', '', '', 'herryan20220607clockin.jpg', ''),
(3, 1, 'herryan', '2022-06-09', '12:51:44', 'terlambat', '', '', 'herryan20220609clockin.jpg', ''),
(4, 3, 'Ganang Ganang', '2022-06-09', '12:51:44', 'terlambat', '', '', 'GanangGanang20220609clockin.jpg', ''),
(5, 987, 'fina', '2022-06-09', '12:51:45', 'terlambat', '', '', 'fina20220609clockin.jpg', '');

-- --------------------------------------------------------

--
-- Table structure for table `tb_raspberry`
--

CREATE TABLE `tb_raspberry` (
  `id` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tb_take_image`
--

CREATE TABLE `tb_take_image` (
  `id` int(11) NOT NULL,
  `enrollment` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jabatan` varchar(300) NOT NULL,
  `alamat` text NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_take_image`
--

INSERT INTO `tb_take_image` (`id`, `enrollment`, `nama`, `jabatan`, `alamat`, `status`) VALUES
(1, '', '', 'Manager', 'Jl aku suka kamu no 3 tersesat', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_users`
--

CREATE TABLE `tb_users` (
  `id` int(11) NOT NULL,
  `enrollment` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_users`
--

INSERT INTO `tb_users` (`id`, `enrollment`, `nama`, `jabatan`, `alamat`, `status`) VALUES
(1, '3', 'Ganang', 'Direktur', 'Tambaksogra', 'registered');

-- --------------------------------------------------------

--
-- Table structure for table `tb_waktu_keluar`
--

CREATE TABLE `tb_waktu_keluar` (
  `id` int(11) NOT NULL,
  `dari` varchar(100) NOT NULL,
  `sampai` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_waktu_keluar`
--

INSERT INTO `tb_waktu_keluar` (`id`, `dari`, `sampai`) VALUES
(1, '150000', '220000');

-- --------------------------------------------------------

--
-- Table structure for table `tb_waktu_masuk`
--

CREATE TABLE `tb_waktu_masuk` (
  `id` int(11) NOT NULL,
  `dari` varchar(100) NOT NULL,
  `sampai` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_waktu_masuk`
--

INSERT INTO `tb_waktu_masuk` (`id`, `dari`, `sampai`) VALUES
(1, '06000', '14000');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_admin`
--
ALTER TABLE `tb_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_camera`
--
ALTER TABLE `tb_camera`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_controls`
--
ALTER TABLE `tb_controls`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_mlx90614`
--
ALTER TABLE `tb_mlx90614`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_presensi`
--
ALTER TABLE `tb_presensi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_raspberry`
--
ALTER TABLE `tb_raspberry`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_take_image`
--
ALTER TABLE `tb_take_image`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_users`
--
ALTER TABLE `tb_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `enrollment` (`enrollment`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `log`
--
ALTER TABLE `log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `tb_admin`
--
ALTER TABLE `tb_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tb_camera`
--
ALTER TABLE `tb_camera`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tb_controls`
--
ALTER TABLE `tb_controls`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tb_mlx90614`
--
ALTER TABLE `tb_mlx90614`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tb_presensi`
--
ALTER TABLE `tb_presensi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tb_raspberry`
--
ALTER TABLE `tb_raspberry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tb_take_image`
--
ALTER TABLE `tb_take_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
