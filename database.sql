-- Таблица пользователей
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INTEGER PRIMARY KEY,
    `username` TEXT,
    `connectTime` INTEGER,
    `firstname` TEXT,
    `lastname` TEXT,
    `referralID` INTEGER,
    `referralCount` INTEGER DEFAULT 0,
    `active` INTEGER DEFAULT 0,
    `complaintsCount` INTEGER DEFAULT 0,
    `rating` INTEGER DEFAULT 0,
    `status` TEXT DEFAULT 'FREE',
    `mutTime` INTEGER DEFAULT 0
);

-- Таблица очереди
CREATE TABLE IF NOT EXISTS `queue` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER UNIQUE
);

-- Таблица активных чатов
CREATE TABLE IF NOT EXISTS `chats` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user` INTEGER,
    `partner` INTEGER
);

-- Таблица истории
CREATE TABLE IF NOT EXISTS `history` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user` INTEGER,
    `partner` INTEGER DEFAULT 0,
    `opinionID` INTEGER DEFAULT 0
);