-- Remove deleted_at column from user_device table
DROP INDEX IF EXISTS user_device_deleted_at_idx;
ALTER TABLE user_device DROP COLUMN IF EXISTS deleted_at; 