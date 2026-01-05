#!/usr/bin/env python3

from elements import *


class Page:

    def __init__(self, element: Elem() )-> None:
        self.elem = element



    def __str__(self):
        result = "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result
    


    def isValid(self):
        if not isinstance(self, Elem):
            return False
        return True
    


    def write_to_file(self, filename: str) -> None:
        try:
            with open(f"{filename}.html", "w") as file:
                file.write(str(self))
            return True
        except Exception as e:
            print(f"An error occurred while writing to file: {e}")
            return False
