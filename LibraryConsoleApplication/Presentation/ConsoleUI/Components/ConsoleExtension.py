
import os
import platform
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition

optimize_for_farsi_flag = False

class ConsoleExtension:
    
    class BoxChars:
        HORIZONTAL = '─'
        VERTICAL = '│'
        TOP_LEFT = '┌'
        TOP_DIVIDER = '┬'
        TOP_RIGHT = '┐'
        LEFT_DIVIDER = '├'
        RIGHT_DIVIDER = '┤'
        BOTTOM_LEFT = '└'
        BOTTOM_DIVIDER = '┴'
        BOTTOM_RIGHT = '┘'
        DIVIDER = '┼'
        
    class BoxCharsHeavy:
        HORIZONTAL = '━'
        VERTICAL = '┃'
        TOP_LEFT = '┏'
        TOP_DIVIDER = '┳'
        TOP_RIGHT = '┓'
        LEFT_DIVIDER = '┡'
        RIGHT_DIVIDER = '┩'
        BOTTOM_LEFT = '┗'
        BOTTOM_DIVIDER = '┻'
        BOTTOM_RIGHT = '┛'
        DIVIDER = '╇'
        

    class Colors:
        OK = '\033[92m'
        DEFAULT_VALUE = '\033[90m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        FOCUSED = '\033[94m'
        UNFOCUSED = '\033[0m'
        RESET = '\033[0m'

    @staticmethod
    def set_cursor(top : int, left : int):
        print("\033[%d;%dH" % (top + 1, left + 1), end='')
        
    @staticmethod
    def clear_console():
        """Clears the console screen (cross-platform)."""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
            
    @staticmethod
    def clear_area(position : SizeAndPosition):
        ConsoleExtension.reset_color()
        for i in range(position.height):
            ConsoleExtension.set_cursor(position.top + i, position.left)
            print(' ' * position.width, end='')
            
    @staticmethod
    def clear_area(area_position : SizeAndPosition, page_position : SizeAndPosition):
        ConsoleExtension.reset_color()
        for i in range(area_position.height):
            ConsoleExtension.set_cursor(page_position.top + area_position.top + i, page_position.left + area_position.left)
            print(' ' * area_position.width, end='')
            
    
    @classmethod
    def reset_color(cls):
        print(cls.Colors.RESET, end='')
        
    @classmethod
    def set_color_ok(cls):
        cls.reset_color()
        print(cls.Colors.OK, end='')
        
    @classmethod
    def set_color_default_value(cls):
        cls.reset_color()
        print(cls.Colors.DEFAULT_VALUE, end='')

    @classmethod
    def set_color_warning(cls):
        cls.reset_color()
        print(cls.Colors.WARNING, end='')
        
    @classmethod
    def set_color_fail(cls):
        cls.reset_color()
        print(cls.Colors.FAIL, end='')
        
    @classmethod
    def set_color_focused(cls):
        cls.reset_color()
        print(cls.Colors.FOCUSED, end='')
        
    @classmethod
    def set_color_unfocused(cls):
        cls.reset_color()
        print(cls.Colors.UNFOCUSED, end='')
        
    @classmethod
    def hide_cursor(cls):
        print('\033[?25l')
        
    @classmethod
    def show_cursor(cls):
        print('\033[?25h')

    @classmethod
    def optimize_for_farsi(cls, txt):
        if optimize_for_farsi_flag:
            return txt
        if any('\u0600' <= c <= '\u06FF' for c in txt):
                return get_display(reshape(txt))
        return txt
    
    @staticmethod
    def short_text(text: str, n: int) -> str:
        if text is None:
            text = ''
        if len(text.splitlines()) > 1:
            first_line = text.splitlines()[0]
        else:
            first_line = text
        return first_line if len(first_line) <= n else first_line[:n - 3] + "..."
    
    @staticmethod
    def wrap_text(text: str, max_lines: int, max_chars_per_line: int):
        original_lines = text.split("\n")  # حفظ خطوط اصلی
        wrapped_lines = []

        for line in original_lines:
            words = line.split()
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
                    current_line += (" " if current_line else "") + word
                else:
                    wrapped_lines.append(current_line)
                    current_line = word

                    if len(wrapped_lines) == max_lines:
                        wrapped_lines[-1] = wrapped_lines[-1][:max_chars_per_line - 3] + "..."
                        return "\n".join(wrapped_lines)

            # آخرین خط این بخش
            if current_line:
                wrapped_lines.append(current_line)
                if len(wrapped_lines) == max_lines and (len(words) > 0 or len(original_lines) > 1):
                    # یعنی متن ادامه داشته
                    wrapped_lines[-1] = wrapped_lines[-1][:max_chars_per_line - 3] + "..."
                    return "\n".join(wrapped_lines)

        return "\n".join(wrapped_lines)

    @staticmethod
    def print_table(
        top_offset: int,
        left_offset: int,
        cols_lens: list[int],
        rows_lens: list[int],
        first_row_as_titles: bool = True
    ):
        """
        Draws a box-style table in the console using box-drawing characters.

        Args:
            top_offset: Top margin in console
            left_offset: Left margin in console
            cols_lens: Widths of columns
            rows_lens: Heights of each row
            first_row_as_titles: If True, the first row uses heavy top borders
        """

        row_pos = 0  # Current top line offset within table

        for row_idx, row_height in enumerate(rows_lens):
            # Determine which box char set to use
            if row_idx == 0 and first_row_as_titles:
                chars = ConsoleExtension.BoxCharsHeavy()
            else:
                chars = ConsoleExtension.BoxChars()

            # ---- Draw Top Border (first line of current row block) ----
            if row_idx == 0:    
                ConsoleExtension.set_cursor(top_offset + row_pos, left_offset)
                left, right = chars.TOP_LEFT, chars.TOP_RIGHT
                middle = chars.TOP_DIVIDER

                print(left, end='')
                for col_idx, col_width in enumerate(cols_lens):
                    print(chars.HORIZONTAL * col_width, end='')
                    if col_idx < len(cols_lens) - 1:
                        print(middle, end='')
                print(right, end='')

            # ---- Draw Row Body (vertical lines) ----
            for i in range(1, row_height + 1):
                row_y = top_offset + row_pos + i
                ConsoleExtension.set_cursor(row_y, left_offset)
                print(chars.VERTICAL, end='')
                col_x = left_offset + 1
                for col_width in cols_lens:
                    col_x += col_width + 1
                    ConsoleExtension.set_cursor(row_y, col_x - 1)
                    print(chars.VERTICAL, end='')

            row_pos += row_height + 1

            # ---- Draw Bottom Border (after last row only) ----
            is_last = (row_idx == len(rows_lens) - 1)
            ConsoleExtension.set_cursor(top_offset + row_pos, left_offset)

            if is_last:
                left, right = chars.BOTTOM_LEFT, chars.BOTTOM_RIGHT
                middle = chars.BOTTOM_DIVIDER
            else:
                left, right = chars.LEFT_DIVIDER, chars.RIGHT_DIVIDER
                middle = chars.DIVIDER

            print(left, end='')
            for col_idx, col_width in enumerate(cols_lens):
                print(chars.HORIZONTAL * col_width, end='')
                if col_idx < len(cols_lens) - 1:
                    print(middle, end='')
            print(right, end='') 
                

if __name__ == '__main__':
    

    ConsoleExtension.set_cursor(1,10)
    ConsoleExtension.set_color_unfocused()
    print('hello')