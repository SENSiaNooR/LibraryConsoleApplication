import unittest
from DataAccess.TestingRepository import TestingRepository
from Exceptions.Exceptions import EmptyModelError, MultipleRowsReturnedError, RepositoryMethodNotAllowedError
from Models.Models import TestingViewModel, TestingModel


class TestCommonQueries(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cursor = TestingRepository._get_cursor()
        
    def tearDown(self) -> None:
        self.cursor.connection.rollback()
        self.cursor.connection.close()
        
    def rollback(self) -> None:
        self.cursor.connection.rollback()
    
    # ──────────────────────────── Testing Table ──────────────────────────
    #
    # id |   name   |   age   |   description
    # ──────────────────────────────────────────────────   
    # 01 |   Ali   ,   25   ,   Student from Tehran
    # 02 |   Sara   ,   30   ,   Software engineer
    # 03 |   Reza   ,   41   ,   Loves hiking and coffee
    # 04 |   Mina   ,   22   ,   Graphic designer
    # 05 |   Ahmad   ,   33   ,   Data analyst
    # 06 |   Neda   ,   28   ,   Enjoys traveling
    # 07 |   Kaveh   ,   35   ,   Backend developer
    # 08 |   Parisa   ,   24   ,   Marketing assistant
    # 09 |   Hossein   ,   39   ,   Project manager
    # 10 |   Fatemeh   ,   27   ,   Photographer
    # 11 |   Navid   ,   31   ,   Music producer
    # 12 |   Leila   ,   26   ,   UI/UX designer
    # 13 |   Hamed   ,   29   ,   Cybersecurity specialist
    # 14 |   Zahra   ,   23   ,   Student of biology
    # 15 |   Sina   ,   34   ,   Mechanical engineer
    # 16 |   Shirin   ,   32   ,   Content writer
    # 17 |   Mohammad   ,   38   ,   Teacher
    # 18 |   Mahsa   ,   21   ,   Art student
    # 19 |   Omid   ,   36   ,   Civil engineer
    # 20 |   Negar   ,   28   ,   Nurse
    # 21 |   Ehsan   ,   42   ,   Financial advisor
    # 22 |   Roya   ,   25   ,   Social media manager
    # 23 |   Kian   ,   40   ,   Chef
    # 24 |   Tara   ,   22   ,   Fashion model
    # 25 |   Farhad   ,   33   ,   Electrician
    # 26 |   Nazanin   ,   27   ,   Architect
    # 27 |   Amir   ,   29   ,   Business consultant
    # 28 |   Maryam   ,   30   ,   Doctor
    # 29 |   Armin   ,   24   ,   Game developer
    # 30 |   Elham   ,   37   ,   HR specialist
    # 31 |   Sahar   ,   26   ,   Translator
    # 32 |   Pouya   ,   28   ,   Mobile developer
    # 33 |   Arezoo   ,   35   ,   Researcher
    # 34 |   Ramin   ,   31   ,   Economist
    # 35 |   Yasmin   ,   23   ,   Law student
    # 36 |   Babak   ,   45   ,   Pilot
    # 37 |   Shahram   ,   39   ,   Mechanical designer
    # 38 |   Hanieh   ,   33   ,   Psychologist
    # 39 |   Behnam   ,   27   ,   Photographer
    # 40 |   Pegah   ,   25   ,   Web developer
    # 41 |   احمد   ,   29   ,   دانشجوی رشته مهندسی نرم‌افزار
    # 42 |   سارا   ,   24   ,   طراح گرافیک در شرکت تبلیغاتی
    # 43 |   رضا   ,   35   ,   کارشناس شبکه و امنیت اطلاعات
    # 44 |   مینا   ,   27   ,   مدرس زبان انگلیسی
    # 45 |   حمید   ,   40   ,   مدیر فروش در یک شرکت بازرگانی
    # 46 |   ندا   ,   31   ,   نویسنده و تولیدکننده محتوا
    # 47 |   کاوه   ,   33   ,   برنامه‌نویس ارشد پایتون
    # 48 |   پریسا   ,   26   ,   دانشجوی کارشناسی ارشد مدیریت
    # 49 |   حسین   ,   38   ,   مهندس عمران با ۱۰ سال سابقه
    # 50 |   فاطمه   ,   22   ,   دانشجوی رشته پزشکی
    # 51 |   نوید   ,   30   ,   توسعه‌دهنده وب
    # 52 |   لیلا   ,   28   ,   کارشناس منابع انسانی
    # 53 |   حامد   ,   34   ,   متخصص امنیت سایبری
    # 54 |   زهرا   ,   25   ,   دانشجوی زیست‌شناسی
    # 55 |   سینا   ,   36   ,   مهندس مکانیک در شرکت خودروسازی
    # 56 |   شیرین   ,   29   ,   مترجم و ویراستار متون
    # 57 |   محمد   ,   41   ,   معلم دبیرستان
    # 58 |   مهسا   ,   23   ,   دانشجوی هنرهای تجسمی
    # 59 |   امید   ,   39   ,   مهندس راه و ساختمان
    # 60 |   نگار   ,   27   ,   پرستار بیمارستان خصوصی
    # 61 |   احسان   ,   42   ,   مشاور مالی
    # 62 |   رویا   ,   25   ,   مدیر شبکه‌های اجتماعی
    # 63 |   کیان   ,   37   ,   سرآشپز رستوران ایتالیایی
    # 64 |   تارا   ,   24   ,   مدل لباس و بازیگر تازه‌کار
    # 65 |   فرهاد   ,   32   ,   تعمیرکار برق صنعتی
    # 66 |   نازنین   ,   26   ,   معمار داخلی
    # 67 |   امیر   ,   30   ,   مشاور کسب‌وکار
    # 68 |   مریم   ,   28   ,   پزشک عمومی
    # 69 |   آرمین   ,   23   ,   توسعه‌دهنده بازی‌های ویدیویی
    # 70 |   الهام   ,   35   ,   کارشناس منابع انسانی
    # 71 |   سحر   ,   29   ,   مترجم زبان انگلیسی
    # 72 |   پویا   ,   33   ,   برنامه‌نویس موبایل
    # 73 |   آرزو   ,   31   ,   پژوهشگر دانشگاهی
    # 74 |   رامین   ,   34   ,   تحلیل‌گر اقتصادی
    # 75 |   یاسمین   ,   22   ,   دانشجوی رشته حقوق
    # 76 |   بابک   ,   44   ,   خلبان خطوط هوایی
    # 77 |   شهرام   ,   38   ,   طراح صنعتی
    # 78 |   هانیه   ,   27   ,   روان‌شناس بالینی
    # 79 |   بهنام   ,   25   ,   عکاس و تدوین‌گر فیلم
    # 80 |   پگاه   ,   28   ,   توسعه‌دهنده وب‌سایت
    # ─────────────────────────────── Tests ───────────────────────────────
   
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
    def test_get_many(self):
        pass
    

    def test_view_one(self):
        pass


    def test_view_many(self):
        pass
    

    def test_add(self):
        pass


    def test_update(self):
        pass


    def test_delete(self):
        pass
            

    def test_remove(self):
        pass
            

    def test_clear(self):
        pass

