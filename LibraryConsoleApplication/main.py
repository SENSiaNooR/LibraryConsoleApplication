from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.ConsoleApp import ConsoleApp

if __name__ == '__main__':
    ConsoleExtension.hide_cursor()  
    app = ConsoleApp()
    app.run()