--
-- PostgreSQL database dump
--

-- Dumped from database version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)

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
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    admin_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- Name: admins_admin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.admins_admin_id_seq OWNER TO postgres;

--
-- Name: admins_admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_admin_id_seq OWNED BY public.admins.admin_id;


--
-- Name: belong_to_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.belong_to_order (
    order_id integer NOT NULL,
    goods_id integer NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT belong_to_order_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.belong_to_order OWNER TO postgres;

--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    user_id integer NOT NULL,
    goods_id integer NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT carts_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: goods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.goods (
    goods_id integer NOT NULL,
    typename character varying(255) NOT NULL,
    goodsname character varying(255) NOT NULL,
    price numeric(10,2) NOT NULL,
    sales integer DEFAULT 0 NOT NULL,
    discount numeric(3,2),
    CONSTRAINT goods_discount_check CHECK (((discount >= (0)::numeric) AND (discount <= (1)::numeric)))
);


ALTER TABLE public.goods OWNER TO postgres;

--
-- Name: goods_goods_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.goods_goods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.goods_goods_id_seq OWNER TO postgres;

--
-- Name: goods_goods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.goods_goods_id_seq OWNED BY public.goods.goods_id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    user_id integer NOT NULL,
    totalprice numeric(10,2) NOT NULL,
    orderdate timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_order_id_seq OWNER TO postgres;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    sex character(1),
    birthday date,
    address text,
    phone character varying(20),
    email character varying(25),
    CONSTRAINT users_sex_check CHECK ((sex = ANY (ARRAY['M'::bpchar, 'F'::bpchar, 'O'::bpchar])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: admins admin_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN admin_id SET DEFAULT nextval('public.admins_admin_id_seq'::regclass);


--
-- Name: goods goods_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goods ALTER COLUMN goods_id SET DEFAULT nextval('public.goods_goods_id_seq'::regclass);


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (admin_id, username, password) FROM stdin;
3	admin	$2b$12$5Svk5h1YsBe5YPsyvg7n9OpPEePwgcVbx./JtVMjNRo4paghHYULu
\.


--
-- Data for Name: belong_to_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.belong_to_order (order_id, goods_id, quantity) FROM stdin;
1	7	1
1	2	2
\.


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carts (user_id, goods_id, quantity) FROM stdin;
\.


--
-- Data for Name: goods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.goods (goods_id, typename, goodsname, price, sales, discount) FROM stdin;
1	饮品	牛奶	32.80	0	1.00
3	水果	苹果	6.99	0	1.00
4	食品	饼干	17.99	0	1.00
5	饮品	矿泉水	2.99	0	1.00
6	日用品	纸巾	27.99	0	1.00
8	数码	iPhone	9.99	0	0.10
9	图书	红楼梦	49.99	0	1.00
10	日用品	牙刷	10.99	0	1.00
11	服装	帽子	37.99	0	1.00
12	家电	冰箱	99.99	0	1.00
13	医药	消毒水	5.99	0	1.00
14	数码	键盘	79.99	0	1.00
15	美妆	面霜	45.99	0	1.00
16	日用品	雨伞	25.99	0	1.00
7	食品	蛋糕	8.99	1	1.00
2	食品	方便面	7.99	2	0.90
17	测试类	数据库	13.00	0	0.90
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (order_id, user_id, totalprice, orderdate) FROM stdin;
1	3	23.37	2024-07-06 21:07:05
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password, sex, birthday, address, phone, email) FROM stdin;
1	lzz	123456	M	2024-07-06	sysu	123	lzz@163.com
2	lzz_enc	$2b$12$Fw/x.ZAgVm2EJZMOzhCKSOlxUQqL0nbrcRtX2hALVXLxzQzecwgii	M	2024-07-05	addr	16606688655	lzz@163.com
3	lz	$2b$12$VVa5phJycx/6yVgTRrVgg.SwwIksu/FLpbNIolBy6mAX7Xfzq24uW	M	2024-07-06	addr	111	1a@mail.com
4	newuser	$2b$12$fR20t3EZj/IJd4OUmi/PX.p/XRrID0Viba3QUUiyfe8ZFGul7GFhi	M	1990-01-01	123 Main St	1234567890	newuser@example.com
6	newuser1	$2b$12$N88JgQrfKXTrrIM7S8Ji9ebcRxf8fBNKr0LZ.EchmLp8ELuQ62gMy	M	1990-01-01	123 Main St	1234567890	newuser@example.com
7	testuser	$2b$12$eC1hZbUuWuGqXK27rxwjJOLtQh4yIc.1Le6lr6zJgrYTaNXqlMEZG	\N	2024-07-09	123 Main St	1234567890	testuser@example.com
8	newuser_1720534225	password123	M	2000-01-01	123 Main St, City	1234567890	newuser@example.com
10	newuser_1720534865	password123	M	2000-01-01	123 Main St, City	1234567890	newuser@example.com
\.


--
-- Name: admins_admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_admin_id_seq', 3, true);


--
-- Name: goods_goods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.goods_goods_id_seq', 17, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 10, true);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (admin_id);


--
-- Name: admins admins_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_username_key UNIQUE (username);


--
-- Name: belong_to_order belong_to_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belong_to_order
    ADD CONSTRAINT belong_to_order_pkey PRIMARY KEY (order_id, goods_id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (user_id, goods_id);


--
-- Name: goods goods_goodsname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goods
    ADD CONSTRAINT goods_goodsname_key UNIQUE (goodsname);


--
-- Name: goods goods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goods
    ADD CONSTRAINT goods_pkey PRIMARY KEY (goods_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: belong_to_order belong_to_order_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belong_to_order
    ADD CONSTRAINT belong_to_order_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: carts carts_goods_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_goods_id_fkey FOREIGN KEY (goods_id) REFERENCES public.goods(goods_id) ON DELETE CASCADE;


--
-- Name: carts carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

