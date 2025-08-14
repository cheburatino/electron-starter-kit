-- Срабатывает при создании или изменении записи в одной из таблиц коммуникаций
-- tg_bot, email...
CREATE OR REPLACE FUNCTION check_communication_channel_single_reference()
    RETURNS TRIGGER AS $$
DECLARE
    foundId int;
    tableName text;
    sqlQuery text;
BEGIN
    FOR tableName IN SELECT table_name FROM ctlg_communication_channel_type WHERE deleted_at IS NULL LOOP
            sqlQuery := format(
                    'SELECT id FROM %I WHERE communication_channel_id = $1 AND deleted_at IS NULL',
                    tableName
                );

            EXECUTE sqlQuery INTO foundId USING NEW.chatbot_platform_id;

            IF foundId IS NOT NULL THEN
                RAISE EXCEPTION 'Communication channel ID % is already referenced in table % with id: %',
                    NEW.chatbot_platform_id, tableName, foundId;
            END IF;
        END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
