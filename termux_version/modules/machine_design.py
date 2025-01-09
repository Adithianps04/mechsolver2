"""
Machine Design Module - Termux Version
Lightweight implementation of machine design calculations
"""
import math
from typing import Dict, Union, Optional

def gear_design(
    power: float,  # in kW
    speed: float,  # in rpm
    ratio: float,
    pressure_angle: float = 20,  # in degrees
    quality: int = 8
) -> Dict[str, float]:
    """Calculate basic gear parameters"""
    # Convert power to watts
    power_watts = power * 1000
    
    # Basic calculations
    pitch_diameter = math.pow((2 * power_watts * 60)/(math.pi * speed), 1/3)
    module = pitch_diameter / 20  # Assuming 20 teeth on pinion
    
    # Calculate teeth numbers
    pinion_teeth = 20
    gear_teeth = int(pinion_teeth * ratio)
    
    # Calculate pitch line velocity
    pitch_velocity = (math.pi * pitch_diameter * speed) / 60000  # in m/s
    
    # Calculate forces
    tangential_force = (power_watts * 1000) / pitch_velocity
    radial_force = tangential_force * math.tan(math.radians(pressure_angle))
    
    return {
        "module": module,
        "pinion_teeth": pinion_teeth,
        "gear_teeth": gear_teeth,
        "pitch_diameter": pitch_diameter,
        "pitch_velocity": pitch_velocity,
        "tangential_force": tangential_force,
        "radial_force": radial_force
    }

def shaft_design(
    torque: float,  # in N⋅m
    bending_moment: float,  # in N⋅m
    material_yield_strength: float,  # in MPa
    safety_factor: float = 2.0
) -> Dict[str, float]:
    """Calculate shaft diameter based on combined loading"""
    # Convert yield strength to Pa
    Sy = material_yield_strength * 1e6
    
    # Maximum shear stress theory
    tau_max = Sy / (2 * safety_factor)
    
    # Calculate equivalent torque
    Te = math.sqrt(torque**2 + bending_moment**2)
    
    # Calculate required diameter
    diameter = math.pow((16 * Te)/(math.pi * tau_max), 1/3)
    
    return {
        "diameter": diameter,
        "max_shear_stress": tau_max,
        "equivalent_torque": Te
    }

def bearing_life(
    load: float,  # in N
    speed: float,  # in rpm
    dynamic_capacity: float,  # in N
    reliability: float = 0.9
) -> Dict[str, float]:
    """Calculate bearing life"""
    # Life exponent (3 for ball bearings, 10/3 for roller bearings)
    p = 3
    
    # Basic rating life in millions of revolutions
    L10 = (dynamic_capacity/load)**p
    
    # Life in hours
    life_hours = (L10 * 1e6)/(60 * speed)
    
    # Reliability factors
    reliability_factors = {
        0.9: 1.0,
        0.95: 0.62,
        0.99: 0.21,
        0.999: 0.02
    }
    
    # Adjusted life
    adjusted_life = life_hours * reliability_factors.get(reliability, 1.0)
    
    return {
        "basic_life_revolutions": L10 * 1e6,
        "life_hours": life_hours,
        "adjusted_life_hours": adjusted_life
    }

def spring_design(
    wire_diameter: float,  # in mm
    mean_coil_diameter: float,  # in mm
    number_of_coils: int,
    material_shear_modulus: float,  # in GPa
    max_force: float  # in N
) -> Dict[str, float]:
    """Calculate spring parameters"""
    # Convert units
    d = wire_diameter / 1000  # to meters
    D = mean_coil_diameter / 1000  # to meters
    G = material_shear_modulus * 1e9  # to Pa
    
    # Spring index
    C = D/d
    
    # Wahl factor
    K = (4*C - 1)/(4*C - 4) + 0.615/C
    
    # Spring rate
    k = (G * d**4)/(8 * D**3 * number_of_coils)
    
    # Maximum deflection
    max_deflection = max_force/k
    
    # Maximum shear stress
    tau_max = K * (8 * max_force * D)/(math.pi * d**3)
    
    # Solid height
    solid_height = (number_of_coils + 2) * d
    
    return {
        "spring_index": C,
        "spring_rate": k,
        "max_deflection": max_deflection,
        "max_shear_stress": tau_max,
        "solid_height": solid_height
    }

def belt_drive(
    power: float,  # in kW
    speed_ratio: float,
    center_distance: float,  # in m
    belt_type: str = "V"  # "V" or "flat"
) -> Dict[str, float]:
    """Calculate belt drive parameters"""
    # Convert power to watts
    power_watts = power * 1000
    
    # Belt velocity (assuming reasonable pulley diameter)
    velocity = 15  # m/s (typical value)
    
    # Calculate minimum pulley diameter
    d1 = math.sqrt((power_watts * 60)/(math.pi * velocity))
    d2 = d1 * speed_ratio
    
    # Calculate belt length
    belt_length = 2 * center_distance + math.pi * (d1 + d2)/2 + (d2 - d1)**2/(4 * center_distance)
    
    # Calculate wrap angles
    theta1 = math.pi - 2 * math.asin((d2 - d1)/(2 * center_distance))
    theta2 = math.pi + 2 * math.asin((d2 - d1)/(2 * center_distance))
    
    return {
        "small_pulley_diameter": d1,
        "large_pulley_diameter": d2,
        "belt_length": belt_length,
        "wrap_angle_driver": math.degrees(theta1),
        "wrap_angle_driven": math.degrees(theta2)
    }

def calculator():
    """Interactive machine design calculator"""
    while True:
        print("\n=== Machine Design Calculator ===")
        print("1: Gear Design")
        print("2: Shaft Design")
        print("3: Bearing Life")
        print("4: Spring Design")
        print("5: Belt Drive")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            try:
                power = float(input("Enter power (kW): "))
                speed = float(input("Enter speed (rpm): "))
                ratio = float(input("Enter gear ratio: "))
                
                results = gear_design(power, speed, ratio)
                print("\nResults:")
                for key, value in results.items():
                    print(f"{key}: {value:.3f}")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                torque = float(input("Enter torque (N⋅m): "))
                moment = float(input("Enter bending moment (N⋅m): "))
                strength = float(input("Enter material yield strength (MPa): "))
                
                results = shaft_design(torque, moment, strength)
                print("\nResults:")
                print(f"Required diameter: {results['diameter']*1000:.2f} mm")
                print(f"Maximum shear stress: {results['max_shear_stress']/1e6:.2f} MPa")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            try:
                load = float(input("Enter bearing load (N): "))
                speed = float(input("Enter speed (rpm): "))
                capacity = float(input("Enter dynamic capacity (N): "))
                
                results = bearing_life(load, speed, capacity)
                print("\nResults:")
                print(f"Life (hours): {results['life_hours']:.0f}")
                print(f"Adjusted life (hours): {results['adjusted_life_hours']:.0f}")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            try:
                wire_d = float(input("Enter wire diameter (mm): "))
                coil_d = float(input("Enter mean coil diameter (mm): "))
                coils = int(input("Enter number of coils: "))
                shear_mod = float(input("Enter material shear modulus (GPa): "))
                force = float(input("Enter maximum force (N): "))
                
                results = spring_design(wire_d, coil_d, coils, shear_mod, force)
                print("\nResults:")
                print(f"Spring rate: {results['spring_rate']:.2f} N/m")
                print(f"Maximum deflection: {results['max_deflection']*1000:.2f} mm")
                print(f"Maximum shear stress: {results['max_shear_stress']/1e6:.2f} MPa")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            try:
                power = float(input("Enter power (kW): "))
                ratio = float(input("Enter speed ratio: "))
                distance = float(input("Enter center distance (m): "))
                
                results = belt_drive(power, ratio, distance)
                print("\nResults:")
                print(f"Small pulley diameter: {results['small_pulley_diameter']*1000:.2f} mm")
                print(f"Large pulley diameter: {results['large_pulley_diameter']*1000:.2f} mm")
                print(f"Belt length: {results['belt_length']*1000:.2f} mm")
                print(f"Wrap angles: {results['wrap_angle_driver']:.1f}° / {results['wrap_angle_driven']:.1f}°")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
            
        input("\nPress Enter to continue...")
