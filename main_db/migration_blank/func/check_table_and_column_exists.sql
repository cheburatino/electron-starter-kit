CREATE OR REPLACE FUNCTION check_table_and_column_exists(target_schema_name text, target_table_name text, target_column_name text)
    RETURNS boolean AS $$
DECLARE
    schema text;
BEGIN
    -- Если схема не указана, используем public
    IF target_schema_name IS NULL THEN
        schema := 'public';
    ELSE
        schema := target_schema_name;
    END IF;

    -- Проверка существования таблицы и столбца
    RETURN EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = schema AND table_name = target_table_name AND column_name = target_column_name
        );
END;
$$ LANGUAGE plpgsql;
