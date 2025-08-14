-- Initial schema for assistant application
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test table to verify migrations work
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    message TEXT DEFAULT 'Migration system works!'
);