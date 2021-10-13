--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Ubuntu 13.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.4 (Ubuntu 13.4-1.pgdg20.04+1)

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
-- Name: am_routines; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.am_routines (
    routine_id integer NOT NULL,
    user_id integer NOT NULL,
    step_id integer NOT NULL,
    product_id integer,
    status boolean,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.am_routines OWNER TO hackbright;

--
-- Name: am_routines_routine_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.am_routines_routine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.am_routines_routine_id_seq OWNER TO hackbright;

--
-- Name: am_routines_routine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.am_routines_routine_id_seq OWNED BY public.am_routines.routine_id;


--
-- Name: cabinets; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.cabinets (
    cabinet_id integer NOT NULL,
    user_id integer NOT NULL,
    product_id integer,
    status boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cabinets OWNER TO hackbright;

--
-- Name: cabinets_cabinet_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.cabinets_cabinet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cabinets_cabinet_id_seq OWNER TO hackbright;

--
-- Name: cabinets_cabinet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.cabinets_cabinet_id_seq OWNED BY public.cabinets.cabinet_id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(25) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.categories OWNER TO hackbright;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_category_id_seq OWNER TO hackbright;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: concerns; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.concerns (
    concern_id integer NOT NULL,
    concern_name character varying(100) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.concerns OWNER TO hackbright;

--
-- Name: concerns_concern_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.concerns_concern_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.concerns_concern_id_seq OWNER TO hackbright;

--
-- Name: concerns_concern_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.concerns_concern_id_seq OWNED BY public.concerns.concern_id;


--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.ingredients (
    ingredient_id integer NOT NULL,
    common_name character varying(50) NOT NULL,
    alternative_name character varying(50),
    active_type character varying(25),
    pm_only boolean,
    irritation_rating integer,
    endocrine_disruption boolean,
    carcinogenic boolean,
    pregnancy_safe boolean,
    reef_safe boolean,
    has_fragrance boolean,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.ingredients OWNER TO hackbright;

--
-- Name: ingredients_ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.ingredients_ingredient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredients_ingredient_id_seq OWNER TO hackbright;

--
-- Name: ingredients_ingredient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.ingredients_ingredient_id_seq OWNED BY public.ingredients.ingredient_id;


--
-- Name: interactions; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.interactions (
    interaction_id integer NOT NULL,
    first_ingredient_id integer,
    second_ingredient_id integer,
    reaction_description text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.interactions OWNER TO hackbright;

--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.interactions_interaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.interactions_interaction_id_seq OWNER TO hackbright;

--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.interactions_interaction_id_seq OWNED BY public.interactions.interaction_id;


--
-- Name: pm_routines; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.pm_routines (
    routine_id integer NOT NULL,
    user_id integer NOT NULL,
    step_id integer NOT NULL,
    product_id integer,
    status boolean,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.pm_routines OWNER TO hackbright;

--
-- Name: pm_routines_routine_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.pm_routines_routine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pm_routines_routine_id_seq OWNER TO hackbright;

--
-- Name: pm_routines_routine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.pm_routines_routine_id_seq OWNED BY public.pm_routines.routine_id;


--
-- Name: product_ingredients; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.product_ingredients (
    prod_ing_id integer NOT NULL,
    product_id integer,
    ingredient_id integer,
    abundance_order integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.product_ingredients OWNER TO hackbright;

--
-- Name: product_ingredients_prod_ing_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.product_ingredients_prod_ing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_ingredients_prod_ing_id_seq OWNER TO hackbright;

--
-- Name: product_ingredients_prod_ing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.product_ingredients_prod_ing_id_seq OWNED BY public.product_ingredients.prod_ing_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(100) NOT NULL,
    brand_name character varying(25),
    product_url character varying(100),
    category_id integer,
    product_type character varying(20),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.products OWNER TO hackbright;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_product_id_seq OWNER TO hackbright;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- Name: skincare_steps; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.skincare_steps (
    step_id integer NOT NULL,
    step_name character varying(25) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.skincare_steps OWNER TO hackbright;

--
-- Name: skincare_steps_step_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.skincare_steps_step_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skincare_steps_step_id_seq OWNER TO hackbright;

--
-- Name: skincare_steps_step_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.skincare_steps_step_id_seq OWNED BY public.skincare_steps.step_id;


--
-- Name: skintypes; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.skintypes (
    skintype_id integer NOT NULL,
    skintype_name character varying(25) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.skintypes OWNER TO hackbright;

--
-- Name: skintypes_skintype_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.skintypes_skintype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skintypes_skintype_id_seq OWNER TO hackbright;

--
-- Name: skintypes_skintype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.skintypes_skintype_id_seq OWNED BY public.skintypes.skintype_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    f_name character varying(25),
    l_name character varying(25),
    email character varying(50) NOT NULL,
    hashed_password character varying(200) NOT NULL,
    skintype_id integer,
    primary_concern_id integer,
    secondary_concern_id integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO hackbright;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: am_routines routine_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.am_routines ALTER COLUMN routine_id SET DEFAULT nextval('public.am_routines_routine_id_seq'::regclass);


--
-- Name: cabinets cabinet_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.cabinets ALTER COLUMN cabinet_id SET DEFAULT nextval('public.cabinets_cabinet_id_seq'::regclass);


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: concerns concern_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.concerns ALTER COLUMN concern_id SET DEFAULT nextval('public.concerns_concern_id_seq'::regclass);


--
-- Name: ingredients ingredient_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN ingredient_id SET DEFAULT nextval('public.ingredients_ingredient_id_seq'::regclass);


--
-- Name: interactions interaction_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.interactions ALTER COLUMN interaction_id SET DEFAULT nextval('public.interactions_interaction_id_seq'::regclass);


--
-- Name: pm_routines routine_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.pm_routines ALTER COLUMN routine_id SET DEFAULT nextval('public.pm_routines_routine_id_seq'::regclass);


--
-- Name: product_ingredients prod_ing_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.product_ingredients ALTER COLUMN prod_ing_id SET DEFAULT nextval('public.product_ingredients_prod_ing_id_seq'::regclass);


--
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- Name: skincare_steps step_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.skincare_steps ALTER COLUMN step_id SET DEFAULT nextval('public.skincare_steps_step_id_seq'::regclass);


--
-- Name: skintypes skintype_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.skintypes ALTER COLUMN skintype_id SET DEFAULT nextval('public.skintypes_skintype_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: am_routines; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.am_routines (routine_id, user_id, step_id, product_id, status, created_at) FROM stdin;
\.


--
-- Data for Name: cabinets; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.cabinets (cabinet_id, user_id, product_id, status, created_at) FROM stdin;
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.categories (category_id, category_name, description, created_at) FROM stdin;
\.


--
-- Data for Name: concerns; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.concerns (concern_id, concern_name, description, created_at) FROM stdin;
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.ingredients (ingredient_id, common_name, alternative_name, active_type, pm_only, irritation_rating, endocrine_disruption, carcinogenic, pregnancy_safe, reef_safe, has_fragrance, created_at) FROM stdin;
1	ingred_1	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.751253+00
2	ingred_2	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.751253+00
3	ingred_3	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.751253+00
4	ingred1	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.796635+00
5	ingred2	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.796635+00
6	ingred3	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.796635+00
7	ingred4	\N	\N	f	\N	f	f	f	f	f	2021-10-12 23:03:40.796635+00
\.


--
-- Data for Name: interactions; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.interactions (interaction_id, first_ingredient_id, second_ingredient_id, reaction_description, created_at) FROM stdin;
\.


--
-- Data for Name: pm_routines; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.pm_routines (routine_id, user_id, step_id, product_id, status, created_at) FROM stdin;
\.


--
-- Data for Name: product_ingredients; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.product_ingredients (prod_ing_id, product_id, ingredient_id, abundance_order, created_at) FROM stdin;
1	1	\N	1	2021-10-12 23:03:40.751253+00
2	1	\N	2	2021-10-12 23:03:40.751253+00
3	1	\N	3	2021-10-12 23:03:40.751253+00
4	2	4	1	2021-10-12 23:03:40.796635+00
5	2	5	2	2021-10-12 23:03:40.796635+00
6	2	6	3	2021-10-12 23:03:40.796635+00
7	2	7	4	2021-10-12 23:03:40.796635+00
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.products (product_id, product_name, brand_name, product_url, category_id, product_type, created_at) FROM stdin;
1	Generic Lotion	\N	\N	\N	\N	2021-10-12 23:03:40.751253+00
2	Facial Lotion	Aveeno	\N	\N	Moisturizer	2021-10-12 23:03:40.796635+00
\.


--
-- Data for Name: skincare_steps; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.skincare_steps (step_id, step_name, description, created_at) FROM stdin;
\.


--
-- Data for Name: skintypes; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.skintypes (skintype_id, skintype_name, description, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.users (user_id, f_name, l_name, email, hashed_password, skintype_id, primary_concern_id, secondary_concern_id, created_at) FROM stdin;
\.


--
-- Name: am_routines_routine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.am_routines_routine_id_seq', 1, false);


--
-- Name: cabinets_cabinet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.cabinets_cabinet_id_seq', 1, false);


--
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.categories_category_id_seq', 1, false);


--
-- Name: concerns_concern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.concerns_concern_id_seq', 1, false);


--
-- Name: ingredients_ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.ingredients_ingredient_id_seq', 7, true);


--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.interactions_interaction_id_seq', 1, false);


--
-- Name: pm_routines_routine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.pm_routines_routine_id_seq', 1, false);


--
-- Name: product_ingredients_prod_ing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.product_ingredients_prod_ing_id_seq', 7, true);


--
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.products_product_id_seq', 2, true);


--
-- Name: skincare_steps_step_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.skincare_steps_step_id_seq', 1, false);


--
-- Name: skintypes_skintype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.skintypes_skintype_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: am_routines am_routines_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.am_routines
    ADD CONSTRAINT am_routines_pkey PRIMARY KEY (routine_id);


--
-- Name: cabinets cabinets_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_pkey PRIMARY KEY (cabinet_id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: concerns concerns_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.concerns
    ADD CONSTRAINT concerns_pkey PRIMARY KEY (concern_id);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (ingredient_id);


--
-- Name: interactions interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.interactions
    ADD CONSTRAINT interactions_pkey PRIMARY KEY (interaction_id);


--
-- Name: pm_routines pm_routines_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.pm_routines
    ADD CONSTRAINT pm_routines_pkey PRIMARY KEY (routine_id);


--
-- Name: product_ingredients product_ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.product_ingredients
    ADD CONSTRAINT product_ingredients_pkey PRIMARY KEY (prod_ing_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: skincare_steps skincare_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.skincare_steps
    ADD CONSTRAINT skincare_steps_pkey PRIMARY KEY (step_id);


--
-- Name: skintypes skintypes_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.skintypes
    ADD CONSTRAINT skintypes_pkey PRIMARY KEY (skintype_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: am_routines am_routines_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.am_routines
    ADD CONSTRAINT am_routines_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: am_routines am_routines_step_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.am_routines
    ADD CONSTRAINT am_routines_step_id_fkey FOREIGN KEY (step_id) REFERENCES public.skincare_steps(step_id);


--
-- Name: am_routines am_routines_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.am_routines
    ADD CONSTRAINT am_routines_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: cabinets cabinets_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: cabinets cabinets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: interactions interactions_first_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.interactions
    ADD CONSTRAINT interactions_first_ingredient_id_fkey FOREIGN KEY (first_ingredient_id) REFERENCES public.ingredients(ingredient_id);


--
-- Name: interactions interactions_second_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.interactions
    ADD CONSTRAINT interactions_second_ingredient_id_fkey FOREIGN KEY (second_ingredient_id) REFERENCES public.ingredients(ingredient_id);


--
-- Name: pm_routines pm_routines_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.pm_routines
    ADD CONSTRAINT pm_routines_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: pm_routines pm_routines_step_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.pm_routines
    ADD CONSTRAINT pm_routines_step_id_fkey FOREIGN KEY (step_id) REFERENCES public.skincare_steps(step_id);


--
-- Name: pm_routines pm_routines_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.pm_routines
    ADD CONSTRAINT pm_routines_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: product_ingredients product_ingredients_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.product_ingredients
    ADD CONSTRAINT product_ingredients_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(ingredient_id);


--
-- Name: product_ingredients product_ingredients_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.product_ingredients
    ADD CONSTRAINT product_ingredients_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: users users_primary_concern_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_primary_concern_id_fkey FOREIGN KEY (primary_concern_id) REFERENCES public.concerns(concern_id);


--
-- Name: users users_secondary_concern_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_secondary_concern_id_fkey FOREIGN KEY (secondary_concern_id) REFERENCES public.concerns(concern_id);


--
-- Name: users users_skintype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_skintype_id_fkey FOREIGN KEY (skintype_id) REFERENCES public.skintypes(skintype_id);


--
-- PostgreSQL database dump complete
--

