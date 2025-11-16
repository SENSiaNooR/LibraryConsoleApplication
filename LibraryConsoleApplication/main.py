import argparse
from Presentation.ConsoleUI.Components import ConsoleExtension
from Presentation.ConsoleUI.ConsoleApp import ConsoleApp

def args_manage():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--farsi",
        action="store_true",
    )

    args = parser.parse_args()
    ConsoleExtension.optimize_for_farsi_flag = args.farsi

if __name__ == '__main__':
    args_manage()
    ConsoleExtension.ConsoleExtension.hide_cursor()  
    app = ConsoleApp()
    app.run()