-- Add deleted_at column to user_device table to support soft delete
ALTER TABLE user_device ADD COLUMN deleted_at TIMESTAMPTZ;

-- Add comment for the new column
COMMENT ON COLUMN user_device.deleted_at IS 'Дата и время удаления записи (soft delete)';

-- Create index for efficient queries excluding deleted records
CREATE INDEX user_device_deleted_at_idx ON user_device (id) WHERE (deleted_at IS NULL); 