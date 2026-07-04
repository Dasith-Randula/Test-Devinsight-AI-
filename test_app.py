# test_app.py - DevInsight Test File
# මේකේ හිතාමතා errors තියෙනවා

import os          # Unused import (W0611: Unused import)
import sys         # Unused import (W0611)

def calculate_area(radius):
    """Circle එකේ area එක ගණනය කරනවා"""
    area = 3.14 * radius * radius
    return area

def main():
    # ERROR 1: 'name' කියන variable එක define කරලා නැහැ (E0602: Undefined variable)
    print("Hello, " + name)
    
    # ERROR 2: Bad indentation (E0001: Indentation error - මේක Python එකට හරින්න බැහැ)
      value = 10
    value += 5
    print(f"Value is: {value}")

if __name__ == "__main__":
    main()