--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

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
-- Name: station; Type: SCHEMA; Schema: -; Owner: station_user
--

CREATE SCHEMA station;


ALTER SCHEMA station OWNER TO station_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: station_user
--

CREATE TABLE public.items (
    item_id integer NOT NULL,
    station_id integer,
    name character varying(100),
    item_index integer,
    status character varying(100)
);


ALTER TABLE public.items OWNER TO station_user;

--
-- Name: items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: station_user
--

CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.items_item_id_seq OWNER TO station_user;

--
-- Name: items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: station_user
--

ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;


--
-- Name: station; Type: TABLE; Schema: public; Owner: station_user
--

CREATE TABLE public.station (
    station_id integer NOT NULL,
    current_x integer,
    current_y integer,
    energy integer
);


ALTER TABLE public.station OWNER TO station_user;

--
-- Name: station_station_id_seq; Type: SEQUENCE; Schema: public; Owner: station_user
--

CREATE SEQUENCE public.station_station_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_station_id_seq OWNER TO station_user;

--
-- Name: station_station_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: station_user
--

ALTER SEQUENCE public.station_station_id_seq OWNED BY public.station.station_id;


--
-- Name: items item_id; Type: DEFAULT; Schema: public; Owner: station_user
--

ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);


--
-- Name: station station_id; Type: DEFAULT; Schema: public; Owner: station_user
--

ALTER TABLE ONLY public.station ALTER COLUMN station_id SET DEFAULT nextval('public.station_station_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: station_user
--

COPY public.items (item_id, station_id, name, item_index, status) FROM stdin;
\.


--
-- Data for Name: station; Type: TABLE DATA; Schema: public; Owner: station_user
--

COPY public.station (station_id, current_x, current_y, energy) FROM stdin;
\.


--
-- Name: items_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: station_user
--

SELECT pg_catalog.setval('public.items_item_id_seq', 1, false);


--
-- Name: station_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: station_user
--

SELECT pg_catalog.setval('public.station_station_id_seq', 1, false);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: station_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);


--
-- Name: station station_pkey; Type: CONSTRAINT; Schema: public; Owner: station_user
--

ALTER TABLE ONLY public.station
    ADD CONSTRAINT station_pkey PRIMARY KEY (station_id);


--
-- Name: items fk_station; Type: FK CONSTRAINT; Schema: public; Owner: station_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES public.station(station_id);


--
-- PostgreSQL database dump complete
--

