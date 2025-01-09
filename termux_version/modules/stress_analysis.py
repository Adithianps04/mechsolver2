"""
Stress Analysis Module - Termux Version
Lightweight implementation of stress and strain calculations
"""
import math
from typing import Dict, Union, Optional

def normal_stress(force: float, area: float) -> float:
    """Calculate normal stress"""
    return force / area

def shear_stress(force: float, area: float) -> float:
    """Calculate shear stress"""
    return force / area

def strain(change_in_length: float, original_length: float) -> float:
    """Calculate strain"""
    return change_in_length / original_length

def elastic_modulus(stress: float, strain: float) -> float:
    """Calculate elastic modulus"""
    return stress / strain

def bending_stress(moment: float, distance: float, moment_of_inertia: float) -> float:
    """Calculate bending stress"""
    return (moment * distance) / moment_of_inertia

def torsional_stress(torque: float, radius: float, polar_moment_of_inertia: float) -> float:
    """Calculate torsional stress"""
    return (torque * radius) / polar_moment_of_inertia

def principal_stresses(sigma_x: float, sigma_y: float, tau_xy: float) -> Dict[str, float]:
    """Calculate principal stresses"""
    avg = (sigma_x + sigma_y) / 2
    diff = (sigma_x - sigma_y) / 2
    r = math.sqrt(diff * diff + tau_xy * tau_xy)
    
    sigma_1 = avg + r
    sigma_2 = avg - r
    theta = math.degrees(math.atan2(tau_xy, diff)) / 2
    
    return {
        "sigma_1": sigma_1,
        "sigma_2": sigma_2,
        "theta": theta
    }

def von_mises_stress(sigma_x: float, sigma_y: float, tau_xy: float) -> float:
    """Calculate von Mises stress"""
    return math.sqrt(sigma_x**2 - sigma_x*sigma_y + sigma_y**2 + 3*tau_xy**2)

def calculator():
    """Interactive stress analysis calculator"""
    while True:
        print("\n=== Stress Analysis Calculator ===")
        print("1: Normal/Shear Stress")
        print("2: Strain and Elastic Modulus")
        print("3: Bending Stress")
        print("4: Torsional Stress")
        print("5: Principal Stresses")
        print("6: Von Mises Stress")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            try:
                force = float(input("Force (N): "))
                area = float(input("Area (m²): "))
                stress_type = input("Calculate (normal/shear)? ").lower()
                
                if stress_type.startswith('n'):
                    result = normal_stress(force, area)
                    print(f"\nNormal stress: {result:.2f} Pa")
                else:
                    result = shear_stress(force, area)
                    print(f"\nShear stress: {result:.2f} Pa")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                delta_l = float(input("Change in length (m): "))
                l0 = float(input("Original length (m): "))
                calc_strain = strain(delta_l, l0)
                print(f"\nStrain: {calc_strain:.6f}")
                
                if input("Calculate elastic modulus (y/n)? ").lower() == 'y':
                    stress = float(input("Stress (Pa): "))
                    E = elastic_modulus(stress, calc_strain)
                    print(f"Elastic modulus: {E:.2e} Pa")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            try:
                M = float(input("Bending moment (N·m): "))
                y = float(input("Distance from neutral axis (m): "))
                I = float(input("Moment of inertia (m⁴): "))
                result = bending_stress(M, y, I)
                print(f"\nBending stress: {result:.2f} Pa")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            try:
                T = float(input("Torque (N·m): "))
                r = float(input("Radius (m): "))
                J = float(input("Polar moment of inertia (m⁴): "))
                result = torsional_stress(T, r, J)
                print(f"\nTorsional stress: {result:.2f} Pa")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            try:
                sx = float(input("σx (Pa): "))
                sy = float(input("σy (Pa): "))
                txy = float(input("τxy (Pa): "))
                result = principal_stresses(sx, sy, txy)
                print("\nPrincipal Stresses:")
                print(f"σ₁: {result['sigma_1']:.2f} Pa")
                print(f"σ₂: {result['sigma_2']:.2f} Pa")
                print(f"θp: {result['theta']:.2f}°")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "6":
            try:
                sx = float(input("σx (Pa): "))
                sy = float(input("σy (Pa): "))
                txy = float(input("τxy (Pa): "))
                result = von_mises_stress(sx, sy, txy)
                print(f"\nVon Mises stress: {result:.2f} Pa")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
