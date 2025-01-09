"""
Kinematics Module - Termux Version
Lightweight implementation of kinematics calculations
"""
import math
from typing import Dict, Union, Optional

def linear_motion(
    initial_velocity: float,
    final_velocity: Optional[float] = None,
    acceleration: Optional[float] = None,
    time: Optional[float] = None,
    displacement: Optional[float] = None
) -> Dict[str, float]:
    """Calculate linear motion parameters using basic equations"""
    results = {}
    
    # v = u + at
    if final_velocity is None and acceleration is not None and time is not None:
        final_velocity = initial_velocity + acceleration * time
        results["final_velocity"] = final_velocity
    
    # s = ut + (1/2)at²
    if displacement is None and acceleration is not None and time is not None:
        displacement = initial_velocity * time + 0.5 * acceleration * time * time
        results["displacement"] = displacement
    
    # v² = u² + 2as
    if final_velocity is None and acceleration is not None and displacement is not None:
        final_velocity = math.sqrt(initial_velocity**2 + 2 * acceleration * displacement)
        results["final_velocity"] = final_velocity
    
    return results

def angular_motion(
    initial_angular_velocity: float,
    final_angular_velocity: Optional[float] = None,
    angular_acceleration: Optional[float] = None,
    time: Optional[float] = None,
    angular_displacement: Optional[float] = None
) -> Dict[str, float]:
    """Calculate angular motion parameters"""
    results = {}
    
    # ω = ω₀ + αt
    if final_angular_velocity is None and angular_acceleration is not None and time is not None:
        final_angular_velocity = initial_angular_velocity + angular_acceleration * time
        results["final_angular_velocity"] = final_angular_velocity
    
    # θ = ω₀t + (1/2)αt²
    if angular_displacement is None and angular_acceleration is not None and time is not None:
        angular_displacement = initial_angular_velocity * time + 0.5 * angular_acceleration * time * time
        results["angular_displacement"] = angular_displacement
    
    # ω² = ω₀² + 2αθ
    if final_angular_velocity is None and angular_acceleration is not None and angular_displacement is not None:
        final_angular_velocity = math.sqrt(initial_angular_velocity**2 + 2 * angular_acceleration * angular_displacement)
        results["final_angular_velocity"] = final_angular_velocity
    
    return results

def projectile_motion(
    initial_velocity: float,
    angle: float,  # in degrees
    height: float = 0
) -> Dict[str, float]:
    """Calculate projectile motion parameters"""
    g = 9.81  # acceleration due to gravity
    angle_rad = math.radians(angle)
    
    # Initial velocities
    v0x = initial_velocity * math.cos(angle_rad)
    v0y = initial_velocity * math.sin(angle_rad)
    
    # Time of flight
    if height == 0:
        time_of_flight = 2 * v0y / g
    else:
        # Quadratic equation for time with initial height
        a = -0.5 * g
        b = v0y
        c = height
        discriminant = b*b - 4*a*c
        time_of_flight = (-b + math.sqrt(discriminant)) / (2*a)
    
    # Maximum height
    max_height = height + (v0y * v0y) / (2 * g)
    
    # Range
    range_x = v0x * time_of_flight
    
    return {
        "time_of_flight": time_of_flight,
        "maximum_height": max_height,
        "range": range_x
    }

def calculator():
    """Interactive kinematics calculator"""
    while True:
        print("\n=== Kinematics Calculator ===")
        print("1: Linear Motion")
        print("2: Angular Motion")
        print("3: Projectile Motion")
        print("B: Back to Main Menu")
        
        choice = input("Select calculation: ").strip().upper()
        
        if choice == "B":
            return
            
        if choice == "1":
            print("\nLinear Motion Calculator")
            try:
                u = float(input("Initial velocity (m/s): "))
                print("\nWhat do you want to calculate?")
                print("1: Final velocity")
                print("2: Displacement")
                sub_choice = input("Choice: ")
                
                if sub_choice == "1":
                    a = float(input("Acceleration (m/s²): "))
                    t = float(input("Time (s): "))
                    result = linear_motion(u, acceleration=a, time=t)
                elif sub_choice == "2":
                    a = float(input("Acceleration (m/s²): "))
                    t = float(input("Time (s): "))
                    result = linear_motion(u, acceleration=a, time=t)
                print("\nResults:", result)
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            print("\nAngular Motion Calculator")
            try:
                w0 = float(input("Initial angular velocity (rad/s): "))
                alpha = float(input("Angular acceleration (rad/s²): "))
                t = float(input("Time (s): "))
                result = angular_motion(w0, angular_acceleration=alpha, time=t)
                print("\nResults:", result)
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            print("\nProjectile Motion Calculator")
            try:
                v0 = float(input("Initial velocity (m/s): "))
                angle = float(input("Angle with horizontal (degrees): "))
                h0 = float(input("Initial height (m, 0 if none): "))
                result = projectile_motion(v0, angle, h0)
                print("\nResults:")
                for key, value in result.items():
                    print(f"{key}: {value:.2f}")
                    
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice, please try again")
