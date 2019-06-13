--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.17
-- Dumped by pg_dump version 11.3 (Ubuntu 11.3-1.pgdg18.04+1)

-- Started on 2019-06-13 10:08:06 CEST

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
-- TOC entry 3639 (class 0 OID 260325)
-- Dependencies: 219
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roles VALUES (1, 'EDIT', '{}');
INSERT INTO public.roles VALUES (2, 'CONTROL', '{}');
INSERT INTO public.roles VALUES (3, 'VALID', '{}');
INSERT INTO public.roles VALUES (4, 'PUBLIC', '{}');
INSERT INTO public.roles VALUES (0, 'VIEW', '{}');


--
-- TOC entry 3645 (class 0 OID 0)
-- Dependencies: 218
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 1, false);


-- Completed on 2019-06-13 10:08:06 CEST

--
-- PostgreSQL database dump complete
--

