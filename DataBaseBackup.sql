--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

-- Started on 2025-05-30 19:24:01

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
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 899 (class 1247 OID 18625)
-- Name: BorrowRequestStatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."BorrowRequestStatus" AS ENUM (
    'pending',
    'accepted',
    'rejected'
);


ALTER TYPE public."BorrowRequestStatus" OWNER TO postgres;

--
-- TOC entry 893 (class 1247 OID 18596)
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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 237 (class 1259 OID 18644)
-- Name: Admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Admin" (
    user_id integer NOT NULL
);


ALTER TABLE public."Admin" OWNER TO postgres;

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
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 236
-- Name: Admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Admin_id_seq" OWNED BY public."Admin".user_id;


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
-- TOC entry 4975 (class 0 OID 0)
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
-- TOC entry 4976 (class 0 OID 0)
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
-- TOC entry 4977 (class 0 OID 0)
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
-- TOC entry 4978 (class 0 OID 0)
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
-- TOC entry 4979 (class 0 OID 0)
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
    user_id integer NOT NULL,
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
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 230
-- Name: LibrarianActivityLog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."LibrarianActivityLog_id_seq" OWNED BY public."LibrarianActivityLog".id;


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
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 226
-- Name: Librarian_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Librarian_id_seq" OWNED BY public."Librarian".user_id;


--
-- TOC entry 225 (class 1259 OID 18556)
-- Name: Member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Member" (
    user_id integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    join_date timestamp with time zone NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public."Member" OWNER TO postgres;

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
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 224
-- Name: Member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Member_id_seq" OWNED BY public."Member".user_id;


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
-- TOC entry 4983 (class 0 OID 0)
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
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 217
-- Name: Publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Publisher_id_seq" OWNED BY public."Publisher".id;


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
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 238
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- TOC entry 4761 (class 2604 OID 18512)
-- Name: Author id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Author" ALTER COLUMN id SET DEFAULT nextval('public."Author_id_seq"'::regclass);


--
-- TOC entry 4764 (class 2604 OID 18539)
-- Name: Book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book" ALTER COLUMN id SET DEFAULT nextval('public."Book_id_seq"'::regclass);


--
-- TOC entry 4770 (class 2604 OID 18621)
-- Name: BorrowRequest id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest" ALTER COLUMN id SET DEFAULT nextval('public."BorrowRequest_id_seq"'::regclass);


--
-- TOC entry 4767 (class 2604 OID 18584)
-- Name: Borrowing id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing" ALTER COLUMN id SET DEFAULT nextval('public."Borrowing_id_seq"'::regclass);


--
-- TOC entry 4763 (class 2604 OID 18530)
-- Name: Category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Category" ALTER COLUMN id SET DEFAULT nextval('public."Category_id_seq"'::regclass);


--
-- TOC entry 4769 (class 2604 OID 18592)
-- Name: LibrarianActivityLog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog" ALTER COLUMN id SET DEFAULT nextval('public."LibrarianActivityLog_id_seq"'::regclass);


--
-- TOC entry 4771 (class 2604 OID 18637)
-- Name: Message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message" ALTER COLUMN id SET DEFAULT nextval('public."Message_id_seq"'::regclass);


--
-- TOC entry 4762 (class 2604 OID 18521)
-- Name: Publisher id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Publisher" ALTER COLUMN id SET DEFAULT nextval('public."Publisher_id_seq"'::regclass);


--
-- TOC entry 4773 (class 2604 OID 18656)
-- Name: User id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- TOC entry 4799 (class 2606 OID 18649)
-- Name: Admin Admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admin"
    ADD CONSTRAINT "Admin_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 4775 (class 2606 OID 18516)
-- Name: Author Author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Author"
    ADD CONSTRAINT "Author_pkey" PRIMARY KEY (id);


--
-- TOC entry 4805 (class 2606 OID 18691)
-- Name: BookAuthor BookAuthor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_pkey" PRIMARY KEY (book_id, author_id);


--
-- TOC entry 4807 (class 2606 OID 18706)
-- Name: BookCategory BookCategory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_pkey" PRIMARY KEY (book_id, category_id);


--
-- TOC entry 4781 (class 2606 OID 18543)
-- Name: Book Book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_pkey" PRIMARY KEY (id);


--
-- TOC entry 4795 (class 2606 OID 18623)
-- Name: BorrowRequest BorrowRequest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_pkey" PRIMARY KEY (id);


--
-- TOC entry 4791 (class 2606 OID 18587)
-- Name: Borrowing Borrowing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_pkey" PRIMARY KEY (id);


--
-- TOC entry 4779 (class 2606 OID 18534)
-- Name: Category Category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Category"
    ADD CONSTRAINT "Category_pkey" PRIMARY KEY (id);


--
-- TOC entry 4783 (class 2606 OID 18549)
-- Name: Guest Guest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Guest"
    ADD CONSTRAINT "Guest_pkey" PRIMARY KEY (id);


--
-- TOC entry 4793 (class 2606 OID 18594)
-- Name: LibrarianActivityLog LibrarianActivityLog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_pkey" PRIMARY KEY (id);


--
-- TOC entry 4789 (class 2606 OID 18577)
-- Name: Librarian Librarian_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Librarian"
    ADD CONSTRAINT "Librarian_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 4785 (class 2606 OID 18568)
-- Name: Member Member_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_email_key" UNIQUE (email);


--
-- TOC entry 4787 (class 2606 OID 18564)
-- Name: Member Member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 4797 (class 2606 OID 18642)
-- Name: Message Message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message"
    ADD CONSTRAINT "Message_pkey" PRIMARY KEY (id);


--
-- TOC entry 4777 (class 2606 OID 18525)
-- Name: Publisher Publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Publisher"
    ADD CONSTRAINT "Publisher_pkey" PRIMARY KEY (id);


--
-- TOC entry 4801 (class 2606 OID 18658)
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 4803 (class 2606 OID 18660)
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- TOC entry 4820 (class 2606 OID 18672)
-- Name: Admin Admin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admin"
    ADD CONSTRAINT "Admin_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id) ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 4821 (class 2606 OID 18697)
-- Name: BookAuthor BookAuthor_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_author_id_fkey" FOREIGN KEY (author_id) REFERENCES public."Author"(id);


--
-- TOC entry 4822 (class 2606 OID 18692)
-- Name: BookAuthor BookAuthor_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookAuthor"
    ADD CONSTRAINT "BookAuthor_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id);


--
-- TOC entry 4823 (class 2606 OID 18707)
-- Name: BookCategory BookCategory_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id);


--
-- TOC entry 4824 (class 2606 OID 18712)
-- Name: BookCategory BookCategory_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BookCategory"
    ADD CONSTRAINT "BookCategory_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public."Category"(id);


--
-- TOC entry 4808 (class 2606 OID 18682)
-- Name: Book Book_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_publisher_id_fkey" FOREIGN KEY (publisher_id) REFERENCES public."Publisher"(id) NOT VALID;


--
-- TOC entry 4816 (class 2606 OID 18722)
-- Name: BorrowRequest BorrowRequest_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4817 (class 2606 OID 18727)
-- Name: BorrowRequest BorrowRequest_handled_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_handled_by_fkey" FOREIGN KEY (handled_by) REFERENCES public."Librarian"(user_id) NOT VALID;


--
-- TOC entry 4818 (class 2606 OID 18717)
-- Name: BorrowRequest BorrowRequest_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."BorrowRequest"
    ADD CONSTRAINT "BorrowRequest_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(user_id) NOT VALID;


--
-- TOC entry 4811 (class 2606 OID 18737)
-- Name: Borrowing Borrowing_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4812 (class 2606 OID 18732)
-- Name: Borrowing Borrowing_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Borrowing"
    ADD CONSTRAINT "Borrowing_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(user_id) NOT VALID;


--
-- TOC entry 4813 (class 2606 OID 18747)
-- Name: LibrarianActivityLog LibrarianActivityLog_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(id) NOT VALID;


--
-- TOC entry 4814 (class 2606 OID 18742)
-- Name: LibrarianActivityLog LibrarianActivityLog_librarian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_librarian_id_fkey" FOREIGN KEY (librarian_id) REFERENCES public."Librarian"(user_id) NOT VALID;


--
-- TOC entry 4815 (class 2606 OID 18752)
-- Name: LibrarianActivityLog LibrarianActivityLog_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."LibrarianActivityLog"
    ADD CONSTRAINT "LibrarianActivityLog_member_id_fkey" FOREIGN KEY (member_id) REFERENCES public."Member"(user_id) NOT VALID;


--
-- TOC entry 4810 (class 2606 OID 18667)
-- Name: Librarian Librarian_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Librarian"
    ADD CONSTRAINT "Librarian_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id) ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 4809 (class 2606 OID 18662)
-- Name: Member Member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Member"
    ADD CONSTRAINT "Member_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id) ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 4819 (class 2606 OID 18757)
-- Name: Message Message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Message"
    ADD CONSTRAINT "Message_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id) NOT VALID;


-- Completed on 2025-05-30 19:24:01

--
-- PostgreSQL database dump complete
--

