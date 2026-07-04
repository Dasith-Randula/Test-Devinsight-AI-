# test_app.py - DevInsight Test File (Fixed Version)
# මේකේ හිතාමතා errors තියෙනවා (Indentation හරියට)

import os          # Unused import (W0611)
import sys         # Unused import (W0611)

def calculate_area(radius):
    """Circle එකේ area එක ගණනය කරනවා"""
    area = 3.14 * radius * radius
    return area

def main():
    # ERROR 1: 'name' කියන variable එක define කරලා නැහැ (E0602: Undefined variable)
    print("Hello, " + name)
    
    # ERROR 2: Indentation දැන් හරි - ඒත් 'value' variable එක define කරලා නැහැ (E0601)
    value = 10
    value += 5
    print(f"Value is: {value}")

if __name__ == "__main__":
    main()