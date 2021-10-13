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
    product_size character varying(20),
    price character varying(10),
    "price_GBP" character varying(10),
    "price_USD" numeric,
    category_id integer,
    product_type character varying(20),
    ingredients text,
    clean_ingreds text,
    rec_combination boolean NOT NULL,
    rec_dry boolean NOT NULL,
    rec_normal boolean NOT NULL,
    rec_oily boolean NOT NULL,
    rec_sensitive boolean NOT NULL,
    fragrance_free boolean,
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
1	Moisturizer		2021-10-10 03:59:15.144415+00
2	Serum		2021-10-10 03:59:15.162688+00
3	Oil		2021-10-10 03:59:15.172278+00
4	Mist		2021-10-10 03:59:15.178987+00
5	Mask		2021-10-10 03:59:15.186462+00
6	Balm		2021-10-10 03:59:15.192824+00
7	Peel		2021-10-10 03:59:15.200868+00
8	Eye Care		2021-10-10 03:59:15.207385+00
9	Cleanser		2021-10-10 03:59:15.21141+00
10	Toner		2021-10-10 03:59:15.216812+00
11	Exfoliator		2021-10-10 03:59:15.221864+00
12	Bath Salts		2021-10-10 03:59:15.225952+00
13	Body Wash		2021-10-10 03:59:15.231297+00
14	Bath Oil		2021-10-10 03:59:15.237464+00
15	Sun Protection		2021-10-10 03:59:15.243686+00
16	Essence		2021-10-10 03:59:15.252463+00
\.


--
-- Data for Name: concerns; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.concerns (concern_id, concern_name, description, created_at) FROM stdin;
1	acne		2021-10-10 03:59:15.116111+00
2	aging	Signs of aging include fine lines and wrinkles, dark spots, rough skin texture, and uneven complexion. The best prevention is to limit sun exposure throughout your life and protect your skin with sunscreen.	2021-10-10 03:59:15.120873+00
3	inflammation and redness	Common signs include redness and puffiness, rough skin texture, and stinging sensations.	2021-10-10 03:59:15.124576+00
4	dullness	Lackluster, unhealthy complexion. This can occur for many reasons, but the two most common ones are a buildup of dead skin cells, and a lack of oxygen supply in the skin.	2021-10-10 03:59:15.129544+00
5	large pores	Skin with large pores are normally caused by genetic factors and cannot shrink. However, certain products may help reduce the appearance of their size by clearing up oil within the pores.	2021-10-10 03:59:15.13588+00
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.ingredients (ingredient_id, common_name, alternative_name, active_type, pm_only, irritation_rating, endocrine_disruption, carcinogenic, pregnancy_safe, reef_safe, has_fragrance, created_at) FROM stdin;
1	squalene	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.345258+00
2	behenyl alcohol	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.345258+00
3	capric triglyceride	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.345258+00
4	glycerin	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.345258+00
5	sodium acrylates/c10-30 alkyl	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.345258+00
6	prunus amygdalus dulcis	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
7	sesamium indicum seed oil	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
8	alcohol	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
9	glyceryl oleate	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
10	calendula officinalis extract	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
11	sodium cera alba	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
12	xanthan gum	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
13	parfum	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
14	limonene	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
15	linalool	\N	\N	f	\N	f	f	f	f	f	2021-10-10 03:59:15.47544+00
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
1	1	\N	1	2021-10-10 03:59:15.345258+00
2	1	\N	2	2021-10-10 03:59:15.345258+00
3	1	\N	3	2021-10-10 03:59:15.345258+00
4	1	\N	4	2021-10-10 03:59:15.345258+00
5	1	\N	5	2021-10-10 03:59:15.345258+00
6	2	\N	1	2021-10-10 03:59:15.47544+00
7	2	\N	2	2021-10-10 03:59:15.47544+00
8	2	\N	3	2021-10-10 03:59:15.47544+00
9	2	4	4	2021-10-10 03:59:15.47544+00
10	2	\N	5	2021-10-10 03:59:15.47544+00
11	2	\N	6	2021-10-10 03:59:15.47544+00
12	2	\N	7	2021-10-10 03:59:15.47544+00
13	2	\N	8	2021-10-10 03:59:15.47544+00
14	2	\N	9	2021-10-10 03:59:15.47544+00
15	2	\N	10	2021-10-10 03:59:15.47544+00
16	2	\N	11	2021-10-10 03:59:15.47544+00
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.products (product_id, product_name, brand_name, product_url, product_size, price, "price_GBP", "price_USD", category_id, product_type, ingredients, clean_ingreds, rec_combination, rec_dry, rec_normal, rec_oily, rec_sensitive, fragrance_free, created_at) FROM stdin;
1	Avène Tolérance Extrême Emulsion 50ml	\N	https://www.lookfantastic.com/avene-tolerance-extreme-emulsion-50ml/11571253.html	\N	£11.25	\N	\N	1	\N	\N	\N	f	f	f	f	f	f	2021-10-10 03:59:15.345258+00
2	Weleda Baby Calendula Cream Bath (200ml)	\N	https://www.lookfantastic.com/weleda-baby-calendula-cream-bath-200ml/10810409.html	\N	£13.95	\N	\N	14	\N	\N	\N	f	f	f	f	f	f	2021-10-10 03:59:15.47544+00
\.


--
-- Data for Name: skincare_steps; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.skincare_steps (step_id, step_name, description, created_at) FROM stdin;
1	Cleanse	Gently wash your face.	2021-10-10 03:59:15.262926+00
2	Apply toner	Gently apply a toner using a cotton pad or with your hands.	2021-10-10 03:59:15.270302+00
3	Apply serum/essence	Place a few drops of the product in your hand to warm it up before applying to your face. Swipe gently.	2021-10-10 03:59:15.275979+00
4	Moisturize	After waiting to dry, add a moisturizer!	2021-10-10 03:59:15.284254+00
5	Apply sunscreen	Apply sunblock, using at least 1/4 to 1/2 teaspoon of product for your entire face. Don't forget your ears!	2021-10-10 03:59:15.291427+00
\.


--
-- Data for Name: skintypes; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.skintypes (skintype_id, skintype_name, description, created_at) FROM stdin;
1	combination	(Type 1) If the “wash your face and leave it for two hours” test gives you different results in January than it does in July, you’re probably a seasonal combo type. (Type 2) If you get oily in some places and tight in others, you probably have a combination of skin types on your face.	2021-10-10 03:59:15.303061+00
2	dry	Dry skin often feels tight, flaky, or itchy. If you wash your face and don’t apply any products, after a couple of hours your skin will feel dry or tight instead of oily.	2021-10-10 03:59:15.311421+00
3	normal	Your skin rarely feels either tight or greasy. Your skin doesn’t flake off, nor does it get shiny by the end of the day.	2021-10-10 03:59:15.317207+00
4	oily	If you wash your face and don’t put on any products, your skin will feel oily and shiny within a couple of hours. (Note: in many cases, people assume they have an oily skin type when they actually have a dehydrated skin condition, and their oiliness can actually be treated and managed.)	2021-10-10 03:59:15.323058+00
5	sensitive	There are two types of sensitivity: irritation (which usually manifests as redness, stinging, small painless bumps, or discomfort to touch) and allergy (which manifests as swelling, itching, or rashes). If you get either of those responses frequently, or if products that most people can use without issue cause an irritation or allergy response in your skin, you may have sensitive skin.	2021-10-10 03:59:15.32902+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.users (user_id, f_name, l_name, email, hashed_password, skintype_id, primary_concern_id, secondary_concern_id, created_at) FROM stdin;
1			bob@bob.com	sha256$YMeiqwEYSuhWrZ4Z$f677e3b151cb6ba9dd87fcf228882985d0b6af516c2bd4570a7dd53d00448643	1	\N	\N	2021-10-10 04:42:09.733907+00
2	Patrick	Star	pstar@gmail.com	sha256$nnbBuku0lxV9VHaG$f1be21e87f7cfb3693d01ab3c6ee865c493b19c7ca2456763ddca830df3680e0	1	\N	\N	2021-10-12 01:32:41.544802+00
3	Squidward	Tentacles	s.tentacles@yahoo.com	sha256$29LpQFAmlxn6dEbv$ee36f490cd7c4853f19e050997a6c1fe13690b758f652883c4e9bf68493920a4	1	\N	\N	2021-10-12 07:40:03.36257+00
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

SELECT pg_catalog.setval('public.ingredients_ingredient_id_seq', 15, true);


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

SELECT pg_catalog.setval('public.product_ingredients_prod_ing_id_seq', 16, true);


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

SELECT pg_catalog.setval('public.users_user_id_seq', 3, true);


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

