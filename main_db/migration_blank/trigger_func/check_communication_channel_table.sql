-- Функция триггера для проверки наличия таблицы и поля communication_channel_id
-- Триггер должен срабатывать на добавлении или изменении таблицы ctlg_communication_channel_type
CREATE OR REPLACE FUNCTION check_communication_channel_table()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем существование таблицы и поля communication_channel_id
    IF NEW.table_name IS NOT NULL THEN
        IF NOT check_table_and_column_exists(NULL, NEW.table_name, 'communication_channel_id') THEN
            RAISE EXCEPTION 'Table "%" does not exists or does not have field "communication_channel_id"', NEW.table_name;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
