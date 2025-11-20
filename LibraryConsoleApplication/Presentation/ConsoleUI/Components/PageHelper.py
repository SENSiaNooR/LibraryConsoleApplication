from Presentation.ConsoleUI.Components.Page import Page


class PageHelper:
    @staticmethod
    def table_prev_func(page : Page, table_data_bag_key : str, table_page_bag_key : str, max_rows_per_page : int):
        table_page = page.bag_get(table_page_bag_key, 1)
            
        if table_page <= 1:
            return
            
        page.bag_set(table_page_bag_key, table_page - 1)

    @staticmethod
    def table_next_func(page : Page, table_data_bag_key : str, table_page_bag_key : str, max_rows_per_page : int):
        table_page = page.bag_get(table_page_bag_key, 1)

        start_row = table_page * max_rows_per_page
        if start_row >= len(page.bag_get(table_data_bag_key)):
            return

        page.bag_set(table_page_bag_key, table_page + 1)
