--
-- PostgreSQL database dump
--

\restrict bRG3eoL5E4mky2uUAd48zeRgS4RouTJ9BwvTbd2cRH1O84A9NdXELCKBPRPlqwk

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

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
-- Name: cards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cards (
    id integer NOT NULL,
    subassembly_id integer,
    name text NOT NULL
);


ALTER TABLE public.cards OWNER TO postgres;

--
-- Name: cards_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cards_id_seq OWNER TO postgres;

--
-- Name: cards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cards_id_seq OWNED BY public.cards.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    level text NOT NULL,
    level_id integer NOT NULL,
    file_path text NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: faults; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.faults (
    id integer NOT NULL,
    level text NOT NULL,
    level_id integer NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.faults OWNER TO postgres;

--
-- Name: faults_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.faults_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.faults_id_seq OWNER TO postgres;

--
-- Name: faults_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.faults_id_seq OWNED BY public.faults.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: steps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.steps (
    id integer NOT NULL,
    fault_id integer,
    step_number integer NOT NULL,
    step text NOT NULL,
    explanation text
);


ALTER TABLE public.steps OWNER TO postgres;

--
-- Name: steps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.steps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.steps_id_seq OWNER TO postgres;

--
-- Name: steps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.steps_id_seq OWNED BY public.steps.id;


--
-- Name: subassemblies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subassemblies (
    id integer NOT NULL,
    system_id integer,
    name text NOT NULL
);


ALTER TABLE public.subassemblies OWNER TO postgres;

--
-- Name: subassemblies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subassemblies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subassemblies_id_seq OWNER TO postgres;

--
-- Name: subassemblies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subassemblies_id_seq OWNED BY public.subassemblies.id;


--
-- Name: systems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.systems (
    id integer NOT NULL,
    project_id integer,
    name text NOT NULL
);


ALTER TABLE public.systems OWNER TO postgres;

--
-- Name: systems_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.systems_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.systems_id_seq OWNER TO postgres;

--
-- Name: systems_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.systems_id_seq OWNED BY public.systems.id;


--
-- Name: cards id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards ALTER COLUMN id SET DEFAULT nextval('public.cards_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: faults id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faults ALTER COLUMN id SET DEFAULT nextval('public.faults_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: steps id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps ALTER COLUMN id SET DEFAULT nextval('public.steps_id_seq'::regclass);


--
-- Name: subassemblies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subassemblies ALTER COLUMN id SET DEFAULT nextval('public.subassemblies_id_seq'::regclass);


--
-- Name: systems id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systems ALTER COLUMN id SET DEFAULT nextval('public.systems_id_seq'::regclass);


--
-- Data for Name: cards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cards (id, subassembly_id, name) FROM stdin;
1	1	Card A1-1-1
2	1	Card A1-1-2
3	2	Card A1-2-1
4	3	Card A2-1-1
5	4	Card B1-1-1
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (id, level, level_id, file_path) FROM stdin;
1	project	1	resources/docs/project_alpha_manual.pdf
2	system	1	resources/docs/system_A1_specs.pdf
3	card	1	resources/docs/card_A1-1-1_diagram.pdf
\.


--
-- Data for Name: faults; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.faults (id, level, level_id, description) FROM stdin;
1	project	1	Project Alpha general fault
2	system	1	System A1 fault example
3	subassembly	1	Subassembly A1-1 minor fault
4	card	1	Card A1-1-1 critical fault
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, name) FROM stdin;
1	Project Alpha
2	Project Beta
\.


--
-- Data for Name: steps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.steps (id, fault_id, step_number, step, explanation) FROM stdin;
1	1	1	Check power supply	Verify that the main power is on
2	1	2	Restart system	Restart the system after power check
3	2	1	Inspect connectors	Ensure connectors are plugged in correctly
4	4	1	Replace card	Replace the card if faulty
\.


--
-- Data for Name: subassemblies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subassemblies (id, system_id, name) FROM stdin;
1	1	Subassembly A1-1
2	1	Subassembly A1-2
3	2	Subassembly A2-1
4	3	Subassembly B1-1
\.


--
-- Data for Name: systems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.systems (id, project_id, name) FROM stdin;
1	1	System A1
2	1	System A2
3	2	System B1
\.


--
-- Name: cards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cards_id_seq', 5, true);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 3, true);


--
-- Name: faults_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.faults_id_seq', 4, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 2, true);


--
-- Name: steps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.steps_id_seq', 4, true);


--
-- Name: subassemblies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subassemblies_id_seq', 4, true);


--
-- Name: systems_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.systems_id_seq', 3, true);


--
-- Name: cards cards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: faults faults_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faults
    ADD CONSTRAINT faults_pkey PRIMARY KEY (id);


--
-- Name: projects projects_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_name_key UNIQUE (name);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: steps steps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_pkey PRIMARY KEY (id);


--
-- Name: subassemblies subassemblies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subassemblies
    ADD CONSTRAINT subassemblies_pkey PRIMARY KEY (id);


--
-- Name: systems systems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systems
    ADD CONSTRAINT systems_pkey PRIMARY KEY (id);


--
-- Name: cards cards_subassembly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_subassembly_id_fkey FOREIGN KEY (subassembly_id) REFERENCES public.subassemblies(id);


--
-- Name: steps steps_fault_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_fault_id_fkey FOREIGN KEY (fault_id) REFERENCES public.faults(id);


--
-- Name: subassemblies subassemblies_system_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subassemblies
    ADD CONSTRAINT subassemblies_system_id_fkey FOREIGN KEY (system_id) REFERENCES public.systems(id);


--
-- Name: systems systems_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systems
    ADD CONSTRAINT systems_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- PostgreSQL database dump complete
--

\unrestrict bRG3eoL5E4mky2uUAd48zeRgS4RouTJ9BwvTbd2cRH1O84A9NdXELCKBPRPlqwk

