--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

-- Started on 2019-03-17 15:13:19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE crawldb;
--
-- TOC entry 2891 (class 1262 OID 16620)
-- Name: crawldb; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE crawldb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Slovenian_Slovenia.1250' LC_CTYPE = 'Slovenian_Slovenia.1250';


ALTER DATABASE crawldb OWNER TO postgres;

\connect crawldb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16621)
-- Name: crawldb; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA crawldb;


ALTER SCHEMA crawldb OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 16622)
-- Name: data_type; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.data_type (
    code character varying(20) NOT NULL
);


ALTER TABLE crawldb.data_type OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16625)
-- Name: image; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.image (
    id integer NOT NULL,
    page_id integer,
    filename character varying(255),
    content_type character varying(50),
    data bytea,
    accessed_time timestamp without time zone
);


ALTER TABLE crawldb.image OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 16631)
-- Name: image_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.image_id_seq OWNER TO postgres;

--
-- TOC entry 2892 (class 0 OID 0)
-- Dependencies: 199
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.image_id_seq OWNED BY crawldb.image.id;


--
-- TOC entry 200 (class 1259 OID 16633)
-- Name: link; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.link (
    from_page integer NOT NULL,
    to_page integer NOT NULL
);


ALTER TABLE crawldb.link OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16636)
-- Name: page; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page (
    id integer NOT NULL,
    site_id integer,
    page_type_code character varying(20),
    url character varying(3000),
    html_content text,
    http_status_code integer,
    accessed_time timestamp without time zone,
    hash character varying(255),
    canon_url character varying(200)
);


ALTER TABLE crawldb.page OWNER TO postgres;

--
-- TOC entry 2893 (class 0 OID 0)
-- Dependencies: 201
-- Name: COLUMN page.hash; Type: COMMENT; Schema: crawldb; Owner: postgres
--

COMMENT ON COLUMN crawldb.page.hash IS 'HTML content hash';


--
-- TOC entry 202 (class 1259 OID 16642)
-- Name: page_data; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page_data (
    id integer NOT NULL,
    page_id integer,
    data_type_code character varying(20),
    data bytea
);


ALTER TABLE crawldb.page_data OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16648)
-- Name: page_data_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.page_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.page_data_id_seq OWNER TO postgres;

--
-- TOC entry 2894 (class 0 OID 0)
-- Dependencies: 203
-- Name: page_data_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.page_data_id_seq OWNED BY crawldb.page_data.id;


--
-- TOC entry 204 (class 1259 OID 16650)
-- Name: page_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.page_id_seq OWNER TO postgres;

--
-- TOC entry 2895 (class 0 OID 0)
-- Dependencies: 204
-- Name: page_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.page_id_seq OWNED BY crawldb.page.id;


--
-- TOC entry 205 (class 1259 OID 16652)
-- Name: page_type; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.page_type (
    code character varying(20) NOT NULL
);


ALTER TABLE crawldb.page_type OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16655)
-- Name: site; Type: TABLE; Schema: crawldb; Owner: postgres
--

CREATE TABLE crawldb.site (
    id integer NOT NULL,
    domain character varying(500),
    robots_content text,
    sitemap_content text
);


ALTER TABLE crawldb.site OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16661)
-- Name: site_id_seq; Type: SEQUENCE; Schema: crawldb; Owner: postgres
--

CREATE SEQUENCE crawldb.site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crawldb.site_id_seq OWNER TO postgres;

--
-- TOC entry 2896 (class 0 OID 0)
-- Dependencies: 207
-- Name: site_id_seq; Type: SEQUENCE OWNED BY; Schema: crawldb; Owner: postgres
--

ALTER SEQUENCE crawldb.site_id_seq OWNED BY crawldb.site.id;


--
-- TOC entry 2720 (class 2604 OID 16663)
-- Name: image id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image ALTER COLUMN id SET DEFAULT nextval('crawldb.image_id_seq'::regclass);


--
-- TOC entry 2721 (class 2604 OID 16664)
-- Name: page id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page ALTER COLUMN id SET DEFAULT nextval('crawldb.page_id_seq'::regclass);


--
-- TOC entry 2722 (class 2604 OID 16665)
-- Name: page_data id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data ALTER COLUMN id SET DEFAULT nextval('crawldb.page_data_id_seq'::regclass);


--
-- TOC entry 2723 (class 2604 OID 16666)
-- Name: site id; Type: DEFAULT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.site ALTER COLUMN id SET DEFAULT nextval('crawldb.site_id_seq'::regclass);


--
-- TOC entry 2875 (class 0 OID 16622)
-- Dependencies: 197
-- Data for Name: data_type; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

INSERT INTO crawldb.data_type (code) VALUES ('PDF');
INSERT INTO crawldb.data_type (code) VALUES ('DOC');
INSERT INTO crawldb.data_type (code) VALUES ('DOCX');
INSERT INTO crawldb.data_type (code) VALUES ('PPT');
INSERT INTO crawldb.data_type (code) VALUES ('PPTX');
INSERT INTO crawldb.data_type (code) VALUES ('asd');


--
-- TOC entry 2876 (class 0 OID 16625)
-- Dependencies: 198
-- Data for Name: image; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--



--
-- TOC entry 2878 (class 0 OID 16633)
-- Dependencies: 200
-- Data for Name: link; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--



--
-- TOC entry 2879 (class 0 OID 16636)
-- Dependencies: 201
-- Data for Name: page; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--



--
-- TOC entry 2880 (class 0 OID 16642)
-- Dependencies: 202
-- Data for Name: page_data; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--



--
-- TOC entry 2883 (class 0 OID 16652)
-- Dependencies: 205
-- Data for Name: page_type; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--

INSERT INTO crawldb.page_type (code) VALUES ('HTML');
INSERT INTO crawldb.page_type (code) VALUES ('BINARY');
INSERT INTO crawldb.page_type (code) VALUES ('DUPLICATE');
INSERT INTO crawldb.page_type (code) VALUES ('FRONTIER');


--
-- TOC entry 2884 (class 0 OID 16655)
-- Dependencies: 206
-- Data for Name: site; Type: TABLE DATA; Schema: crawldb; Owner: postgres
--



--
-- TOC entry 2897 (class 0 OID 0)
-- Dependencies: 199
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.image_id_seq', 4, true);


--
-- TOC entry 2898 (class 0 OID 0)
-- Dependencies: 203
-- Name: page_data_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.page_data_id_seq', 1, false);


--
-- TOC entry 2899 (class 0 OID 0)
-- Dependencies: 204
-- Name: page_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.page_id_seq', 99, true);


--
-- TOC entry 2900 (class 0 OID 0)
-- Dependencies: 207
-- Name: site_id_seq; Type: SEQUENCE SET; Schema: crawldb; Owner: postgres
--

SELECT pg_catalog.setval('crawldb.site_id_seq', 11, true);


--
-- TOC entry 2730 (class 2606 OID 16668)
-- Name: link _0; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT _0 PRIMARY KEY (from_page, to_page);


--
-- TOC entry 2725 (class 2606 OID 16670)
-- Name: data_type pk_data_type_code; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.data_type
    ADD CONSTRAINT pk_data_type_code PRIMARY KEY (code);


--
-- TOC entry 2728 (class 2606 OID 16672)
-- Name: image pk_image_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image
    ADD CONSTRAINT pk_image_id PRIMARY KEY (id);


--
-- TOC entry 2742 (class 2606 OID 16674)
-- Name: page_data pk_page_data_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT pk_page_data_id PRIMARY KEY (id);


--
-- TOC entry 2736 (class 2606 OID 16676)
-- Name: page pk_page_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT pk_page_id PRIMARY KEY (id);


--
-- TOC entry 2744 (class 2606 OID 16678)
-- Name: page_type pk_page_type_code; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_type
    ADD CONSTRAINT pk_page_type_code PRIMARY KEY (code);


--
-- TOC entry 2746 (class 2606 OID 16680)
-- Name: site pk_site_id; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.site
    ADD CONSTRAINT pk_site_id PRIMARY KEY (id);


--
-- TOC entry 2738 (class 2606 OID 16682)
-- Name: page unq_url_idx; Type: CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT unq_url_idx UNIQUE (url);


--
-- TOC entry 2726 (class 1259 OID 16683)
-- Name: idx_image_page_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_image_page_id ON crawldb.image USING btree (page_id);


--
-- TOC entry 2731 (class 1259 OID 16684)
-- Name: idx_link_from_page; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_link_from_page ON crawldb.link USING btree (from_page);


--
-- TOC entry 2732 (class 1259 OID 16685)
-- Name: idx_link_to_page; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_link_to_page ON crawldb.link USING btree (to_page);


--
-- TOC entry 2739 (class 1259 OID 16686)
-- Name: idx_page_data_data_type_code; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_data_data_type_code ON crawldb.page_data USING btree (data_type_code);


--
-- TOC entry 2740 (class 1259 OID 16687)
-- Name: idx_page_data_page_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_data_page_id ON crawldb.page_data USING btree (page_id);


--
-- TOC entry 2733 (class 1259 OID 16688)
-- Name: idx_page_page_type_code; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_page_type_code ON crawldb.page USING btree (page_type_code);


--
-- TOC entry 2734 (class 1259 OID 16689)
-- Name: idx_page_site_id; Type: INDEX; Schema: crawldb; Owner: postgres
--

CREATE INDEX idx_page_site_id ON crawldb.page USING btree (site_id);


--
-- TOC entry 2747 (class 2606 OID 16690)
-- Name: image fk_image_page_data; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.image
    ADD CONSTRAINT fk_image_page_data FOREIGN KEY (page_id) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- TOC entry 2748 (class 2606 OID 16695)
-- Name: link fk_link_page; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT fk_link_page FOREIGN KEY (from_page) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- TOC entry 2749 (class 2606 OID 16700)
-- Name: link fk_link_page_1; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.link
    ADD CONSTRAINT fk_link_page_1 FOREIGN KEY (to_page) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- TOC entry 2752 (class 2606 OID 16705)
-- Name: page_data fk_page_data_data_type; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT fk_page_data_data_type FOREIGN KEY (data_type_code) REFERENCES crawldb.data_type(code) ON DELETE RESTRICT;


--
-- TOC entry 2753 (class 2606 OID 16710)
-- Name: page_data fk_page_data_page; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page_data
    ADD CONSTRAINT fk_page_data_page FOREIGN KEY (page_id) REFERENCES crawldb.page(id) ON DELETE RESTRICT;


--
-- TOC entry 2750 (class 2606 OID 16715)
-- Name: page fk_page_page_type; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT fk_page_page_type FOREIGN KEY (page_type_code) REFERENCES crawldb.page_type(code) ON DELETE RESTRICT;


--
-- TOC entry 2751 (class 2606 OID 16720)
-- Name: page fk_page_site; Type: FK CONSTRAINT; Schema: crawldb; Owner: postgres
--

ALTER TABLE ONLY crawldb.page
    ADD CONSTRAINT fk_page_site FOREIGN KEY (site_id) REFERENCES crawldb.site(id) ON DELETE RESTRICT;


-- Completed on 2019-03-17 15:13:22

--
-- PostgreSQL database dump complete
--

