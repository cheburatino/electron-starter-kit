--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: check_communication_channel_single_reference(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_communication_channel_single_reference() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
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
$_$;


ALTER FUNCTION public.check_communication_channel_single_reference() OWNER TO postgres;

--
-- Name: check_communication_channel_table(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_communication_channel_table() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Проверяем существование таблицы и поля communication_channel_id
    IF NEW.table_name IS NOT NULL THEN
        IF NOT check_table_and_column_exists(NULL, NEW.table_name, 'communication_channel_id') THEN
            RAISE EXCEPTION 'Table "%" does not exists or does not have field "communication_channel_id"', NEW.table_name;
        END IF;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_communication_channel_table() OWNER TO postgres;

--
-- Name: FUNCTION check_communication_channel_table(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.check_communication_channel_table() IS 'Функция для проверки существования таблицы с полем communication_channel_id при добавлении или изменении типа канала коммуникации';


--
-- Name: check_table_and_column_exists(text, text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_table_and_column_exists(target_schema_name text, target_table_name text, target_column_name text) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.check_table_and_column_exists(target_schema_name text, target_table_name text, target_column_name text) OWNER TO postgres;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
   NEW.updated_at = now();
   RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

--
-- Name: FUNCTION update_updated_at_column(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.update_updated_at_column() IS 'Функция-триггер, которая устанавливает текущее время в поле updated_at при обновлении строки.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: user_auth_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_auth_token (
    id integer NOT NULL,
    device_id integer NOT NULL,
    client_app character varying(100),
    access_token text,
    refresh_token text,
    access_token_expires_at timestamp with time zone,
    refresh_token_expires_at timestamp with time zone,
    is_active boolean DEFAULT true,
    last_used_at timestamp with time zone,
    ip_address character varying(45),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.user_auth_token OWNER TO postgres;

--
-- Name: TABLE user_auth_token; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_auth_token IS 'Токены авторизации для участников системы';


--
-- Name: COLUMN user_auth_token.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN user_auth_token.device_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.device_id IS 'Ссылка на устройство';


--
-- Name: COLUMN user_auth_token.client_app; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.client_app IS 'Идентификатор приложения или браузера на устройстве';


--
-- Name: COLUMN user_auth_token.access_token; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.access_token IS 'Короткоживущий токен доступа (JWT)';


--
-- Name: COLUMN user_auth_token.refresh_token; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.refresh_token IS 'Долгоживущий токен обновления (JWT)';


--
-- Name: COLUMN user_auth_token.access_token_expires_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.access_token_expires_at IS 'Время истечения срока действия токена доступа';


--
-- Name: COLUMN user_auth_token.refresh_token_expires_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.refresh_token_expires_at IS 'Время истечения срока действия токена обновления';


--
-- Name: COLUMN user_auth_token.is_active; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.is_active IS 'Активна ли сессия авторизации';


--
-- Name: COLUMN user_auth_token.last_used_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.last_used_at IS 'Время последнего использования токена';


--
-- Name: COLUMN user_auth_token.ip_address; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.ip_address IS 'IP-адрес, с которого был получен токен';


--
-- Name: COLUMN user_auth_token.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.created_at IS 'Время создания записи';


--
-- Name: COLUMN user_auth_token.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_token.updated_at IS 'Время последнего обновления записи';


--
-- Name: auth_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_token_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_token_id_seq OWNER TO postgres;

--
-- Name: auth_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_token_id_seq OWNED BY public.user_auth_token.id;


--
-- Name: chatbot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chatbot (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.chatbot OWNER TO postgres;

--
-- Name: TABLE chatbot; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.chatbot IS 'Таблица для хранения чат-ботов, которые могут работать через разные платформы';


--
-- Name: COLUMN chatbot.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.id IS 'Уникальный идентификатор чат-бота';


--
-- Name: COLUMN chatbot.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.name IS 'Название чат-бота';


--
-- Name: COLUMN chatbot.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.description IS 'Описание чат-бота и его назначения';


--
-- Name: COLUMN chatbot.is_active; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.is_active IS 'Флаг активности чат-бота';


--
-- Name: COLUMN chatbot.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN chatbot.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN chatbot.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.chatbot.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: chatbot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chatbot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chatbot_id_seq OWNER TO postgres;

--
-- Name: chatbot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chatbot_id_seq OWNED BY public.chatbot.id;


--
-- Name: communication_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communication_channel (
    id integer NOT NULL,
    type_id integer NOT NULL,
    title character varying(255) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.communication_channel OWNER TO postgres;

--
-- Name: TABLE communication_channel; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.communication_channel IS 'Таблица для хранения каналов коммуникации (мессенджеры, email, sms и т.д.)';


--
-- Name: COLUMN communication_channel.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.id IS 'Уникальный идентификатор канала коммуникации';


--
-- Name: COLUMN communication_channel.type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.type_id IS 'Идентификатор типа канала коммуникации';


--
-- Name: COLUMN communication_channel.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.title IS 'Название канала коммуникации';


--
-- Name: COLUMN communication_channel.is_active; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.is_active IS 'Флаг активности канала коммуникации';


--
-- Name: COLUMN communication_channel.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN communication_channel.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN communication_channel.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.communication_channel.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: communication_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.communication_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.communication_channel_id_seq OWNER TO postgres;

--
-- Name: communication_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.communication_channel_id_seq OWNED BY public.communication_channel.id;


--
-- Name: ctlg_communication_channel_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_communication_channel_type (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone,
    table_name character varying(50) NOT NULL,
    encrypt_key_env_var_name character varying(128) NOT NULL
);


ALTER TABLE public.ctlg_communication_channel_type OWNER TO postgres;

--
-- Name: TABLE ctlg_communication_channel_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_communication_channel_type IS 'Справочник типов каналов коммуникации';


--
-- Name: COLUMN ctlg_communication_channel_type.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.id IS 'Уникальный идентификатор типа канала коммуникации';


--
-- Name: COLUMN ctlg_communication_channel_type.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.code IS 'Символьный код типа канала коммуникации';


--
-- Name: COLUMN ctlg_communication_channel_type.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.title IS 'Название типа канала коммуникации';


--
-- Name: COLUMN ctlg_communication_channel_type.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN ctlg_communication_channel_type.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN ctlg_communication_channel_type.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_communication_channel_type.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: ctlg_communication_channel_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_communication_channel_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_communication_channel_type_id_seq OWNER TO postgres;

--
-- Name: ctlg_communication_channel_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_communication_channel_type_id_seq OWNED BY public.ctlg_communication_channel_type.id;


--
-- Name: ctlg_user_device_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_user_device_type (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ctlg_user_device_type OWNER TO postgres;

--
-- Name: TABLE ctlg_user_device_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_user_device_type IS 'Справочник типов устройств для авторизации';


--
-- Name: COLUMN ctlg_user_device_type.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.id IS 'Уникальный идентификатор типа устройства';


--
-- Name: COLUMN ctlg_user_device_type.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.code IS 'Символьный код типа устройства (например, web, mobile, desktop)';


--
-- Name: COLUMN ctlg_user_device_type.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.title IS 'Название типа устройства';


--
-- Name: COLUMN ctlg_user_device_type.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.description IS 'Описание типа устройства';


--
-- Name: COLUMN ctlg_user_device_type.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.created_at IS 'Время создания записи';


--
-- Name: COLUMN ctlg_user_device_type.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_type.updated_at IS 'Время последнего обновления записи';


--
-- Name: ctlg_device_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_device_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_device_type_id_seq OWNER TO postgres;

--
-- Name: ctlg_device_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_device_type_id_seq OWNED BY public.ctlg_user_device_type.id;


--
-- Name: ctlg_participant_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_participant_type (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    title character varying(255),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ctlg_participant_type OWNER TO postgres;

--
-- Name: TABLE ctlg_participant_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_participant_type IS 'Справочник типов участников коммуникации.';


--
-- Name: COLUMN ctlg_participant_type.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_participant_type.id IS 'Уникальный идентификатор типа участника';


--
-- Name: COLUMN ctlg_participant_type.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_participant_type.code IS 'Код типа участника (например, person, neuroperson, tg_bot)';


--
-- Name: COLUMN ctlg_participant_type.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_participant_type.title IS 'Описание типа участника';


--
-- Name: COLUMN ctlg_participant_type.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_participant_type.created_at IS 'Время создания записи типа';


--
-- Name: COLUMN ctlg_participant_type.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_participant_type.updated_at IS 'Время последнего обновления записи типа';


--
-- Name: ctlg_participant_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_participant_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_participant_type_id_seq OWNER TO postgres;

--
-- Name: ctlg_participant_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_participant_type_id_seq OWNED BY public.ctlg_participant_type.id;


--
-- Name: ctlg_user_auth_reason; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_user_auth_reason (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    code character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.ctlg_user_auth_confirm_code_reason OWNER TO postgres;

--
-- Name: TABLE ctlg_user_auth_reason; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_user_auth_confirm_code_reason IS 'Справочник причин аутентификации пользователей';


--
-- Name: COLUMN ctlg_user_auth_reason.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN ctlg_user_auth_reason.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.title IS 'Наименование причины аутентификации';


--
-- Name: COLUMN ctlg_user_auth_reason.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.code IS 'Уникальный код причины аутентификации';


--
-- Name: COLUMN ctlg_user_auth_reason.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN ctlg_user_auth_reason.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN ctlg_user_auth_reason.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_confirm_code_reason.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: ctlg_person_auth_reason_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_person_auth_reason_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_person_auth_reason_id_seq OWNER TO postgres;

--
-- Name: ctlg_person_auth_reason_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_person_auth_reason_id_seq OWNED BY public.ctlg_user_auth_confirm_code_reason.id;


--
-- Name: ctlg_user_auth_comm_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_user_auth_comm_channel (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    code character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.ctlg_user_auth_comm_channel OWNER TO postgres;

--
-- Name: TABLE ctlg_user_auth_comm_channel; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_user_auth_comm_channel IS 'Справочник типов аутентификации пользователей (email, telegram и т.д.)';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.title IS 'Наименование типа аутентификации';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.code IS 'Уникальный код типа аутентификации';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN ctlg_user_auth_comm_channel.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_auth_comm_channel.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: ctlg_person_auth_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_person_auth_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_person_auth_type_id_seq OWNER TO postgres;

--
-- Name: ctlg_person_auth_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_person_auth_type_id_seq OWNED BY public.ctlg_user_auth_comm_channel.id;


--
-- Name: ctlg_user_device_app; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ctlg_user_device_app (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    code character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.ctlg_user_device_app OWNER TO postgres;

--
-- Name: TABLE ctlg_user_device_app; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.ctlg_user_device_app IS 'Справочник типов приложений для устройств пользователей';


--
-- Name: COLUMN ctlg_user_device_app.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN ctlg_user_device_app.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.title IS 'Наименование типа приложения';


--
-- Name: COLUMN ctlg_user_device_app.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.code IS 'Уникальный код типа приложения';


--
-- Name: COLUMN ctlg_user_device_app.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN ctlg_user_device_app.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN ctlg_user_device_app.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.ctlg_user_device_app.deleted_at IS 'Дата и время удаления записи';


--
-- Name: ctlg_user_device_app_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ctlg_user_device_app_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ctlg_user_device_app_id_seq OWNER TO postgres;

--
-- Name: ctlg_user_device_app_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ctlg_user_device_app_id_seq OWNED BY public.ctlg_user_device_app.id;


--
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization (
    id integer NOT NULL,
    participant_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.organization OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_id_seq OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organization_id_seq OWNED BY public.organization.id;


--
-- Name: participant; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant (
    id integer NOT NULL,
    participant_type_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.participant OWNER TO postgres;

--
-- Name: TABLE participant; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.participant IS 'Центральная таблица для идентификации участников коммуникации (людей, ботов, нейроперсон).';


--
-- Name: COLUMN participant.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participant.id IS 'Уникальный идентификатор участника.';


--
-- Name: COLUMN participant.participant_type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participant.participant_type_id IS 'Ссылка на тип участника в справочнике ctlg_participant_type.';


--
-- Name: COLUMN participant.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participant.created_at IS 'Время создания записи участника.';


--
-- Name: COLUMN participant.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participant.updated_at IS 'Время последнего обновления записи участника.';


--
-- Name: participant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_id_seq OWNER TO postgres;

--
-- Name: participant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person (
    id integer NOT NULL,
    last_name character varying(100),
    first_name character varying(100),
    middle_name character varying(100),
    birth_date date,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone,
    participant_id integer NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Name: TABLE person; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.person IS 'Человек';


--
-- Name: COLUMN person.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.id IS 'Уникальный идентификатор';


--
-- Name: COLUMN person.last_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.last_name IS 'Фамилия';


--
-- Name: COLUMN person.first_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.first_name IS 'Имя';


--
-- Name: COLUMN person.middle_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.middle_name IS 'Отчество';


--
-- Name: COLUMN person.birth_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.birth_date IS 'Дата рождения';


--
-- Name: COLUMN person.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.created_at IS 'Время создания записи';


--
-- Name: COLUMN person.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.updated_at IS 'Время последнего обновления записи';


--
-- Name: COLUMN person.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.person.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: tg_bot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tg_bot (
    id integer NOT NULL,
    title character varying(150),
    description text,
    library_id integer,
    is_active boolean DEFAULT false NOT NULL,
    encrypted_token bytea,
    communication_channel_id integer NOT NULL
);


ALTER TABLE public.tg_bot OWNER TO postgres;

--
-- Name: tg_bot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tg_bot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tg_bot_id_seq OWNER TO postgres;

--
-- Name: tg_bot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tg_bot_id_seq OWNED BY public.tg_bot.id;


--
-- Name: tg_bot_library; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tg_bot_library (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    class_name character varying(50) NOT NULL
);


ALTER TABLE public.tg_bot_library OWNER TO postgres;

--
-- Name: TABLE tg_bot_library; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tg_bot_library IS 'Библиотеки для реализации телеграм ботов';


--
-- Name: COLUMN tg_bot_library.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tg_bot_library.id IS 'Уникальный идентификатор';


--
-- Name: COLUMN tg_bot_library.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tg_bot_library.title IS 'Название';


--
-- Name: COLUMN tg_bot_library.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tg_bot_library.description IS 'Описание';


--
-- Name: COLUMN tg_bot_library.class_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tg_bot_library.class_name IS 'Имя класса';


--
-- Name: tg_bot_library_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tg_bot_library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tg_bot_library_id_seq OWNER TO postgres;

--
-- Name: tg_bot_library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tg_bot_library_id_seq OWNED BY public.tg_bot_library.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    person_id integer,
    auth_email character varying(255),
    auth_telegram_id character varying(100),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone,
    has_access boolean DEFAULT false NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: TABLE "user"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."user" IS 'Таблица пользователей системы (аккаунты)';


--
-- Name: COLUMN "user".id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN "user".person_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".person_id IS 'Связь с записью в таблице person';


--
-- Name: COLUMN "user".auth_email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".auth_email IS 'Email для аутентификации';


--
-- Name: COLUMN "user".auth_telegram_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".auth_telegram_id IS 'Telegram ID для аутентификации';


--
-- Name: COLUMN "user".created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN "user".updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN "user".deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: COLUMN "user".has_access; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".has_access IS 'Флаг доступа пользователя к системе';


--
-- Name: user_auth; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_auth (
    id integer NOT NULL,
    user_id integer,
    reason_id integer NOT NULL,
    ip_address inet,
    comm_channel_id integer NOT NULL,
    comm_channel_address character varying(255) NOT NULL,
    device_id integer,
    confirm_code character varying(50) NOT NULL,
    is_sent boolean DEFAULT false,
    sending_error text,
    is_used boolean DEFAULT false,
    attempts_count integer DEFAULT 0,
    last_attempt_at timestamp with time zone,
    expires_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.user_auth_confirm_code OWNER TO postgres;

--
-- Name: TABLE user_auth; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_auth_confirm_code IS 'Таблица для хранения данных аутентификации пользователей';


--
-- Name: COLUMN user_auth.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN user_auth.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.user_id IS 'Идентификатор пользователя из таблицы user';


--
-- Name: COLUMN user_auth.reason_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.reason_id IS 'Причина аутентификации из справочника ctlg_person_auth_reason';


--
-- Name: COLUMN user_auth.ip_address; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.ip_address IS 'IP-адрес, с которого производится аутентификация';


--
-- Name: COLUMN user_auth.comm_channel_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.comm_channel_id IS 'Тип аутентификации из справочника ctlg_person_auth_type';


--
-- Name: COLUMN user_auth.comm_channel_address; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.comm_channel_address IS 'Адрес для аутентификации (email или username телеграм)';


--
-- Name: COLUMN user_auth.device_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.device_id IS 'Идентификатор устройства, с которого производится аутентификация';


--
-- Name: COLUMN user_auth.confirm_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.confirm_code IS 'Код подтверждения';


--
-- Name: COLUMN user_auth.is_sent; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.is_sent IS 'Флаг успешной отправки кода';


--
-- Name: COLUMN user_auth.sending_error; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.sending_error IS 'Ошибка отправки кода, если есть';


--
-- Name: COLUMN user_auth.is_used; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.is_used IS 'Флаг успешного использования кода';


--
-- Name: COLUMN user_auth.attempts_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.attempts_count IS 'Количество попыток использования кода';


--
-- Name: COLUMN user_auth.last_attempt_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.last_attempt_at IS 'Время последней попытки использования кода';


--
-- Name: COLUMN user_auth.expires_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.expires_at IS 'Время истечения срока действия кода';


--
-- Name: COLUMN user_auth.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN user_auth.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN user_auth.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_auth_confirm_code.deleted_at IS 'Дата и время удаления записи (soft delete)';


--
-- Name: user_auth_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_auth_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_auth_id_seq OWNER TO postgres;

--
-- Name: user_auth_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_auth_id_seq OWNED BY public.user_auth_confirm_code.id;


--
-- Name: user_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_device (
    id integer NOT NULL,
    device_id_ext character varying(100) NOT NULL,
    device_type_id integer NOT NULL,
    last_seen_at timestamp with time zone,
    user_agent text,
    device_name character varying(255),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_device OWNER TO postgres;

--
-- Name: TABLE user_device; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_device IS 'Устройства пользователей для авторизации';


--
-- Name: COLUMN user_device.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device.id IS 'Уникальный идентификатор устройства в системе';


--
-- Name: COLUMN user_device.device_id_ext; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device.device_id_ext IS 'Внешний идентификатор устройства, полученный от клиента';


--
-- Name: COLUMN user_device.device_type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device.device_type_id IS 'Ссылка на тип устройства в справочнике ctlg_device_type';


--
-- Name: user_device_app; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_device_app (
    id integer NOT NULL,
    user_id integer NOT NULL,
    app_type_id integer NOT NULL,
    user_device_id integer NOT NULL,
    app_version character varying(50),
    device_info jsonb,
    is_active boolean DEFAULT true,
    last_active_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    deleted_at timestamp with time zone
);


ALTER TABLE public.user_device_app OWNER TO postgres;

--
-- Name: TABLE user_device_app; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_device_app IS 'Таблица приложений на устройствах пользователей';


--
-- Name: COLUMN user_device_app.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.id IS 'Уникальный идентификатор записи';


--
-- Name: COLUMN user_device_app.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.user_id IS 'Идентификатор пользователя';


--
-- Name: COLUMN user_device_app.app_type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.app_type_id IS 'Тип приложения из справочника ctlg_user_device_app';


--
-- Name: COLUMN user_device_app.user_device_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.user_device_id IS 'Идентификатор устройства пользователя';


--
-- Name: COLUMN user_device_app.app_version; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.app_version IS 'Версия приложения';


--
-- Name: COLUMN user_device_app.device_info; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.device_info IS 'Информация об устройстве в формате JSON (user agent, platform, etc)';


--
-- Name: COLUMN user_device_app.is_active; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.is_active IS 'Флаг активности приложения';


--
-- Name: COLUMN user_device_app.last_active_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.last_active_at IS 'Время последней активности';


--
-- Name: COLUMN user_device_app.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.created_at IS 'Дата и время создания записи';


--
-- Name: COLUMN user_device_app.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.updated_at IS 'Дата и время последнего обновления записи';


--
-- Name: COLUMN user_device_app.deleted_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_device_app.deleted_at IS 'Дата и время удаления записи';


--
-- Name: user_device_app_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_device_app_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_device_app_id_seq OWNER TO postgres;

--
-- Name: user_device_app_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_device_app_id_seq OWNED BY public.user_device_app.id;


--
-- Name: user_device_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_device_id_seq OWNER TO postgres;

--
-- Name: user_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_device_id_seq OWNED BY public.user_device.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: chatbot id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chatbot ALTER COLUMN id SET DEFAULT nextval('public.chatbot_id_seq'::regclass);


--
-- Name: communication_channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communication_channel ALTER COLUMN id SET DEFAULT nextval('public.communication_channel_id_seq'::regclass);


--
-- Name: ctlg_communication_channel_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_communication_channel_type ALTER COLUMN id SET DEFAULT nextval('public.ctlg_communication_channel_type_id_seq'::regclass);


--
-- Name: ctlg_participant_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_participant_type ALTER COLUMN id SET DEFAULT nextval('public.ctlg_participant_type_id_seq'::regclass);


--
-- Name: ctlg_user_auth_comm_channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_auth_comm_channel ALTER COLUMN id SET DEFAULT nextval('public.ctlg_person_auth_type_id_seq'::regclass);


--
-- Name: ctlg_user_auth_reason id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_auth_confirm_code_reason ALTER COLUMN id SET DEFAULT nextval('public.ctlg_person_auth_reason_id_seq'::regclass);


--
-- Name: ctlg_user_device_app id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_device_app ALTER COLUMN id SET DEFAULT nextval('public.ctlg_user_device_app_id_seq'::regclass);


--
-- Name: ctlg_user_device_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_device_type ALTER COLUMN id SET DEFAULT nextval('public.ctlg_device_type_id_seq'::regclass);


--
-- Name: organization id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization ALTER COLUMN id SET DEFAULT nextval('public.organization_id_seq'::regclass);


--
-- Name: participant id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);


--
-- Name: tg_bot id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot ALTER COLUMN id SET DEFAULT nextval('public.tg_bot_id_seq'::regclass);


--
-- Name: tg_bot_library id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot_library ALTER COLUMN id SET DEFAULT nextval('public.tg_bot_library_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_auth id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code ALTER COLUMN id SET DEFAULT nextval('public.user_auth_id_seq'::regclass);


--
-- Name: user_auth_token id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_token ALTER COLUMN id SET DEFAULT nextval('public.auth_token_id_seq'::regclass);


--
-- Name: user_device id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device ALTER COLUMN id SET DEFAULT nextval('public.user_device_id_seq'::regclass);


--
-- Name: user_device_app id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device_app ALTER COLUMN id SET DEFAULT nextval('public.user_device_app_id_seq'::regclass);


--
-- Data for Name: chatbot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chatbot (id, name, description, is_active, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: communication_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communication_channel (id, type_id, title, is_active, created_at, updated_at, deleted_at) FROM stdin;
1	1	Electron assistant telegram bot	t	2025-05-22 07:29:58.484383+00	2025-05-22 07:29:58.484383+00	\N
\.


--
-- Data for Name: ctlg_communication_channel_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_communication_channel_type (id, code, title, created_at, updated_at, deleted_at, table_name, encrypt_key_env_var_name) FROM stdin;
1	tg_bot	Telegram Bot	2025-05-21 13:50:14.053113+00	2025-05-22 09:07:25.717256+00	\N	tg_bot	TG_BOT_TOKEN_ENCRYPT_KEY
\.


--
-- Data for Name: ctlg_participant_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_participant_type (id, code, title, created_at, updated_at) FROM stdin;
1	person	Person	2025-05-20 16:26:45.681475+00	2025-05-20 16:26:45.681475+00
2	organization	Organization	2025-05-20 16:27:00.491805+00	2025-05-20 16:27:00.491805+00
3	neuroperson	Neuroperson	2025-05-20 16:27:20.348859+00	2025-05-20 16:27:20.348859+00
\.


--
-- Data for Name: ctlg_user_auth_comm_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_user_auth_comm_channel (id, title, code, created_at, updated_at, deleted_at) FROM stdin;
1	Email	email	2025-05-19 18:41:32.709177+00	2025-05-19 18:41:32.709177+00	\N
2	Telegram	telegram	2025-05-19 18:41:32.709177+00	2025-05-19 18:41:32.709177+00	\N
\.


--
-- Data for Name: ctlg_user_auth_reason; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_user_auth_confirm_code_reason (id, title, code, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: ctlg_user_device_app; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_user_device_app (id, title, code, created_at, updated_at, deleted_at) FROM stdin;
1	Веб-браузер	web	2025-05-19 21:46:41.813854+00	2025-05-19 21:46:41.813854+00	\N
2	Мобильное приложение	mobile	2025-05-19 21:46:41.813854+00	2025-05-19 21:46:41.813854+00	\N
3	Настольное приложение	desktop	2025-05-19 21:46:41.813854+00	2025-05-19 21:46:41.813854+00	\N
\.


--
-- Data for Name: ctlg_user_device_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ctlg_user_device_type (id, code, title, description, created_at, updated_at) FROM stdin;
1	web	Веб-браузер	Стандартный веб-браузер на компьютере или мобильном устройстве	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
2	mobile_app	Мобильное приложение	Нативное мобильное приложение (iOS, Android)	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
3	desktop_app	Настольное приложение	Нативное настольное приложение (Windows, macOS, Linux)	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
4	tablet	Планшет	Браузер на планшетном устройстве	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
5	smart_tv	Smart TV	Приложение или браузер на Smart TV устройстве	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
6	api_client	API клиент	Программный клиент, использующий API напрямую	2025-05-14 09:30:37.472882+00	2025-05-14 09:30:37.472882+00
\.


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization (id, participant_id, title, description, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: participant; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant (id, participant_type_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person (id, last_name, first_name, middle_name, birth_date, created_at, updated_at, deleted_at, participant_id) FROM stdin;
\.


--
-- Data for Name: tg_bot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tg_bot (id, title, description, library_id, is_active, encrypted_token, communication_channel_id) FROM stdin;
1	Electron assistant	Main bot	1	t	\N	1
\.


--
-- Data for Name: tg_bot_library; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tg_bot_library (id, title, description, class_name) FROM stdin;
1	Python telegram bot	Библиотека Python telegram bot (Ptb). Импортируется как import telegram	PtbTgBotClient
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, person_id, auth_email, auth_telegram_id, created_at, updated_at, deleted_at, has_access) FROM stdin;
\.


--
-- Data for Name: user_auth; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_auth_confirm_code (id, user_id, reason_id, ip_address, comm_channel_id, comm_channel_address, device_id, confirm_code, is_sent, sending_error, is_used, attempts_count, last_attempt_at, expires_at, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: user_auth_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_auth_token (id, device_id, client_app, access_token, refresh_token, access_token_expires_at, refresh_token_expires_at, is_active, last_used_at, ip_address, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: user_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_device (id, device_id_ext, device_type_id, last_seen_at, user_agent, device_name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_device_app; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_device_app (id, user_id, app_type_id, user_device_id, app_version, device_info, is_active, last_active_at, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Name: auth_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_token_id_seq', 1, false);


--
-- Name: chatbot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chatbot_id_seq', 1, false);


--
-- Name: communication_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.communication_channel_id_seq', 1, true);


--
-- Name: ctlg_communication_channel_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_communication_channel_type_id_seq', 1, true);


--
-- Name: ctlg_device_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_device_type_id_seq', 6, true);


--
-- Name: ctlg_participant_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_participant_type_id_seq', 3, true);


--
-- Name: ctlg_person_auth_reason_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_person_auth_reason_id_seq', 1, false);


--
-- Name: ctlg_person_auth_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_person_auth_type_id_seq', 2, true);


--
-- Name: ctlg_user_device_app_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ctlg_user_device_app_id_seq', 3, true);


--
-- Name: organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organization_id_seq', 1, false);


--
-- Name: participant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_id_seq', 1, false);


--
-- Name: tg_bot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tg_bot_id_seq', 2, false);


--
-- Name: tg_bot_library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tg_bot_library_id_seq', 1, true);


--
-- Name: user_auth_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_auth_id_seq', 1, false);


--
-- Name: user_device_app_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_device_app_id_seq', 1, false);


--
-- Name: user_device_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_device_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: user_auth_token auth_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_token
    ADD CONSTRAINT auth_token_pkey PRIMARY KEY (id);


--
-- Name: chatbot chatbot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chatbot
    ADD CONSTRAINT chatbot_pkey PRIMARY KEY (id);


--
-- Name: communication_channel communication_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communication_channel
    ADD CONSTRAINT communication_channel_pkey PRIMARY KEY (id);


--
-- Name: ctlg_communication_channel_type ctlg_communication_channel_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_communication_channel_type
    ADD CONSTRAINT ctlg_communication_channel_type_pkey PRIMARY KEY (id);


--
-- Name: ctlg_user_device_type ctlg_device_type_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_device_type
    ADD CONSTRAINT ctlg_device_type_code_key UNIQUE (code);


--
-- Name: ctlg_user_device_type ctlg_device_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_device_type
    ADD CONSTRAINT ctlg_device_type_pkey PRIMARY KEY (id);


--
-- Name: ctlg_participant_type ctlg_participant_type_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_participant_type
    ADD CONSTRAINT ctlg_participant_type_code_key UNIQUE (code);


--
-- Name: ctlg_participant_type ctlg_participant_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_participant_type
    ADD CONSTRAINT ctlg_participant_type_pkey PRIMARY KEY (id);


--
-- Name: ctlg_user_auth_reason ctlg_person_auth_reason_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_auth_confirm_code_reason
    ADD CONSTRAINT ctlg_person_auth_reason_pkey PRIMARY KEY (id);


--
-- Name: ctlg_user_auth_comm_channel ctlg_person_auth_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_auth_comm_channel
    ADD CONSTRAINT ctlg_person_auth_type_pkey PRIMARY KEY (id);


--
-- Name: ctlg_user_device_app ctlg_user_device_app_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ctlg_user_device_app
    ADD CONSTRAINT ctlg_user_device_app_pkey PRIMARY KEY (id);


--
-- Name: user_device device_device_id_ext_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device
    ADD CONSTRAINT device_device_id_ext_key UNIQUE (device_id_ext);


--
-- Name: user_device device_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device
    ADD CONSTRAINT device_pkey PRIMARY KEY (id);


--
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- Name: participant participant_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: tg_bot_library tg_bot_library_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot_library
    ADD CONSTRAINT tg_bot_library_pkey PRIMARY KEY (id);


--
-- Name: tg_bot tg_bot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot
    ADD CONSTRAINT tg_bot_pkey PRIMARY KEY (id);


--
-- Name: user_auth_token uk_auth_token_user_device_client; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_token
    ADD CONSTRAINT uk_auth_token_user_device_client UNIQUE (user_id, device_id, client_app);


--
-- Name: organization uq_organization_participant; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT uq_organization_participant UNIQUE (participant_id);


--
-- Name: person uq_person_participant; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT uq_person_participant UNIQUE (participant_id);


--
-- Name: user_auth user_auth_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code
    ADD CONSTRAINT user_auth_pkey PRIMARY KEY (id);


--
-- Name: user_device_app user_device_app_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device_app
    ADD CONSTRAINT user_device_app_pkey PRIMARY KEY (id);


--
-- Name: user user_person_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_person_id_key UNIQUE (person_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ctlg_communication_channel_type_code_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ctlg_communication_channel_type_code_idx ON public.ctlg_communication_channel_type USING btree (code) WHERE (deleted_at IS NULL);


--
-- Name: ctlg_user_auth_comm_channel_code_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ctlg_user_auth_comm_channel_code_idx ON public.ctlg_user_auth_comm_channel USING btree (code) WHERE (deleted_at IS NULL);


--
-- Name: ctlg_user_auth_reason_code_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ctlg_user_auth_reason_code_idx ON public.ctlg_user_auth_confirm_code_reason USING btree (code) WHERE (deleted_at IS NULL);


--
-- Name: ctlg_user_device_app_code_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ctlg_user_device_app_code_idx ON public.ctlg_user_device_app USING btree (code) WHERE (deleted_at IS NULL);


--
-- Name: user_auth_auth_address_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_auth_auth_address_idx ON public.user_auth_confirm_code USING btree (comm_channel_address) WHERE (deleted_at IS NULL);


--
-- Name: user_auth_confirm_code_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_auth_confirm_code_idx ON public.user_auth_confirm_code USING btree (confirm_code) WHERE ((deleted_at IS NULL) AND (NOT is_used) AND (attempts_count < 3));


--
-- Name: user_auth_device_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_auth_device_id_idx ON public.user_auth_confirm_code USING btree (device_id) WHERE (deleted_at IS NULL);


--
-- Name: user_auth_email_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX user_auth_email_idx ON public."user" USING btree (auth_email) WHERE ((deleted_at IS NULL) AND (auth_email IS NOT NULL));


--
-- Name: user_auth_ip_address_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_auth_ip_address_idx ON public.user_auth_confirm_code USING btree (ip_address) WHERE (deleted_at IS NULL);


--
-- Name: user_auth_telegram_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX user_auth_telegram_id_idx ON public."user" USING btree (auth_telegram_id) WHERE ((deleted_at IS NULL) AND (auth_telegram_id IS NOT NULL));


--
-- Name: user_auth_user_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_auth_user_id_idx ON public.user_auth_confirm_code USING btree (user_id) WHERE (deleted_at IS NULL);


--
-- Name: user_device_app_unique_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX user_device_app_unique_idx ON public.user_device_app USING btree (user_id, user_device_id, app_type_id) WHERE (deleted_at IS NULL);


--
-- Name: user_device_app_user_device_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_device_app_user_device_id_idx ON public.user_device_app USING btree (user_device_id) WHERE (deleted_at IS NULL);


--
-- Name: user_device_app_user_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_device_app_user_id_idx ON public.user_device_app USING btree (user_id) WHERE (deleted_at IS NULL);


--
-- Name: user_has_access_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_has_access_idx ON public."user" USING btree (has_access) WHERE (deleted_at IS NULL);


--
-- Name: ctlg_communication_channel_type tr_check_communication_channel_table; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_check_communication_channel_table BEFORE INSERT OR UPDATE ON public.ctlg_communication_channel_type FOR EACH ROW EXECUTE FUNCTION public.check_communication_channel_table();


--
-- Name: user_auth_token trigger_update_auth_token_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_auth_token_updated_at BEFORE UPDATE ON public.user_auth_token FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: chatbot trigger_update_chatbot_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_chatbot_updated_at BEFORE UPDATE ON public.chatbot FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: communication_channel trigger_update_communication_channel_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_communication_channel_updated_at BEFORE UPDATE ON public.communication_channel FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_communication_channel_type trigger_update_ctlg_communication_channel_type_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_ctlg_communication_channel_type_updated_at BEFORE UPDATE ON public.ctlg_communication_channel_type FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_user_device_type trigger_update_ctlg_device_type_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_ctlg_device_type_updated_at BEFORE UPDATE ON public.ctlg_user_device_type FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_participant_type trigger_update_ctlg_participant_type_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_ctlg_participant_type_updated_at BEFORE UPDATE ON public.ctlg_participant_type FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_device trigger_update_device_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_device_updated_at BEFORE UPDATE ON public.user_device FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: organization trigger_update_organization_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_organization_updated_at BEFORE UPDATE ON public.organization FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: participant trigger_update_participant_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_participant_updated_at BEFORE UPDATE ON public.participant FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: person trigger_update_person_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_person_updated_at BEFORE UPDATE ON public.person FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_user_auth_reason update_ctlg_person_auth_reason_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_ctlg_person_auth_reason_updated_at BEFORE UPDATE ON public.ctlg_user_auth_confirm_code_reason FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_user_auth_comm_channel update_ctlg_person_auth_type_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_ctlg_person_auth_type_updated_at BEFORE UPDATE ON public.ctlg_user_auth_comm_channel FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: ctlg_user_device_app update_ctlg_user_device_app_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_ctlg_user_device_app_updated_at BEFORE UPDATE ON public.ctlg_user_device_app FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_auth update_user_auth_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_user_auth_updated_at BEFORE UPDATE ON public.user_auth_confirm_code FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_device_app update_user_device_app_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_user_device_app_updated_at BEFORE UPDATE ON public.user_device_app FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user update_user_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON public."user" FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: communication_channel communication_channel_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communication_channel
    ADD CONSTRAINT communication_channel_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.ctlg_communication_channel_type(id);


--
-- Name: user_auth_token fk_auth_token_device; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_token
    ADD CONSTRAINT fk_auth_token_device FOREIGN KEY (device_id) REFERENCES public.user_device(id) ON DELETE CASCADE;


--
-- Name: user_auth_token fk_auth_token_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_token
    ADD CONSTRAINT fk_auth_token_user FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: user_device fk_device_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device
    ADD CONSTRAINT fk_device_type FOREIGN KEY (device_type_id) REFERENCES public.ctlg_user_device_type(id);


--
-- Name: organization fk_organization_participant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT fk_organization_participant FOREIGN KEY (participant_id) REFERENCES public.participant(id);


--
-- Name: participant fk_participant_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT fk_participant_type FOREIGN KEY (participant_type_id) REFERENCES public.ctlg_participant_type(id) ON DELETE RESTRICT;


--
-- Name: person fk_person_participant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT fk_person_participant FOREIGN KEY (participant_id) REFERENCES public.participant(id);


--
-- Name: user_auth person_auth_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code
    ADD CONSTRAINT person_auth_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.user_device(id);


--
-- Name: user_auth person_auth_reason_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code
    ADD CONSTRAINT person_auth_reason_id_fkey FOREIGN KEY (reason_id) REFERENCES public.ctlg_user_auth_confirm_code_reason(id);


--
-- Name: tg_bot tg_bot_communication_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot
    ADD CONSTRAINT tg_bot_communication_channel_id_fkey FOREIGN KEY (communication_channel_id) REFERENCES public.communication_channel(id);


--
-- Name: tg_bot tg_bot_library_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tg_bot
    ADD CONSTRAINT tg_bot_library_id_fkey FOREIGN KEY (library_id) REFERENCES public.tg_bot_library(id) ON DELETE RESTRICT;


--
-- Name: user_auth user_auth_comm_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code
    ADD CONSTRAINT user_auth_comm_channel_id_fkey FOREIGN KEY (comm_channel_id) REFERENCES public.ctlg_user_auth_comm_channel(id);


--
-- Name: user_auth user_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_auth_confirm_code
    ADD CONSTRAINT user_auth_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_device_app user_device_app_app_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device_app
    ADD CONSTRAINT user_device_app_app_type_id_fkey FOREIGN KEY (app_type_id) REFERENCES public.ctlg_user_device_app(id);


--
-- Name: user_device_app user_device_app_user_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device_app
    ADD CONSTRAINT user_device_app_user_device_id_fkey FOREIGN KEY (user_device_id) REFERENCES public.user_device(id);


--
-- Name: user_device_app user_device_app_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_device_app
    ADD CONSTRAINT user_device_app_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user user_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.person(id);


--
-- PostgreSQL database dump complete
--

