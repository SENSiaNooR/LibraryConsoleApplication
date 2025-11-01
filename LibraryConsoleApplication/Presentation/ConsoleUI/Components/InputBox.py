import re
import time
import keyboard
from Presentation.ConsoleUI.Components.Element import Element
from typing import Callable, Dict, Optional
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition

class InputBox(Element):
    """
    A UI InputBox element that renders input box at a given position
    """
    eng_to_farsi = {
        'H':'آ','h':'ا','f':'ب','\\':'پ','j':'ت','e':'ث','[':'ج',']':'چ','p':'ح',
        'o':'خ','n':'د','b':'ذ','v':'ر','c':'ز','C':'ژ','s':'س','a':'ش','m':'ئ',
        'w':'ص','q':'ض','x':'ط','z':'ظ','u':'ع','y':'غ','t':'ف','r':'ق','M':'ء',
        ';':'ک',"'":'گ','g':'ل','l':'م','k':'ن',',':'و','i':'ه','d':'ی'
    }


    def __init__(
        self,
        display_text: str,
        checker: Callable[[str],bool] = lambda _ : True,
        position: Optional[SizeAndPosition] = None,
        linked_elements: Optional[Dict[str, Element]]= None,
        password_mode: bool = False
    ):
        super().__init__(position=position, linked_elements=linked_elements, focusable=True, clickable=True)

        if len(display_text.splitlines()) > 1:
            raise Exception('default text must be single line')
        
        self.display_text = display_text
        self.checker = checker
        self.password_mode = password_mode
        self.content = ''

        if self.position is None:
            self.position = SizeAndPosition()
            
        height = 1
        width = len(display_text) + 4
        
        self.position.height = height
        self.position.width = width
        
        self.is_farsi = False
        self.running = False
            


    def resize_to_fit(self):
        """Resize element so it just fits its contents."""
        self.position.width = len(self.display_text) + 4 if self.content == '' else len(self.content) + 4
        
    def check(self):
        return self.checker(self.content)

    def render(self, top_offset: int = 0, left_offset: int = 0):
        """
        Renders in the console at the given position.
        """  
        self.resize_to_fit()

        if self._is_focused:
            if self.running:
                if self.check():
                    ConsoleExtension.set_color_ok()
                else:
                    ConsoleExtension.set_color_fail()
            else:
                ConsoleExtension.set_color_warning()
        else:
            ConsoleExtension.reset_color()

        
        ConsoleExtension.set_cursor(self.position.top + top_offset, self.position.left + left_offset)
        print('[ ',end='')
        if self.content == '':
            #ConsoleExtension.set_color_default_value()
            txt = ConsoleExtension.optimize_for_farsi(self.display_text)
            print(txt, end='')
        else: 
            #ConsoleExtension.reset_color()
            txt = ConsoleExtension.optimize_for_farsi(self.content)
            if self.password_mode:
                print('*' * len(txt), end='')
            else:
                print(txt, end='')
         
        if self._is_focused:
            if self.running:
                if self.check():
                    ConsoleExtension.set_color_ok()
                else:
                    ConsoleExtension.set_color_fail()
            else:
                ConsoleExtension.set_color_warning()
        else:
            ConsoleExtension.reset_color()
        print(' ]',end='')
          
        ConsoleExtension.reset_color()

    def _clear(self, top_offset, left_offset):
        ConsoleExtension.set_cursor(
            top = top_offset + self.position.top,
            left = left_offset + self.position.left
        )
        ConsoleExtension.reset_color()
        print(' ' * self.position.width, end='')


    def click(self, top_offset, left_offset):
        alt_pressed = False
        shift_pressed = False
        self.running = True
        while True:
            event = keyboard.read_event(suppress=True)
            
            if event.event_type == keyboard.KEY_DOWN:
                if event.name in ['esc', 'enter']:
                    break
                
                elif event.name == 'backspace':
                    if self.content != '':
                        self.content = self.content[:-1]
                    alt_pressed = False
                    shift_pressed = False
                 
                elif event.name == 'shift':
                    shift_pressed = True

                elif event.name == 'alt':
                    alt_pressed = True

                elif len(event.name) == 1:
                    if self.is_farsi:
                        self.content += self.eng_to_farsi.get(event.name, event.name)
                    else:
                        self.content += event.name
                    alt_pressed = False
                    shift_pressed = False
                    
                elif event.name == 'space':
                    self.content += ' '
                    alt_pressed = False
                    shift_pressed = False
                    
                else:
                    alt_pressed = False
                    shift_pressed = False
                    
                if shift_pressed and alt_pressed:
                    alt_pressed = False
                    shift_pressed = False
                    
                    self.is_farsi = not self.is_farsi
                    
                    self._clear(top_offset, left_offset)
                    
                    ConsoleExtension.set_cursor(top_offset + self.position.top, left_offset + self.position.left)
                    
                    alert = 'زبان : فارسی' if self.is_farsi else 'زبان : انگلیسی'
                    print(ConsoleExtension.optimize_for_farsi(alert), end = '')
                    time.sleep(0.3)
                    
                    ConsoleExtension.set_cursor(top_offset + self.position.top, left_offset + self.position.left)
                    
                    print(' ' * len(alert), end = '')
                    
                                        
                    
            self._clear(top_offset, left_offset)
            self.render(top_offset, left_offset)
        self.running = False
        self._clear(top_offset, left_offset)
        self.render(top_offset, left_offset)


    def __repr__(self):
        return f"InputBox(display_text={self.display_text!r}, pos={self.position}, is_farsi={self.is_farsi})"