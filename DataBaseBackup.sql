--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

-- Started on 2025-06-09 22:55:55

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 913 (class 1247 OID 18625)
-- Name: BorrowRequestStatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."BorrowRequestStatus" AS ENUM (
    'pending',
    'accepted',
    'rejected'
);


ALTER TYPE public."BorrowRequestStatus" OWNER TO postgres;

--
-- TOC entry 907 (class 1247 OID 18596)
-- Name: LibrarianAction; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."LibrarianAction" AS ENUM (
    'create_member',
    'update_member_password',
    'deactivate_member',
    'activate_member',
    'create_book',
    'update_book',
    'delete_book',
    'accept_borrow_request',
    'reject_borrow_request',
    'send_message'
);


ALTER TYPE public."LibrarianAction" OWNER TO postgres;

--
-- TOC entry 961 (class 1247 OID 18864)
-- Name: UserType; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."UserType" AS ENUM (
    'admin',
    'librarian',
    'member'
);


ALTER TYPE public."UserType" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 237 (class 1259 OID 18644)
-- Name: Admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Admin" (
    id integer NOT NULL
);


ALTER TABLE public."Admin" OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 18653)
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    hashed_password character varying(200) NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 18795)
-- Name: AdminView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."AdminView" AS
 SELECT "User".id,
    "User".username,
    "User".hashed_password
   FROM (public."Admin"
     JOIN public."User" ON (("User".id = "Admin".id)));


ALTER VIEW public."AdminView" OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 18643)
-- Name: Admin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Admin_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Admin_id_seq" OWNER TO postgres;

--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 236
-- Name: Admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Admin_id_seq" OWNED BY public."Admin".id;


--
-- TOC entry 216 (class 1259 OID 18509)
-- Name: Author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Author" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    biography text
);


ALTER TABLE public."Author" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 18769)
-- Name: AuthorView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."AuthorView" AS
SELECT
    NULL::integer AS id,
    NULL::character varying(255) AS name,
    NULL::text AS books,
    NULL::text AS biography;


ALTER VIEW public."AuthorView" OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 18508)
-- Name: Author_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Author_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Author_id_seq" OWNER TO postgres;

--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 215
-- Name: Author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Author_id_seq" OWNED BY public."Author".id;


--
-- TOC entry 222 (class 1259 OID 18536)
-- Name: Book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Book" (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    publisher_id integer NOT NULL,
    total_copies integer NOT NULL,
    available_copies integer NOT NULL
);


ALTER TABLE public."Book" OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 18687)
-- Name: BookAuthor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BookAuthor" (
    book_id integer NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public."BookAuthor" OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 18702)
-- Name: BookCategory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BookCategory" (
    book_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public."BookCategory" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 18764)
-- Name: BookView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."BookView" AS
SELECT
    NULL::integer AS id,
    NULL::character varying(255) AS title,
    NULL::character varying(255) AS publisher,
    NULL::text AS author,
    NULL::text AS category,
    NULL::integer AS total_copies,
    NULL::integer AS available_copies;


ALTER VIEW public."BookView" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 18535)
-- Name: Book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Book_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Book_id_seq" OWNER TO postgres;

--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 221
-- Name: Book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Book_id_seq" OWNED BY public."Book".id;


--
-- TOC entry 233 (class 1259 OID 18618)
-- Name: BorrowRequest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BorrowRequest" (
    id integer NOT NULL,
    member_id integer NOT NULL,
    book_id integer NOT NULL,
    request_timestamp timestamp with time zone NOT NULL,
    status public."BorrowRequestStatus" NOT NULL,
    handled_at timestamp with time zone,
    handled_by integer,
    note character varying
);


ALTER TABLE public."BorrowRequest" OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 18617)
-- Name: BorrowRequest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."BorrowRequest_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."BorrowRequest_id_seq" OWNER TO postgres;

--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 232
-- Name: BorrowRequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."BorrowRequest_id_seq" OWNED BY public."BorrowRequest".id;


--
-- TOC entry 229 (class 1259 OID 18581)
-- Name: Borrowing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Borrowing" (
    id integer NOT NULL,
    member_id integer NOT NULL,
    book_id integer NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone,
    returned boolean DEFAULT false NOT NULL
);


ALTER TABLE public."Borrowing" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 18556)
-- Name: Member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Member" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    join_date timestamp with time zone NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public."Member" OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 18840)
-- Name: BorrowingView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."BorrowingView" AS
 SELECT "Borrowing".id,
    "Member".name,
    "Book".title AS book,
    "Borrowing".start_date,
    "Borrowing".end_date,
    "Borrowing".returned
   FROM ((public."Borrowing"
     JOIN public."Member" ON (("Member".id = "Borrowing".member_id)))
     JOIN public."Book" ON (("Book".id = "Borrowing".book_id)));


ALTER VIEW public."BorrowingView" OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 18580)
-- Name: Borrowing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Borrowing_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Borrowing_id_seq" OWNER TO postgres;

--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 228
-- Name: Borrowing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Borrowing_id_seq" OWNED BY public."Borrowing".id;


--
-- TOC entry 220 (class 1259 OID 18527)
-- Name: Category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Category" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE public."Category" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 18774)
-- Name: CategoryView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."CategoryView" AS
SELECT
    NULL::integer AS id,
    NULL::character varying(255) AS name,
    NULL::text AS books,
    NULL::text AS description;


ALTER VIEW public."CategoryView" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 18526)
-- Name: Category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Category_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Category_id_seq" OWNER TO postgres;

--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 219
-- Name: Category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Category_id_seq" OWNED BY public."Category".id;


--
-- TOC entry 223 (class 1259 OID 18544)
-- Name: Guest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Guest" (
    id uuid NOT NULL,
    created_time timestamp with time zone NOT NULL,
    request_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public."Guest" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 18570)
-- Name: Librarian; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Librarian" (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public."Librarian" OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 18589)
-- Name: LibrarianActivityLog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."LibrarianActivityLog" (
    id integer NOT NULL,
    librarian_id integer NOT NULL,
    action_type public."LibrarianAction" NOT NULL,
    book_id integer,
    member_id integer,
    "timestamp" timestamp with time zone NOT NULL
);


ALTER TABLE public."LibrarianActivityLog" OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 18835)
-- Name: LibrarianActivityLogView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."LibrarianActivityLogView" AS
 SELECT "LibrarianActivityLog".id,
    "Librarian".name AS librarian_name,
    "LibrarianActivityLog".action_type,
    "Book".title AS book,
    "Member".name AS member,
    "LibrarianActivityLog"."timestamp"
   FROM (((public."LibrarianActivityLog"
     JOIN public."Librarian" ON (("Librarian".id = "LibrarianActivityLog".librarian_id)))
     LEFT JOIN public."Book" ON (("Book".id = "LibrarianActivityLog".book_id)))
     LEFT JOIN public."Member" ON (("Member".id = "LibrarianActivityLog".member_id)))
  ORDER BY "LibrarianActivityLog"."timestamp";


ALTER VIEW public."LibrarianActivityLogView" OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 18588)
-- Name: LibrarianActivityLog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."LibrarianActivityLog_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."LibrarianActivityLog_id_seq" OWNER TO postgres;

--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 230
-- Name: LibrarianActivityLog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."LibrarianActivityLog_id_seq" OWNED BY public."LibrarianActivityLog".id;


--
-- TOC entry 246 (class 1259 OID 18783)
-- Name: LibrarianView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."LibrarianView" AS
 SELECT "User".id,
    "Librarian".name,
    "User".username,
    "User".hashed_password
   FROM (public."Librarian"
     JOIN public."User" ON (("User".id = "Librarian".id)));


ALTER VIEW public."LibrarianView" OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 18569)
-- Name: Librarian_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Librarian_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Librarian_id_seq" OWNER TO postgres;

--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 226
-- Name: Librarian_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Librarian_id_seq" OWNED BY public."Librarian".id;


--
-- TOC entry 245 (class 1259 OID 18779)
-- Name: MemberView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."MemberView" AS
 SELECT "User".id,
    "Member".name,
    "User".username,
    "User".hashed_password,
    "Member".email,
    "Member".join_date,
    "Member".active
   FROM (public."Member"
     JOIN public."User" ON (("User".id = "Member".id)));


ALTER VIEW public."MemberView" OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 18882)
-- Name: MemberWithoutPasswordView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."MemberWithoutPasswordView" AS
 SELECT "User".id,
    "Member".name,
    "User".username,
    "Member".email,
    "Member".join_date,
    "Member".active
   FROM (public."Member"
     JOIN public."User" ON (("User".id = "Member".id)));


ALTER VIEW public."MemberWithoutPasswordView" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 18555)
-- Name: Member_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Member_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Member_id_seq" OWNER TO postgres;

--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 224
-- Name: Member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Member_id_seq" OWNED BY public."Member".id;


--
-- TOC entry 250 (class 1259 OID 18844)
-- Name: MembersBorrowRequestView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."MembersBorrowRequestView" AS
 SELECT "BorrowRequest".id,
    "Member".name,
    "Book".title AS book,
    "BorrowRequest".request_timestamp,
    "BorrowRequest".status,
    "BorrowRequest".handled_at,
    "Librarian".name AS handled_by,
    "BorrowRequest".note
   FROM (((public."BorrowRequest"
     JOIN public."Member" ON (("Member".id = "BorrowRequest".member_id)))
     JOIN public."Book" ON (("Book".id = "BorrowRequest".book_id)))
     LEFT JOIN public."Librarian" ON (("Librarian".id = "BorrowRequest".handled_by)));


ALTER VIEW public."MembersBorrowRequestView" OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 18634)
-- Name: Message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Message" (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text,
    created_time timestamp with time zone NOT NULL,
    seen boolean DEFAULT false NOT NULL
);


ALTER TABLE public."Message" OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 18876)
-- Name: UserWithoutPasswordView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."UserWithoutPasswordView" AS
 SELECT "User".id,
    "User".username,
    COALESCE("Member".name, "Librarian".name) AS name,
        CASE
            WHEN ("Librarian".id IS NOT NULL) THEN 'librarian'::public."UserType"
            WHEN ("Member".id IS NOT NULL) THEN 'member'::public."UserType"
            ELSE 'admin'::public."UserType"
        END AS user_type
   FROM ((public."User"
     LEFT JOIN public."Librarian" ON (("User".id = "Librarian".id)))
     LEFT JOIN public."Member" ON (("User".id = "Member".id)))
  ORDER BY "User".id;


ALTER VIEW public."UserWithoutPasswordView" OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 18927)
-- Name: MessageView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."MessageView" AS
 SELECT "Message".id,
    "UserWithoutPasswordView".username AS "to",
    "UserWithoutPasswordView".user_type AS receiver_role,
    "Message".message,
    "Message".created_time,
    "Message".seen
   FROM (public."Message"
     JOIN public."UserWithoutPasswordView" ON (("UserWithoutPasswordView".id = "Message".user_id)))
  ORDER BY "Message".created_time DESC;


ALTER VIEW public."MessageView" OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 18633)
-- Name: Message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Message_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Message_id_seq" OWNER TO postgres;

--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 234
-- Name: Message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Message_id_seq" OWNED BY public."Message".id;


--
-- TOC entry 218 (class 1259 OID 18518)
-- Name: Publisher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Publisher" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address text,
    contact_email character varying(255),
    phone character varying(255)
);


ALTER TABLE public."Publisher" OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 18850)
-- Name: PublisherView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."PublisherView" AS
SELECT
    NULL::integer AS id,
    NULL::character varying(255) AS name,
    NULL::text AS address,
    NULL::character varying(255) AS contact_email,
    NULL::character varying(255) AS phone,
    NULL::text AS books;


ALTER VIEW public."PublisherView" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 18517)
-- Name: Publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Publisher_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Publisher_id_seq" OWNER TO postgres;

--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 217
-- Name: Publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Publisher_id_seq" OWNED BY public."Publisher".id;


--
-- TOC entry 252 (class 1259 OID 18871)
-- Name: UserView; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."UserView" AS
 SELECT "User".id,
    "User".username,
    "User".hashed_password,
    COALESCE("Member".name, "Librarian".name) AS name,
        CASE
            WHEN ("Librarian".id IS NOT NULL) THEN 'librarian'::public."UserType"
            WHEN ("Member".id IS NOT NULL) THEN 'member'::public."UserType"
            ELSE 'admin'::public."UserType"
        END AS user_type
   FROM ((public."User"
     LEFT JOIN public."Librarian" ON (("User".id = "Librarian".id)))
     LEFT JOIN public."Member" ON (("User".id = "Member".id)))
  ORDER BY "User".id;


ALTER VIEW public."UserView" OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 18652)
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_id_seq" OWNER TO postgres;

--
-- TOC entry 5073 (class 0 OID 0)
-- Dependencies: 238
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- TOC entry 4820 (class 2604 OID 18512)
-- Name: Author id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Author" ALTER COLUMN id SET DEFAULT nextval('public."Author_id_seq"'::regclass);


--
-- TOC entry 4823 (class 2604 OID 18539)
-- Name: Book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book" ALTER COLUMN id SET DEFAULT nextval('public."Book_id_seq"'::regclass);


--
-- TOC entry 4829 (class 2604 OID 18621)
-- Name: BorrowRequest id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest" ALTER COLUMN id SET DEFAULT nextval('public."BorrowRequest_id_seq"'::regclass);


--
-- TOC entry 4826 (class 2604 OID 18584)
-- Name: Borrowing id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing" ALTER COLUMN id SET DEFAULT nextval('public."Borrowing_id_seq"'::regclass);


--
-- TOC entry 4822 (class 2604 OID 18530)
-- Name: Category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Category" ALTER COLUMN id SET DEFAULT nextval('public."Category_id_seq"'::regclass);


--
-- TOC entry 4828 (class 2604 OID 18592)
-- Name: LibrarianActivityLog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog" ALTER COLUMN id SET DEFAULT nextval('public."LibrarianActivityLog_id_seq"'::regclass);


--
-- TOC entry 4830 (class 2604 OID 18637)
-- Name: Message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message" ALTER COLUMN id SET DEFAULT nextval('public."Message_id_seq"'::regclass);


--
-- TOC entry 4821 (class 2604 OID 18521)
-- Name: Publisher id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Publisher" ALTER COLUMN id SET DEFAULT nextval('public."Publisher_id_seq"'::regclass);


--
-- TOC entry 4832 (class 2604 OID 18656)
-- Name: User id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- TOC entry 4873 (class 2606 OID 18649)
-- Name: Admin Admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admin"
    ADD CONSTRAINT "Admin_pkey" PRIMARY KEY (id);


--
-- TOC entry 4841 (class 2606 OID 18887)
-- Name: Author Author_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Author"
    ADD CONSTRAINT "Author_name_key" UNIQUE (name);


--
-- TOC entry 4843 (class 2606 OID 18516)
-- Name: Author Author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Author"
    ADD CONSTRAINT "Author_pkey" PRIMARY KEY (id);


--
-- TOC entry 4879 (class 2606 OID 18691)
-- Name: BookAuthor BookAuthor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_pkey" PRIMARY KEY (book_id, author_id);


--
-- TOC entry 4881 (class 2606 OID 18706)
-- Name: BookCategory BookCategory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_pkey" PRIMARY KEY (book_id, category_id);


--
-- TOC entry 4835 (class 2606 OID 18895)
-- Name: Book Book_available_copies_check; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Book"
    ADD CONSTRAINT "Book_available_copies_check" CHECK ((available_copies >= 0)) NOT VALID;


--
-- TOC entry 4836 (class 2606 OID 18894)
-- Name: Book Book_check; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Book"
    ADD CONSTRAINT "Book_check" CHECK ((available_copies <= total_copies)) NOT VALID;


--
-- TOC entry 4853 (class 2606 OID 18543)
-- Name: Book Book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_pkey" PRIMARY KEY (id);


--
-- TOC entry 4855 (class 2606 OID 18893)
-- Name: Book Book_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_title_key" UNIQUE (title);


--
-- TOC entry 4837 (class 2606 OID 18896)
-- Name: Book Book_total_copies_check; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Book"
    ADD CONSTRAINT "Book_total_copies_check" CHECK ((total_copies >= 0)) NOT VALID;


--
-- TOC entry 4869 (class 2606 OID 18623)
-- Name: BorrowRequest BorrowRequest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_pkey" PRIMARY KEY (id);


--
-- TOC entry 4865 (class 2606 OID 18587)
-- Name: Borrowing Borrowing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_pkey" PRIMARY KEY (id);


--
-- TOC entry 4849 (class 2606 OID 18763)
-- Name: Category Category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Category"
    ADD CONSTRAINT "Category_name_key" UNIQUE (name);


--
-- TOC entry 4851 (class 2606 OID 18534)
-- Name: Category Category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Category"
    ADD CONSTRAINT "Category_pkey" PRIMARY KEY (id);


--
-- TOC entry 4857 (class 2606 OID 18549)
-- Name: Guest Guest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Guest"
    ADD CONSTRAINT "Guest_pkey" PRIMARY KEY (id);


--
-- TOC entry 4867 (class 2606 OID 18594)
-- Name: LibrarianActivityLog LibrarianActivityLog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_pkey" PRIMARY KEY (id);


--
-- TOC entry 4863 (class 2606 OID 18577)
-- Name: Librarian Librarian_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Librarian"
    ADD CONSTRAINT "Librarian_pkey" PRIMARY KEY (id);


--
-- TOC entry 4859 (class 2606 OID 18568)
-- Name: Member Member_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_email_key" UNIQUE (email);


--
-- TOC entry 4861 (class 2606 OID 18564)
-- Name: Member Member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_pkey" PRIMARY KEY (id);


--
-- TOC entry 4871 (class 2606 OID 18642)
-- Name: Message Message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message"
    ADD CONSTRAINT "Message_pkey" PRIMARY KEY (id);


--
-- TOC entry 4845 (class 2606 OID 18889)
-- Name: Publisher Publisher_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Publisher"
    ADD CONSTRAINT "Publisher_name_key" UNIQUE (name);


--
-- TOC entry 4847 (class 2606 OID 18525)
-- Name: Publisher Publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Publisher"
    ADD CONSTRAINT "Publisher_pkey" PRIMARY KEY (id);


--
-- TOC entry 4875 (class 2606 OID 18658)
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 4839 (class 2606 OID 18881)
-- Name: User User_username_check; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."User"
    ADD CONSTRAINT "User_username_check" CHECK (((username)::text ~* '^[a-zA-Z][a-zA-Z0-9_]{2,15}$'::text)) NOT VALID;


--
-- TOC entry 4877 (class 2606 OID 18660)
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- TOC entry 4838 (class 2606 OID 18834)
-- Name: Member valid_email; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Member"
    ADD CONSTRAINT valid_email CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)) NOT VALID;


--
-- TOC entry 4833 (class 2606 OID 18890)
-- Name: Publisher valid_email; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Publisher"
    ADD CONSTRAINT valid_email CHECK (((contact_email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)) NOT VALID;


--
-- TOC entry 4834 (class 2606 OID 18891)
-- Name: Publisher valid_phone; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."Publisher"
    ADD CONSTRAINT valid_phone CHECK (((phone)::text ~* '^0\d{2,3}-?\d{8}$'::text)) NOT VALID;


--
-- TOC entry 5042 (class 2618 OID 18767)
-- Name: BookView _RETURN; Type: RULE; Schema: public; Owner: postgres
--

CREATE OR REPLACE VIEW public."BookView" AS
 SELECT "Book".id,
    "Book".title,
    "Publisher".name AS publisher,
    string_agg(DISTINCT ("Author".name)::text, ' ،'::text) AS author,
    string_agg(DISTINCT ("Category".name)::text, ' ،'::text) AS category,
    "Book".total_copies,
    "Book".available_copies
   FROM (((((public."Book"
     JOIN public."Publisher" ON (("Book".publisher_id = "Publisher".id)))
     JOIN public."BookAuthor" ON (("Book".id = "BookAuthor".book_id)))
     JOIN public."Author" ON (("BookAuthor".author_id = "Author".id)))
     JOIN public."BookCategory" ON (("BookCategory".book_id = "Book".id)))
     JOIN public."Category" ON (("BookCategory".category_id = "Category".id)))
  GROUP BY "Book".id, "Publisher".name;


--
-- TOC entry 5043 (class 2618 OID 18772)
-- Name: AuthorView _RETURN; Type: RULE; Schema: public; Owner: postgres
--

CREATE OR REPLACE VIEW public."AuthorView" AS
 SELECT "Author".id,
    "Author".name,
    string_agg(DISTINCT ("Book".title)::text, ' ،'::text) AS books,
    "Author".biography
   FROM ((public."Author"
     JOIN public."BookAuthor" ON (("BookAuthor".author_id = "Author".id)))
     JOIN public."Book" ON (("Book".id = "BookAuthor".book_id)))
  GROUP BY "Author".id;


--
-- TOC entry 5044 (class 2618 OID 18777)
-- Name: CategoryView _RETURN; Type: RULE; Schema: public; Owner: postgres
--

CREATE OR REPLACE VIEW public."CategoryView" AS
 SELECT "Category".id,
    "Category".name,
    string_agg(DISTINCT ("Book".title)::text, ' ،'::text) AS books,
    "Category".description
   FROM ((public."Category"
     JOIN public."BookCategory" ON (("BookCategory".category_id = "Category".id)))
     JOIN public."Book" ON (("Book".id = "BookCategory".book_id)))
  GROUP BY "Category".id;


--
-- TOC entry 5051 (class 2618 OID 18853)
-- Name: PublisherView _RETURN; Type: RULE; Schema: public; Owner: postgres
--

CREATE OR REPLACE VIEW public."PublisherView" AS
 SELECT "Publisher".id,
    "Publisher".name,
    "Publisher".address,
    "Publisher".contact_email,
    "Publisher".phone,
    string_agg(("Book".title)::text, ' ،'::text) AS books
   FROM (public."Publisher"
     LEFT JOIN public."Book" ON (("Book".publisher_id = "Publisher".id)))
  GROUP BY "Publisher".id
  ORDER BY "Publisher".id;


--
-- TOC entry 4894 (class 2606 OID 18672)
-- Name: Admin Admin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admin"
    ADD CONSTRAINT "Admin_user_id_fkey" FOREIGN KEY (id) REFERENCES public."User"(id) ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 4895 (class 2606 OID 18902)
-- Name: BookAuthor BookAuthor_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_author_id_fkey" FOREIGN KEY (author_id) REFERENCES public."Author"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4896 (class 2606 OID 18897)
-- Name: BookAuthor BookAuthor_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4897 (class 2606 OID 18907)
-- Name: BookCategory BookCategory_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4898 (class 2606 OID 18912)
-- Name: BookCategory BookCategory_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public."Category"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4882 (class 2606 OID 18682)
-- Name: Book Book_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_publisher_id_fkey" FOREIGN KEY (publisher_id) REFERENCES public."Publisher"(id) NOT VALID;


--
-- TOC entry 4890 (class 2606 OID 18722)
-- Name: BorrowRequest BorrowRequest_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4891 (class 2606 OID 18727)
-- Name: BorrowRequest BorrowRequest_handled_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_handled_by_fkey" FOREIGN KEY (handled_by) REFERENCES public."Librarian"(id) NOT VALID;


--
-- TOC entry 4892 (class 2606 OID 18717)
-- Name: BorrowRequest BorrowRequest_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(id) NOT VALID;


--
-- TOC entry 4885 (class 2606 OID 18737)
-- Name: Borrowing Borrowing_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4886 (class 2606 OID 18732)
-- Name: Borrowing Borrowing_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(id) NOT VALID;


--
-- TOC entry 4887 (class 2606 OID 18747)
-- Name: LibrarianActivityLog LibrarianActivityLog_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4888 (class 2606 OID 18742)
-- Name: LibrarianActivityLog LibrarianActivityLog_librarian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_librarian_id_fkey" FOREIGN KEY (librarian_id) REFERENCES public."Librarian"(id) NOT VALID;


--
-- TOC entry 4889 (class 2606 OID 18752)
-- Name: LibrarianActivityLog LibrarianActivityLog_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(id) NOT VALID;


--
-- TOC entry 4884 (class 2606 OID 18922)
-- Name: Librarian Librarian_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Librarian"
    ADD CONSTRAINT "Librarian_user_id_fkey" FOREIGN KEY (id) REFERENCES public."User"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4883 (class 2606 OID 18917)
-- Name: Member Member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_user_id_fkey" FOREIGN KEY (id) REFERENCES public."User"(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4893 (class 2606 OID 18757)
-- Name: Message Message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message"
    ADD CONSTRAINT "Message_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id) NOT VALID;


-- Completed on 2025-06-09 22:55:56

--
-- PostgreSQL database dump complete
--

