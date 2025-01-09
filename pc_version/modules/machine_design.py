"""
Machine Design Module - Handles calculations for mechanical components
"""
import math
from typing import Dict, Union, Optional

def gear_design(
    power: float,
    speed: float,
    gear_ratio: float,
    pressure_angle: float = 20,
    quality_grade: int = 7,
    material_strength: float = 300  # MPa
) -> Dict[str, float]:
    """Calculate gear parameters for spur gears"""
    # Convert power to watts
    power_watts = power * 1000
    
    # Calculate torque
    torque = (power_watts * 60) / (2 * math.pi * speed)
    
    # Lewis form factor (approximate)
    y = 0.484 - (2.87 / 20)  # assume 20 teeth minimum
    
    # Basic size calculations
    module = math.pow((2 * torque * quality_grade) / 
                     (material_strength * y * math.pi), 1/3)
    
    # Round module to standard value
    std_modules = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50]
    module = min(std_modules, key=lambda x: abs(x - module))
    
    # Calculate pitch diameters
    z1 = 20  # minimum teeth for pinion
    z2 = int(z1 * gear_ratio)
    d1 = module * z1
    d2 = module * z2
    
    # Calculate pitch line velocity
    v = (math.pi * d1 * speed) / 60000  # m/s
    
    # Calculate tangential force
    Ft = (2000 * power) / v
    
    # Calculate beam strength (Lewis equation)
    Sb = material_strength * module * 10 * y
    
    # Calculate wear strength (Buckingham equation)
    Q = 2 * gear_ratio / (gear_ratio + 1)  # load sharing ratio
    b = 10 * module  # face width
    Sw = b * Q * material_strength * d1 / 2000
    
    return {
        "module": module,
        "pinion_teeth": z1,
        "gear_teeth": z2,
        "pinion_diameter": d1,
        "gear_diameter": d2,
        "center_distance": (d1 + d2) / 2,
        "face_width": b,
        "pitch_line_velocity": v,
        "tangential_force": Ft,
        "beam_strength": Sb,
        "wear_strength": Sw,
        "power_rating": min(Sb, Sw) * v / 1000  # kW
    }

def shaft_design(
    torque: float,
    bending_moment: float,
    material_yield_strength: float,
    fatigue_strength: Optional[float] = None,
    safety_factor: float = 2.0,
    stress_concentration_factor: float = 1.5
) -> Dict[str, float]:
    """Calculate shaft parameters considering combined loading"""
    if fatigue_strength is None:
        fatigue_strength = 0.5 * material_yield_strength
    
    # Convert strengths to Pa
    Sy = material_yield_strength * 1e6
    Sf = fatigue_strength * 1e6
    
    # Calculate equivalent moment (ASME code)
    Me = math.sqrt((stress_concentration_factor * bending_moment)**2 + 
                  (0.75 * (stress_concentration_factor * torque)**2))
    
    # Calculate required diameter for static loading
    d_static = math.pow((16 * safety_factor * Me) / (math.pi * Sy), 1/3)
    
    # Calculate required diameter for fatigue loading
    d_fatigue = math.pow((16 * safety_factor * Me) / (math.pi * Sf), 1/3)
    
    # Select larger diameter
    diameter = max(d_static, d_fatigue)
    
    # Round up to nearest standard size (mm)
    std_sizes = [10, 12, 15, 17, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100]
    diameter_mm = diameter * 1000
    actual_diameter = min(size for size in std_sizes if size >= diameter_mm) / 1000
    
    # Calculate actual stresses
    actual_stress = (32 * Me) / (math.pi * actual_diameter**3)
    safety_margin = min(Sy, Sf) / actual_stress
    
    return {
        "required_diameter": diameter,
        "actual_diameter": actual_diameter,
        "equivalent_moment": Me,
        "maximum_stress": actual_stress / 1e6,  # Convert to MPa
        "actual_safety_factor": safety_margin
    }

def belt_design(
    power: float,
    speed_driver: float,
    speed_driven: float,
    center_distance: float,
    belt_type: str = "V"
) -> Dict[str, float]:
    """Calculate belt drive parameters"""
    # Calculate speed ratio
    ratio = speed_driver / speed_driven
    
    # Power correction factors
    service_factor = 1.2  # for normal duty
    design_power = power * service_factor
    
    # Estimate pulley diameters
    d1 = math.sqrt(power * 1000 / speed_driver) * 0.03
    d2 = d1 * ratio
    
    # Round to standard sizes (mm)
    std_sizes = [63, 71, 80, 90, 100, 112, 125, 140, 160, 180, 200, 224, 250, 280, 315]
    d1 = min(std_sizes, key=lambda x: abs(x - d1*1000)) / 1000
    d2 = min(std_sizes, key=lambda x: abs(x - d2*1000)) / 1000
    
    # Calculate belt length
    belt_length = 2 * center_distance + math.pi * (d1 + d2) / 2 + \
                 ((d2 - d1)**2) / (4 * center_distance)
    
    # Calculate belt velocity
    v = math.pi * d1 * speed_driver / 60
    
    # Calculate wrap angles
    alpha1 = math.pi - 2 * math.asin((d2 - d1) / (2 * center_distance))
    alpha2 = math.pi + 2 * math.asin((d2 - d1) / (2 * center_distance))
    
    # Tension ratios (approximate)
    if belt_type == "V":
        mu = 0.35  # coefficient of friction
        beta = 34 * math.pi / 180  # groove angle
        tension_ratio = math.exp(mu * alpha1 / math.sin(beta/2))
    else:  # Flat belt
        mu = 0.30
        tension_ratio = math.exp(mu * alpha1)
    
    # Calculate tensions
    power_per_belt = power * 1000  # Convert to watts
    t1 = power_per_belt / v  # Tight side tension
    t2 = t1 / tension_ratio  # Slack side tension
    
    return {
        "driver_diameter": d1,
        "driven_diameter": d2,
        "belt_length": belt_length,
        "belt_speed": v,
        "wrap_angle_driver": alpha1 * 180/math.pi,
        "wrap_angle_driven": alpha2 * 180/math.pi,
        "tight_side_tension": t1,
        "slack_side_tension": t2,
        "power_per_belt": power_per_belt/1000,  # back to kW
        "number_of_belts_required": math.ceil(design_power / (power_per_belt/1000))
    }

def bearing_life(
    load: float,
    speed: float,
    dynamic_capacity: float,
    reliability: float = 0.90,
    application: str = "ball"
) -> Dict[str, float]:
    """Calculate bearing life using modified rating life equation"""
    # Life modification factors
    a1 = {0.90: 1.00, 0.95: 0.62, 0.99: 0.21}  # reliability factor
    a2 = 1.0  # material factor
    a3 = 1.0  # operating conditions factor
    
    # Load-life exponent
    p = 3.0 if application == "ball" else 10/3  # ball or roller bearing
    
    # Basic rating life
    l10 = (dynamic_capacity / load) ** p
    
    # Modified rating life
    lna = a1[reliability] * a2 * a3 * l10
    
    # Life in hours
    life_hours = (1e6 / (60 * speed)) * lna
    
    # Dynamic equivalent load
    # Assuming purely radial load for simplicity
    p_eq = load
    
    return {
        "basic_rating_life": l10,
        "modified_rating_life": lna,
        "life_hours": life_hours,
        "dynamic_equivalent_load": p_eq,
        "reliability_factor": a1[reliability]
    }

def spring_design(
    load: float,
    deflection: float,
    wire_diameter: float,
    material_modulus: float = 79.3e9,  # G for steel
    material_strength: float = 1200e6,  # Ultimate tensile strength
    safety_factor: float = 1.5
) -> Dict[str, float]:
    """Design helical compression spring"""
    # Spring index (C = D/d), typically between 4 and 12
    C = 6  # chosen for moderate stress and good stability
    
    # Mean coil diameter
    D = C * wire_diameter
    
    # Required spring rate
    k = load / deflection
    
    # Number of active coils
    Na = (material_modulus * wire_diameter**4) / (8 * D**3 * k)
    
    # Total number of coils (adding inactive coils)
    Nt = Na + 2
    
    # Free length (assuming squared and ground ends)
    free_length = (Nt * wire_diameter) + (1.15 * deflection)
    
    # Solid length
    solid_length = Nt * wire_diameter
    
    # Spring index correction factor
    Ks = (4*C - 1)/(4*C - 4) + 0.615/C
    
    # Maximum shear stress
    tau_max = (Ks * 8 * load * D) / (math.pi * wire_diameter**3)
    
    # Buckling check
    critical_length = 2.63 * D
    
    return {
        "mean_coil_diameter": D,
        "spring_index": C,
        "active_coils": Na,
        "total_coils": Nt,
        "free_length": free_length,
        "solid_length": solid_length,
        "spring_rate": k,
        "max_shear_stress": tau_max,
        "stress_safety_factor": material_strength / (safety_factor * tau_max),
        "buckling_slenderness": free_length / D,
        "critical_slenderness": critical_length / D
    }

def power_screw_design(
    axial_load: float,
    mean_diameter: float,
    pitch: float,
    coefficient_friction: float = 0.15,
    collar_friction: float = 0.12,
    collar_mean_diameter: Optional[float] = None
) -> Dict[str, float]:
    """Calculate power screw parameters"""
    if collar_mean_diameter is None:
        collar_mean_diameter = 1.5 * mean_diameter
    
    # Thread angle (standard)
    alpha = 29 * math.pi / 180  # 29° for Acme threads
    
    # Lead angle
    lead_angle = math.atan(pitch / (math.pi * mean_diameter))
    
    # Modified friction coefficient
    f_prime = coefficient_friction / math.cos(alpha/2)
    
    # Torque to raise load
    torque_screw = (axial_load * mean_diameter / 2) * \
                   (math.tan(lead_angle) + f_prime) / \
                   (1 - f_prime * math.tan(lead_angle))
    
    # Collar torque
    torque_collar = (axial_load * collar_friction * collar_mean_diameter / 2)
    
    # Total torque
    torque_total = torque_screw + torque_collar
    
    # Efficiency
    efficiency = (axial_load * pitch) / (2 * math.pi * torque_total)
    
    # Self-locking check
    self_locking = f_prime > math.tan(lead_angle)
    
    return {
        "raising_torque": torque_total,
        "lowering_torque": torque_total if not self_locking else 0,
        "efficiency": efficiency * 100,  # as percentage
        "lead_angle_degrees": lead_angle * 180/math.pi,
        "self_locking": self_locking,
        "screw_torque": torque_screw,
        "collar_torque": torque_collar
    }
