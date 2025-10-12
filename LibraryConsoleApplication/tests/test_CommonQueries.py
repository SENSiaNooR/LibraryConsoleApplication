import unittest
import psycopg2
from DataAccess.BaseRepository import BaseRepository
from DataAccess.TestingRepository import TestingRepository
from Exceptions.Exceptions import EmptyModelError, MultipleRowsReturnedError
from Models.Models import TestingViewModel, TestingModel
from Models.Schema import DBTableColumns, DBViewColumns


class TestCommonQueries(unittest.TestCase):
    
    # switch this variable to True, so table will rebuild before running tests. 
    __rebuild_table = False
    __rebuild_table_query = """
    DELETE FROM public."Testing";
    SELECT setval('public."Testng_id_seq"', 81, true);
    INSERT INTO public."Testing" VALUES
	(1, 'Ali', 25, 'Student from Tehran'),
	(2, 'Sara', 30, 'Software engineer'),
	(3, 'Reza', 41, 'Loves hiking and coffee'),
	(4, 'Mina', 22, 'Graphic designer'),
	(5, 'Ahmad', 33, 'Data analyst'),
	(6, 'Neda', 28, 'Enjoys traveling'),
	(7, 'Kaveh', 35, 'Backend developer'),
	(8, 'Parisa', 24, 'Marketing assistant'),
	(9, 'Hossein', 39, 'Project manager'),
	(10, 'Fatemeh', 27, 'Photographer'),
	(11, 'Navid', 31, 'Music producer'),
	(12, 'Leila', 26, 'UI/UX designer'),
	(13, 'Hamed', 29, 'Cybersecurity specialist'),
	(14, 'Zahra', 23, 'Student of biology'),
	(15, 'Sina', 34, 'Mechanical engineer'),
	(16, 'Shirin', 32, 'Content writer'),
	(17, 'Mohammad', 38, 'Teacher'),
	(18, 'Mahsa', 21, 'Art student'),
	(19, 'Omid', 36, 'Civil engineer'),
	(20, 'Negar', 28, 'Nurse'),
	(21, 'Ehsan', 42, 'Financial advisor'),
	(22, 'Roya', 25, 'Social media manager'),
	(23, 'Kian', 40, 'Chef'),
	(24, 'Tara', 22, 'Fashion model'),
	(25, 'Farhad', 33, 'Electrician'),
	(26, 'Nazanin', 27, 'Architect'),
	(27, 'Amir', 29, 'Business consultant'),
	(28, 'Maryam', 30, 'Doctor'),
	(29, 'Armin', 24, 'Game developer'),
	(30, 'Elham', 37, 'HR specialist'),
	(31, 'Sahar', 26, 'Translator'),
	(32, 'Pouya', 28, 'Mobile developer'),
	(33, 'Arezoo', 35, 'Researcher'),
	(34, 'Ramin', 31, 'Economist'),
	(35, 'Yasmin', 23, 'Law student'),
	(36, 'Babak', 45, 'Pilot'),
	(37, 'Shahram', 39, 'Mechanical designer'),
	(38, 'Hanieh', 33, 'Psychologist'),
	(39, 'Behnam', 27, 'Photographer'),
	(40, 'Pegah', 25, 'Web developer'),
	(41, 'احمد', 29, 'دانشجوی رشته مهندسی نرم‌افزار'),
	(42, 'سارا', 24, 'طراح گرافیک در شرکت تبلیغاتی'),
	(43, 'رضا', 35, 'کارشناس شبکه و امنیت اطلاعات'),
	(44, 'مینا', 27, 'مدرس زبان انگلیسی'),
	(45, 'حمید', 40, 'مدیر فروش در یک شرکت بازرگانی'),
	(46, 'ندا', 31, 'نویسنده و تولیدکننده محتوا'),
	(47, 'کاوه', 33, 'برنامه‌نویس ارشد پایتون'),
	(48, 'پریسا', 26, 'دانشجوی کارشناسی ارشد مدیریت'),
	(49, 'حسین', 38, 'مهندس عمران با ۱۰ سال سابقه'),
	(50, 'فاطمه', 22, 'دانشجوی رشته پزشکی'),
	(51, 'نوید', 30, 'توسعه‌دهنده وب'),
	(52, 'لیلا', 28, 'کارشناس منابع انسانی'),
	(53, 'حامد', 34, 'متخصص امنیت سایبری'),
	(54, 'زهرا', 25, 'دانشجوی زیست‌شناسی'),
	(55, 'سینا', 36, 'مهندس مکانیک در شرکت خودروسازی'),
	(56, 'شیرین', 29, 'مترجم و ویراستار متون'),
	(57, 'محمد', 41, 'معلم دبیرستان'),
	(58, 'مهسا', 23, 'دانشجوی هنرهای تجسمی'),
	(59, 'امید', 39, 'مهندس راه و ساختمان'),
	(60, 'نگار', 27, 'پرستار بیمارستان خصوصی'),
	(61, 'احسان', 42, 'مشاور مالی'),
	(62, 'رویا', 25, 'مدیر شبکه‌های اجتماعی'),
	(63, 'کیان', 37, 'سرآشپز رستوران ایتالیایی'),
	(64, 'تارا', 24, 'مدل لباس و بازیگر تازه‌کار'),
	(65, 'فرهاد', 32, 'تعمیرکار برق صنعتی'),
	(66, 'نازنین', 26, 'معمار داخلی'),
	(67, 'امیر', 30, 'مشاور کسب‌وکار'),
	(68, 'مریم', 28, 'پزشک عمومی'),
	(69, 'آرمین', 23, 'توسعه‌دهنده بازی‌های ویدیویی'),
	(70, 'الهام', 35, 'کارشناس منابع انسانی'),
	(71, 'سحر', 29, 'مترجم زبان انگلیسی'),
	(72, 'پویا', 33, 'برنامه‌نویس موبایل'),
	(73, 'آرزو', 31, 'پژوهشگر دانشگاهی'),
	(74, 'رامین', 34, 'تحلیل‌گر اقتصادی'),
	(75, 'یاسمین', 22, 'دانشجوی رشته حقوق'),
	(76, 'بابک', 44, 'خلبان خطوط هوایی'),
	(77, 'شهرام', 38, 'طراح صنعتی'),
	(78, 'هانیه', 27, 'روان‌شناس بالینی'),
	(79, 'بهنام', 25, 'عکاس و تدوین‌گر فیلم'),
	(80, 'پگاه', 28, 'توسعه‌دهنده وب‌سایت');
    """

    def setUp(self) -> None:
        self.cursor = TestingRepository._get_cursor()

        if self.__rebuild_table:
            c = TestingRepository._get_cursor()
            c.execute(self.__rebuild_table_query)
            c.connection.commit()
            c.connection.close()
              
    def tearDown(self) -> None:
        self.cursor.connection.rollback()
        self.cursor.connection.close()
        
    def rollback(self) -> None:
        self.cursor.connection.rollback()


    # ─────────── get_one ────────────
    def test_get_one_case1(self):
        """Case 1: Fetch by name -> record should be found"""
        omid = TestingModel(name="امید")
        fetched = TestingRepository.get_one(omid, self.cursor)
        expected = TestingModel(id=59, name="امید", age=39, description="مهندس راه و ساختمان")
        self.assertEqual(fetched, expected)

    def test_get_one_case2(self):
        """Case 2: Fetch by ID -> record should be found"""
        negar = TestingModel(id=20)
        fetched = TestingRepository.get_one(negar, self.cursor)
        expected = TestingModel(id=20, name="Negar", age=28, description="Nurse")
        self.assertEqual(fetched, expected)

    def test_get_one_case3(self):
        """Case 3: Empty model -> should raise EmptyModelError"""
        with self.assertRaises(EmptyModelError):
            TestingRepository.get_one(TestingModel(), self.cursor)

    def test_get_one_case4(self):
        """Case 4: Non-existent record -> should return None"""
        asghar = TestingModel(name="اصغر")
        fetched = TestingRepository.get_one(asghar, self.cursor)
        self.assertIsNone(fetched)

    def test_get_one_case5(self):
        """Case 5: Multiple record -> should raise MultipleRowsReturnedError"""
        model = TestingModel(age = 29) #
        with self.assertRaises(MultipleRowsReturnedError):
            TestingRepository.get_one(model, self.cursor)
        

    # ─────────── get_many ────────────       
    def test_get_many_case1(self):
        """Case 1: Empty model -> should return all records. (records number limited to 'return_limit')"""
        fetched = TestingRepository.get_many(TestingModel(), self.cursor)
        
        self.assertEqual(len(fetched), 80)
        
        for record in fetched:
            self.assertIsInstance(record, TestingModel)
    
    def test_get_many_case2(self):
        """Case 2: Fetch by age = 23 -> records with 69, 58, 35, 14 id should return"""
        model = TestingModel(age = 23)
        fetched = TestingRepository.get_many(model, self.cursor)
        
        self.assertEqual(len(fetched), 4)
        
        expected1 = TestingModel(id = 69, age = 23, name= 'آرمین', description= 'توسعه‌دهنده بازی‌های ویدیویی')
        expected2 = TestingModel(id = 58, age = 23, name= 'مهسا', description= 'دانشجوی هنرهای تجسمی')
        expected3 = TestingModel(id = 35, age = 23, name= 'Yasmin', description= 'Law student')
        expected4 = TestingModel(id = 14, age = 23, name= 'Zahra', description= 'Student of biology')
        
        self.assertIn(expected1, fetched)
        self.assertIn(expected2, fetched)
        self.assertIn(expected3, fetched)
        self.assertIn(expected4, fetched)
        
    def test_get_many_case3(self):
        """Case 3: Set limiter to records returned count"""
        TestingRepository.return_limit = 20
        fetched = TestingRepository.get_many(TestingModel(), self.cursor)
        self.assertEqual(len(fetched), 20)
        
        TestingRepository.return_limit = BaseRepository.return_limit
        fetched = TestingRepository.get_many(TestingModel(), self.cursor)
        self.assertEqual(len(fetched), 80)
  
    def test_get_many_case4(self):
        """Case 4: Try to filter by restricted field for where clause. -> should return all records."""
        model = TestingModel(description="دانشجو")
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(len(fetched), 6)

        TestingRepository.where_clause_exclude = { DBTableColumns.Testing.DESCRIPTION }
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(len(fetched), 80)
        
        TestingRepository.where_clause_exclude = set()
        
    def test_get_many_case5(self):
        """Case 5: Filter by multiple fields (age + name)."""
        model = TestingModel(name="Neda", age=28)
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(len(fetched), 1)
        expected = TestingModel(id=6, name="Neda", age=28, description="Enjoys traveling")
        self.assertIn(expected, fetched)
        
    def test_get_many_case6(self):
        """Case 6: No matching records."""
        model = TestingModel(name="Asghar", age=99)
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(fetched, [])
    

    # ─────────── view_one ────────────     
    def test_view_one_case1(self):
        """Case 1: Fetch by name -> record should be found"""
        omid = TestingViewModel(name="امید")
        fetched = TestingRepository.view_one(omid, self.cursor)
        expected = TestingViewModel(id=59, name="امید", age=39, description="مهندس راه و ساختمان")
        self.assertEqual(fetched, expected)

    def test_view_one_case2(self):
        """Case 2: Fetch by ID -> record should be found"""
        negar = TestingViewModel(id=20)
        fetched = TestingRepository.view_one(negar, self.cursor)
        expected = TestingViewModel(id=20, name="Negar", age=28, description="Nurse")
        self.assertEqual(fetched, expected)

    def test_view_one_case3(self):
        """Case 3: Empty model -> should raise EmptyModelError"""
        with self.assertRaises(EmptyModelError):
            TestingRepository.view_one(TestingViewModel(), self.cursor)

    def test_view_one_case4(self):
        """Case 4: Non-existent record -> should return None"""
        asghar = TestingViewModel(name="اصغر")
        fetched = TestingRepository.view_one(asghar, self.cursor)
        self.assertIsNone(fetched)

    def test_view_one_case5(self):
        """Case 5: Multiple record -> should raise MultipleRowsReturnedError"""
        model = TestingViewModel(age = 29)
        with self.assertRaises(MultipleRowsReturnedError):
            TestingRepository.view_one(model, self.cursor)


    # ─────────── view_many ────────────
    def test_view_many_case1(self):
        """Case 1: Empty model -> should return all records in sorted sequence due to TestingView implementation in Psql. (records number limited to 'return_limit')
        TestingView:
            SELECT id,name,age,description
            FROM "Testing"
            ORDER BY age DESC;
        """
        fetched = TestingRepository.view_many(TestingViewModel(), self.cursor)
        
        self.assertEqual(len(fetched), 80)
        
        for record in fetched:
            self.assertIsInstance(record, TestingViewModel)
            
        sorted_fetch = sorted(fetched, key = lambda record : record.age, reverse= True)
        self.assertEqual(fetched, sorted_fetch)
    
    def test_view_many_case2(self):
        """Case 2: Fetch by age = 23 -> records with 69, 58, 35, 14 id should return"""
        model = TestingViewModel(age = 23)
        fetched = TestingRepository.view_many(model, self.cursor)
        
        self.assertEqual(len(fetched), 4)
        
        expected1 = TestingViewModel(id = 69, age = 23, name= 'آرمین', description= 'توسعه‌دهنده بازی‌های ویدیویی')
        expected2 = TestingViewModel(id = 58, age = 23, name= 'مهسا', description= 'دانشجوی هنرهای تجسمی')
        expected3 = TestingViewModel(id = 35, age = 23, name= 'Yasmin', description= 'Law student')
        expected4 = TestingViewModel(id = 14, age = 23, name= 'Zahra', description= 'Student of biology')
        
        self.assertIn(expected1, fetched)
        self.assertIn(expected2, fetched)
        self.assertIn(expected3, fetched)
        self.assertIn(expected4, fetched)
          
    def test_view_many_case3(self):
        """Case 4: Try to filter by restricted field for where clause. -> should return all records."""
        model = TestingViewModel(description="دانشجو")
        fetched = TestingRepository.view_many(model, self.cursor)
        self.assertEqual(len(fetched), 6)

        TestingRepository.where_clause_exclude = { DBViewColumns.TestingView.DESCRIPTION }
        fetched = TestingRepository.view_many(model, self.cursor)
        self.assertEqual(len(fetched), 80)
        
        TestingRepository.where_clause_exclude = set()
        
    def test_view_many_case4(self):
        """Case 5: Filter by multiple fields (age + name)."""
        model = TestingViewModel(name="Neda", age=28)
        fetched = TestingRepository.view_many(model, self.cursor)
        self.assertEqual(len(fetched), 1)
        expected = TestingViewModel(id=6, name="Neda", age=28, description="Enjoys traveling")
        self.assertIn(expected, fetched)
        
    def test_view_many_case5(self):
        """Case 6: No matching records."""
        model = TestingViewModel(name="Asghar", age=99)
        fetched = TestingRepository.view_many(model, self.cursor)
        self.assertEqual(fetched, [])
    

    # ─────────── add ────────────
    def test_add_case1(self):
        """Case 1: Add record"""
        model = TestingModel(name='سجاد', age=25, description='امنیت شبکه')
        added_record = TestingRepository.add(model, self.cursor)
        self.assertIsNotNone(added_record)
        fetched = TestingRepository.get_one(model, self.cursor)
        self.assertIsNotNone(fetched)
        self.rollback()

    def test_add_case2(self):
        """Case 2: Try to add record with Unset or None value
        Testing Table:
            CREATE TABLE Testing (
            id integer NOT NULL,
            name character varying(255) DEFAULT 'ناشناس'::character varying NOT NULL,
            age integer,
            description character varying(255)
            );
        """
        model = TestingModel(age=25, description='امنیت شبکه')
        added_record = TestingRepository.add(model, self.cursor)
        self.assertEqual(added_record.name, 'ناشناس')
        self.rollback()
        
        model = TestingModel(name=None, age=25, description='امنیت شبکه')
        with self.assertRaises(psycopg2.errors.NotNullViolation):
            added_record = TestingRepository.add(model, self.cursor)           
        self.rollback()

    def test_add_case3(self):
        """Case 3: Try to specify excluded field (insert_clause_exclude). should ignore that field"""
        model = TestingModel(id = 10000, name='سجاد', age=25, description='امنیت شبکه')
        added_record = TestingRepository.add(model, self.cursor)
        self.assertNotEqual(added_record.id, 10000)
        self.rollback()

    def test_add_case4(self):
        """Case 4: Try to add empty model."""
        model = TestingModel()
        with self.assertRaises(EmptyModelError):  
            added_record = TestingRepository.add(model, self.cursor)      
        self.rollback()

    def test_add_case5(self):
        """Case 10: Try to inject SQL-like input."""
        model = TestingModel(name="Robert'); DROP TABLE Testing;--", age=20, description="Test")
        added = TestingRepository.add(model, self.cursor)
        self.assertIsNotNone(added.id)
        fetched = TestingRepository.get_many(TestingModel(), self.cursor)
        self.assertNotEqual(fetched, [])
        self.rollback()


    # ─────────── update ────────────
    def test_update_case1(self):
        """Case 1: Successfully update a record field."""
        model = TestingModel(id=20, age=29, description="Updated nurse info")
        TestingRepository.update(model, self.cursor)
    
        fetched = TestingRepository.get_one(TestingModel(id=20), self.cursor)
        self.assertEqual(fetched.age, 29)
        self.assertEqual(fetched.description, "Updated nurse info")
        self.rollback()
    
    def test_update_case2(self):
        """Case 2: Try to update without providing an id -> should raise ValueError."""
        model = TestingModel(name="Sara", age=40)
        with self.assertRaises(ValueError):
            TestingRepository.update(model, self.cursor)
    
    def test_update_case3(self):
        """Case 3: No fields set to update -> should perform no action."""
        model = TestingModel(id=10)
        TestingRepository.update(model, self.cursor)
    
        fetched = TestingRepository.get_one(TestingModel(id=10), self.cursor)
        expected = TestingModel(id=10, name="Fatemeh", age=27, description="Photographer")
        self.assertEqual(fetched, expected)
        self.rollback()
    
    def test_update_case4(self):
        """Case 4: Try to update excluded field (should be ignored)."""
        TestingRepository.set_clause_exclude = {DBTableColumns.Testing.ID, DBTableColumns.Testing.NAME}
    
        model = TestingModel(id=5, name="UpdatedName", age=33)
        TestingRepository.update(model, self.cursor)
    
        fetched = TestingRepository.get_one(TestingModel(id=5), self.cursor)
        self.assertNotEqual(fetched.name, "UpdatedName")
        self.assertEqual(fetched.age, 33)
    
        TestingRepository.set_clause_exclude = {DBTableColumns.Testing.ID}
        self.rollback()
    

    # ─────────── delete ────────────
    def test_delete_case1(self):
        """Case 1: Successfully delete an existing record."""
        fetched = TestingRepository.get_one(TestingModel(id=10), self.cursor)
        self.assertIsNotNone(fetched)

        TestingRepository.delete(10, self.cursor)

        fetched_after = TestingRepository.get_one(TestingModel(id=10), self.cursor)
        self.assertIsNone(fetched_after)
        self.rollback()
            

    # ─────────── remove ────────────
    def test_remove_case1(self):
        """Case 1: Successfully delete selected record."""
        model = TestingModel(age = 23)
        
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertNotEqual(fetched, [])
        
        TestingRepository.remove(model, cursor = self.cursor)
        fetched = TestingRepository.get_many(model, self.cursor)
        
        self.assertEqual(fetched, [])
        self.rollback()

    def test_remove_case2(self):
        """Case 2: Use empty model. -> should raise EmptyModelError."""
        with self.assertRaises(EmptyModelError):
            TestingRepository.remove(TestingModel(), cursor = self.cursor)
        self.rollback()

    def test_remove_case3(self):
        """Case 3: Use like for strings."""
        model = TestingModel(description='دانشجو')
        
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(len(fetched), 6)
        
        TestingRepository.remove(model, use_like_for_strings = False, cursor = self.cursor)
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(len(fetched), 6)

        TestingRepository.remove(model, use_like_for_strings = True, cursor = self.cursor)
        fetched = TestingRepository.get_many(model, self.cursor)
        self.assertEqual(fetched, [])
        
        self.rollback()
            

    # ─────────── clear ────────────
    def test_clear_case1(self):
        """Case 1: Successfully clear table."""
        TestingRepository.clear(self.cursor)
        fetched = TestingRepository.get_many(TestingModel(), self.cursor)
        self.assertEqual(len(fetched), 0)
        self.rollback()

