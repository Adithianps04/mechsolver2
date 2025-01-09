"""
Fluid Mechanics Module - Termux Version
Lightweight implementation of fluid mechanics calculations
"""
import math
from typing import Dict, Union, Optional

def reynolds_number(velocity: float, characteristic_length: float, kinematic_viscosity: float) -> float:
    """Calculate Reynolds number"""
    return (velocity * characteristic_length) / kinematic_viscosity

def bernoulli_equation(
    height1: float,
    velocity1: float,
    pressure1: float,
    height2: float,
    velocity2: Optional[float] = None,
    pressure2: Optional[float] = None,
    density: float = 1000.0  # default to water density
) -> Dict[str, float]:
    """Calculate unknown parameter in Bernoulli's equation"""
    g = 9.81  # acceleration due to gravity
    
    if velocity2 is None:
        # p1 + ρgh1 + ½ρv1² = p2 + ρgh2 + ½ρv2²
        term1 = pressure1 + density * g * height1 + 0.5 * density * velocity1**2
        term2 = pressure2 + density * g * height2
        velocity2 = math.sqrt(2 * (term1 - term2) / density)
        return {"velocity2": velocity2}
        
    elif pressure2 is None:
        pressure2 = pressure1 + density * g * (height1 - height2) + \
                   0.5 * density * (velocity1**2 - velocity2**2)
        return {"pressure2": pressure2}
    
    return {}

def head_loss(
    length: float,
    diameter: float,
    velocity: float,
    friction_factor: float,
    minor_loss_coefficient: float = 0
) -> float:
    """Calculate head loss in a pipe"""
    g = 9.81
    # Major losses (Darcy-Weisbach equation)
    major_loss = friction_factor * (length / diameter) * (velocity**2 / (2 * g))
    # Minor losses
    minor_loss = minor_loss_coefficient * (velocity**2 / (2 * g))
    return major_loss + minor_loss

def flow_rate(velocity: float, area: float) -> float:
    """Calculate volumetric flow rate"""
    return velocity * area

def pressure_drop(
    length: float,
    diameter: float,
    velocity: float,
    density: float,
    viscosity: float
) -> float:
    """Calculate pressure drop in a pipe using Darcy-Weisbach"""
    # Calculate Reynolds number
    re = reynolds_number(velocity, diameter, viscosity/density)
    
    # Estimate friction factor (Blasius equation for turbulent flow)
    if re < 2300:
        f = 64/re  # Laminar flow
    else:
        f = 0.316 * re**(-0.25)  # Turbulent flow (Blasius equation)
    
    # Calculate pressure drop
    return f * (length/diameter) * (density * velocity**2) / 2

def calculator():
    """Interactive fluid mechanics calculator"""
    while True:
        print("\n=== Fluid Mechanics Calculator ===")
        print("1: Reynolds Number")
        print("2: Bernoulli's Equation")
        print("3: Head Loss")
        print("4: Flow Rate")
        print("5: Pressure Drop")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            try:
                v = float(input("Velocity (m/s): "))
                l = float(input("Characteristic length (m): "))
                nu = float(input("Kinematic viscosity (m²/s): "))
                re = reynolds_number(v, l, nu)
                print(f"\nReynolds number: {re:.2f}")
                if re < 2300:
                    print("Flow is laminar")
                elif re < 4000:
                    print("Flow is transitional")
                else:
                    print("Flow is turbulent")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                h1 = float(input("Height 1 (m): "))
                v1 = float(input("Velocity 1 (m/s): "))
                p1 = float(input("Pressure 1 (Pa): "))
                h2 = float(input("Height 2 (m): "))
                
                calc_type = input("Calculate (velocity2/pressure2)? ").lower()
                if calc_type.startswith('v'):
                    p2 = float(input("Pressure 2 (Pa): "))
                    result = bernoulli_equation(h1, v1, p1, h2, pressure2=p2)
                    print(f"\nVelocity 2: {result['velocity2']:.2f} m/s")
                else:
                    v2 = float(input("Velocity 2 (m/s): "))
                    result = bernoulli_equation(h1, v1, p1, h2, v2)
                    print(f"\nPressure 2: {result['pressure2']:.2f} Pa")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            try:
                l = float(input("Pipe length (m): "))
                d = float(input("Pipe diameter (m): "))
                v = float(input("Flow velocity (m/s): "))
                f = float(input("Friction factor: "))
                k = float(input("Minor loss coefficient (0 if none): "))
                
                loss = head_loss(l, d, v, f, k)
                print(f"\nTotal head loss: {loss:.2f} m")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            try:
                v = float(input("Velocity (m/s): "))
                a = float(input("Cross-sectional area (m²): "))
                q = flow_rate(v, a)
                print(f"\nFlow rate: {q:.2f} m³/s")
                print(f"         : {q * 3600:.2f} m³/h")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            try:
                l = float(input("Pipe length (m): "))
                d = float(input("Pipe diameter (m): "))
                v = float(input("Flow velocity (m/s): "))
                rho = float(input("Fluid density (kg/m³): "))
                mu = float(input("Dynamic viscosity (Pa·s): "))
                
                dp = pressure_drop(l, d, v, rho, mu)
                print(f"\nPressure drop: {dp:.2f} Pa")
                print(f"             : {dp/1000:.4f} kPa")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
