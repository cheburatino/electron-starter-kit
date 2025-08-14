-- Информация о таблице
SELECT c.table_schema,
       c.table_name,
       c.column_name,
       c.data_type,
       c.character_maximum_length,
       c.is_nullable,
       pg_get_expr(d.adbin, d.adrelid) AS default_value,
       obj_description((c.table_schema || '.' || c.table_name)::regclass::oid, 'pg_class') AS table_comment,
       col_description((c.table_schema || '.' || c.table_name)::regclass::oid, c.ordinal_position) AS column_comment
FROM information_schema.columns c
         LEFT JOIN pg_attrdef d ON (d.adrelid = (c.table_schema || '.' || c.table_name)::regclass::oid
    AND d.adnum = c.ordinal_position)
WHERE c.table_schema = 'public'  -- Укажите схему
  AND c.table_name = 'tg_bot'  -- Укажите имя таблицы
ORDER BY c.ordinal_position;

-- Информация об индексах
SELECT
    i.relname AS index_name,
    a.attname AS column_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary,
    pg_get_indexdef(ix.indexrelid) AS index_definition
FROM
    pg_class t,
    pg_class i,
    pg_index ix,
    pg_attribute a
WHERE
        t.oid = ix.indrelid
  AND i.oid = ix.indexrelid
  AND a.attrelid = t.oid
  AND a.attnum = ANY(ix.indkey)
  AND t.relkind = 'r'
  AND t.relname = 'participant'  -- Укажите имя таблицы
ORDER BY
    i.relname,
    a.attnum;

-- Информация о триггерах
SELECT
    t.tgname AS trigger_name,
    pg_get_triggerdef(t.oid) AS trigger_definition,
    CASE
        WHEN t.tgenabled = 'O' THEN 'ORIGIN'
        WHEN t.tgenabled = 'D' THEN 'DISABLED'
        WHEN t.tgenabled = 'R' THEN 'REPLICA'
        WHEN t.tgenabled = 'A' THEN 'ALWAYS'
        END AS trigger_status,
    p.proname AS trigger_function
FROM
    pg_trigger t
        JOIN
    pg_class c ON t.tgrelid = c.oid
        JOIN
    pg_proc p ON t.tgfoid = p.oid
WHERE
        c.relname = 'user_auth'  -- Укажите имя таблицы
  AND NOT t.tgisinternal;

-- Информация о внешних ключах
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS references_table,
    ccu.column_name AS references_column,
    rc.delete_rule,
    rc.update_rule
FROM
    information_schema.table_constraints tc
        JOIN
    information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        JOIN
    information_schema.referential_constraints rc ON tc.constraint_name = rc.constraint_name
        JOIN
    information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
WHERE
        tc.table_name = 'user'  -- Укажите имя таблицы
  AND tc.constraint_type = 'FOREIGN KEY';
