"""
Interactive module for MechSolver
Handles user interaction and input validation
"""
import sys
from typing import Any, Dict, Optional, Union, Callable
import numpy as np

def clear_screen() -> None:
    """Clear the console screen"""
    print("\033[H\033[J", end="")

def get_float_input(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """Get validated float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be greater than {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be less than {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def get_choice(options: Dict[str, str], prompt: str = "Enter your choice: ") -> str:
    """Get user choice from a dictionary of options"""
    while True:
        print("\nAvailable options:")
        for key, desc in options.items():
            print(f"{key}: {desc}")
        choice = input(prompt).strip().upper()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")

def get_yes_no(prompt: str) -> bool:
    """Get yes/no input from user"""
    while True:
        choice = input(f"{prompt} (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def print_results(results: Dict[str, Any], title: str = "Results") -> None:
    """Print results in a formatted way"""
    print(f"\n{title}")
    print("=" * len(title))
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.4g}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

def show_main_menu() -> str:
    """Show main menu and get user choice"""
    options = {
        "1": "Kinematics and Dynamics",
        "2": "Stress Analysis and Material Science",
        "3": "Thermodynamics",
        "4": "Fluid Mechanics",
        "5": "Machine Design",
        "6": "Engineering Mathematics",
        "Q": "Quit"
    }
    clear_screen()
    print("=" * 40)
    print("MechSolver - Engineering Calculator")
    print("=" * 40)
    return get_choice(options)

def show_kinematics_menu() -> str:
    """Show kinematics submenu"""
    options = {
        "1": "Projectile Motion",
        "2": "Angular Motion",
        "3": "Simple Harmonic Motion",
        "4": "Gear Train Analysis",
        "5": "Four-bar Mechanism",
        "B": "Back to Main Menu"
    }
    return get_choice(options)

def show_stress_menu() -> str:
    """Show stress analysis submenu"""
    options = {
        "1": "Normal Stress and Strain",
        "2": "Beam Analysis",
        "3": "Torsion",
        "4": "Combined Loading",
        "5": "Mohr's Circle",
        "6": "Material Selection",
        "B": "Back to Main Menu"
    }
    return get_choice(options)

def show_thermo_menu() -> str:
    """Show thermodynamics submenu"""
    options = {
        "1": "Gas Laws",
        "2": "Thermodynamic Cycles",
        "3": "Heat Transfer",
        "4": "Steam Properties",
        "5": "Psychrometrics",
        "B": "Back to Main Menu"
    }
    return get_choice(options)

def show_fluid_menu() -> str:
    """Show fluid mechanics submenu"""
    options = {
        "1": "Pipe Flow",
        "2": "Pump Selection",
        "3": "Drag Force",
        "4": "Lift Calculation",
        "5": "Flow Measurement",
        "B": "Back to Main Menu"
    }
    return get_choice(options)

def handle_error(func: Callable) -> Callable:
    """Decorator for error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Error: Invalid input - {str(e)}")
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return None
    return wrapper
