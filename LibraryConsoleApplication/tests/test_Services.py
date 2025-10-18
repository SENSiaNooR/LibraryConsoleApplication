# -*- coding: utf-8 -*-
from Exceptions.Exceptions import InappropriateRoleError, ReachedToRequestLimitError
from Models.Models import PlainUserModel
from Services.AdminServices import AdminServices
from Services.LibrarianServices import LibrarianServices
from Services.AuthServices import AuthServices
from Services.GuestServices import GuestServices
from Services.MemberServices import MemberServices
import unittest


class TestServices(unittest.TestCase):

    def test_login(self):
        plain_user = PlainUserModel(username = 'ahmadmanafi', password = '11mm33nn55')
        login_result = AuthServices.login(plain_user)
        member_service = MemberServices(login_result.token)
        print(member_service.my_info().encode('utf-8'))
        
    def test_guest_services(self):
        token = AuthServices.login_as_guest()
        service_provider = GuestServices(token)

        for i in range(20):
            service_provider.get_all_books()
            
        with self.assertRaises(ReachedToRequestLimitError):
            service_provider.get_all_books()
            

        plain_user = PlainUserModel(username = 'ahmadmanafi', password = '11mm33nn55')
        login_res = AuthServices.login(plain_user) 
        with self.assertRaises(InappropriateRoleError):
            service_provider = GuestServices(login_res.token)
            
        with self.assertRaises(InappropriateRoleError):
            service_provider = LibrarianServices(login_res.token)

        with self.assertRaises(InappropriateRoleError):
            service_provider = AdminServices(login_res.token)
            
        service_provider = MemberServices(login_res.token)
        

        plain_user = PlainUserModel(username = 'librarian3', password = 'qazwsxedc')
        login_res = AuthServices.login(plain_user)
        service_provider = LibrarianServices(login_res.token)

    def test_guest_services_case2(self):
        token = AuthServices.login_as_guest()
        service_provider = GuestServices(token)
        a = service_provider.book_advance_search(title='ر',categories=['رمان', 'حماسی', 'زنانه'])
        
        

        
        

        
