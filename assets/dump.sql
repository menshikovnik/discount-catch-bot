--
-- PostgreSQL database dump
--

-- Dumped from database version 16rc1
-- Dumped by pg_dump version 16rc1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: user_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_products (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    article character varying(255) NOT NULL,
    price numeric(10,2) NOT NULL,
    url character varying(255),
    name_of_product character varying(255)
);


ALTER TABLE public.user_products OWNER TO postgres;

--
-- Name: user_products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_products_id_seq OWNER TO postgres;

--
-- Name: user_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_products_id_seq OWNED BY public.user_products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    chat_id bigint NOT NULL,
    username character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: user_products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_products ALTER COLUMN id SET DEFAULT nextval('public.user_products_id_seq'::regclass);


--
-- Data for Name: user_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_products (id, username, article, price, url, name_of_product) FROM stdin;
9	menshikovnik	28188889	549.00	https://tinyurl.com/26e84zsa	Сухой корм для собак мелких пород от 10 месяцев Royal Canin Mini Adult, с птицей, 800 г
10	menshikovnik	1140623086	446.00	https://tinyurl.com/2a6d9osu	Мышь беспроводная для ноутбука бесшумная компьютерная игровая оптическая мышка, с подсветкой, М102
11	menshikovnik	487262987	339.00	https://tinyurl.com/2y3w4qrr	Антибликовые очки для водителя / очки поляризационные мужские 2 шт. / очки для рыбалки
12	yannybol	249608950	747.00	https://tinyurl.com/2auo78pg	Kerasys УКРЕПЛЯЮЩИЙ корейский шампунь для сияния волос 470 мл, ORIENTAL PREMIUM Профессиональный увлажняющий от выпадения волос, Корея
7	menshikovnik	1419011041	460.00	https://tinyurl.com/27khrwhw	Защитный чехол на Apple iPhone 13 Pro (С принтом мишки)
8	menshikovnik	912328914	6890.00	https://tinyurl.com/24r93amd	Toshiba 2 ТБ Внешний жесткий диск (HDTB520EK3AA), черный матовый
6	menshikovnik	713264136	308.00	https://tinyurl.com/27mef5fa	Силиконовый,защитный чехол с рисунком Black Bear/Черный Медведь на Apple IPhone 13 Pro/Айфон 13 Про
13	vegaldn	1345363213	1305.00	https://tinyurl.com/2blzd7d5	Машинка игрушка металлическая Ferrari Laferrari 1:24
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, chat_id, username) FROM stdin;
446109205	446109205	menshikovnik
474177073	474177073	yannybol
409438517	409438517	vegaldn
\.


--
-- Name: user_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_products_id_seq', 13, true);


--
-- Name: user_products user_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_products
    ADD CONSTRAINT user_products_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- PostgreSQL database dump complete
--

