#!/usr/bin/env python3
"""
MechSolver - Termux Version
A lightweight mechanical engineering calculator optimized for mobile devices
"""
import sys
import math
from typing import Dict, Any, Optional
from modules import (
    kinematics,
    stress_analysis,
    fluid_mechanics,
    thermodynamics,
    machine_design,
    materials
)

def clear_screen():
    """Clear the console screen"""
    print('\n' * 50)

def print_header():
    """Print a fancy header"""
    print("=" * 50)
    print("  MechSolver - Termux Edition  ")
    print("=" * 50)

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
    """Get validated choice from user"""
    while True:
        try:
            print("\nAvailable options:")
            for key, desc in options.items():
                print(f"{key}: {desc}")
            choice = input(prompt).strip().upper()
            if choice in options:
                return choice
            print("Invalid choice, please try again")
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting MechSolver...")
            sys.exit(0)

def main():
    """Main program loop"""
    try:
        modules = {
            "1": "Kinematics",
            "2": "Stress Analysis",
            "3": "Fluid Mechanics",
            "4": "Thermodynamics",
            "5": "Machine Design",
            "6": "Materials Engineering",
            "Q": "Quit"
        }
        
        calculators = {
            "1": kinematics.calculator,
            "2": stress_analysis.calculator,
            "3": fluid_mechanics.calculator,
            "4": thermodynamics.calculator,
            "5": machine_design.calculator,
            "6": materials.calculator
        }
        
        while True:
            try:
                clear_screen()
                print_header()
                
                choice = get_choice(modules, "\nSelect calculation type: ")
                if choice == "Q":
                    print("\nThank you for using MechSolver!")
                    sys.exit(0)
                    
                calculator = calculators.get(choice)
                if calculator:
                    clear_screen()
                    try:
                        calculator()
                    except Exception as e:
                        print(f"\nError: {str(e)}")
                        input("\nPress Enter to continue...")
                else:
                    print("\nThis feature is not yet implemented.")
                    input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                print("\n\nExiting MechSolver...")
                sys.exit(0)
    except Exception as e:
        print(f"\nFatal Error: {str(e)}")
        print("Please report this issue to the developers.")
        sys.exit(1)

def show_about():
    """Show information about the program"""
    clear_screen()
    print_header()
    print("\nMechSolver is a comprehensive mechanical engineering")
    print("calculator designed specifically for Termux/Android.")
    print("\nFeatures:")
    print("- Mobile-optimized interface")
    print("- Fast, lightweight calculations")
    print("- Six engineering modules")
    print("- Works completely offline")
    print("\nVersion: 1.0.0")
    print("Made with  by the MechSolver Team")
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--about":
            show_about()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nThank you for using MechSolver! ")
        sys.exit(0)
