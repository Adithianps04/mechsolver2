"""
Stress Analysis Module - Handles structural mechanics calculations
"""
import numpy as np
from typing import Dict, Union, Optional, List, Tuple

def calculate_stress(force: float, area: float) -> float:
    """Calculate normal stress"""
    return force / area

def calculate_strain(stress: float, youngs_modulus: float) -> float:
    """Calculate strain using Hooke's Law"""
    return stress / youngs_modulus

def beam_bending_stress(
    moment: float,
    distance: float,
    moment_of_inertia: float
) -> float:
    """Calculate bending stress in a beam"""
    return (moment * distance) / moment_of_inertia

def beam_deflection(
    load: float,
    length: float,
    elastic_modulus: float,
    moment_of_inertia: float,
    load_type: str = 'point_center'
) -> Dict[str, float]:
    """
    Calculate beam deflection for various loading conditions
    
    Args:
        load: Applied load (N)
        length: Beam length (m)
        elastic_modulus: Young's modulus (Pa)
        moment_of_inertia: Second moment of area (m⁴)
        load_type: Type of loading ('point_center', 'point_end', 'uniform')
    """
    factors = {
        'point_center': 1/48,  # Point load at center
        'point_end': 1/3,      # Point load at end
        'uniform': 5/384       # Uniformly distributed load
    }
    
    if load_type not in factors:
        raise ValueError(f"Unsupported load type. Choose from: {list(factors.keys())}")
    
    max_deflection = factors[load_type] * load * length**3 / (elastic_modulus * moment_of_inertia)
    
    # Calculate bending moment
    if load_type == 'point_center':
        max_moment = load * length / 4
    elif load_type == 'point_end':
        max_moment = load * length
    else:  # uniform
        max_moment = load * length**2 / 8
    
    return {
        'max_deflection': max_deflection,
        'max_moment': max_moment
    }

def combined_stress(
    normal_stress: float,
    shear_stress: float
) -> Dict[str, float]:
    """Calculate principal stresses and maximum shear stress"""
    avg_normal = normal_stress / 2
    radius = np.sqrt((normal_stress/2)**2 + shear_stress**2)
    
    principal_1 = avg_normal + radius
    principal_2 = avg_normal - radius
    max_shear = radius
    
    return {
        'principal_stress_1': principal_1,
        'principal_stress_2': principal_2,
        'max_shear_stress': max_shear,
        'angle_principal': np.degrees(np.arctan2(2*shear_stress, normal_stress))/2
    }

def torsional_stress(
    torque: float,
    radius: float,
    polar_moment: float
) -> Dict[str, float]:
    """Calculate torsional stress and angle of twist"""
    shear_stress = (torque * radius) / polar_moment
    return {
        'shear_stress': shear_stress,
        'max_shear_stress': shear_stress  # At outer radius
    }

def fatigue_analysis(
    stress_max: float,
    stress_min: float,
    ultimate_strength: float,
    endurance_limit: float,
    surface_factor: float = 0.9,
    size_factor: float = 0.95,
    reliability_factor: float = 0.897  # 90% reliability
) -> Dict[str, float]:
    """
    Perform fatigue analysis using modified Goodman criterion
    
    Args:
        stress_max: Maximum stress in cycle (Pa)
        stress_min: Minimum stress in cycle (Pa)
        ultimate_strength: Ultimate tensile strength (Pa)
        endurance_limit: Material endurance limit (Pa)
        surface_factor: Surface finish factor
        size_factor: Size effect factor
        reliability_factor: Statistical reliability factor
    """
    # Calculate stress amplitude and mean
    stress_amp = (stress_max - stress_min) / 2
    stress_mean = (stress_max + stress_min) / 2
    
    # Modify endurance limit
    Se = endurance_limit * surface_factor * size_factor * reliability_factor
    
    # Calculate safety factor using Goodman criterion
    safety_factor = 1 / (stress_amp/Se + stress_mean/ultimate_strength)
    
    # Calculate cycles to failure (simplified Basquin equation)
    if safety_factor > 1:
        cycles = 1e6  # Infinite life
    else:
        b = -0.085  # Typical fatigue strength exponent
        cycles = (stress_amp / Se)**(1/b)
    
    return {
        'safety_factor': safety_factor,
        'modified_endurance_limit': Se,
        'stress_amplitude': stress_amp,
        'mean_stress': stress_mean,
        'cycles_to_failure': cycles
    }

def composite_lamina_properties(
    E1: float,  # Longitudinal modulus
    E2: float,  # Transverse modulus
    nu12: float,  # Major Poisson's ratio
    G12: float,  # Shear modulus
    theta: float  # Orientation angle in degrees
) -> Dict[str, float]:
    """
    Calculate transformed elastic properties of a composite lamina
    
    Args:
        E1: Longitudinal elastic modulus
        E2: Transverse elastic modulus
        nu12: Major Poisson's ratio
        G12: Shear modulus
        theta: Orientation angle in degrees
    """
    # Convert angle to radians
    theta_rad = np.radians(theta)
    c = np.cos(theta_rad)
    s = np.sin(theta_rad)
    
    # Calculate minor Poisson's ratio
    nu21 = nu12 * E2 / E1
    
    # Calculate transformed properties
    Ex = 1 / (c**4/E1 + s**4/E2 + (1/G12 - 2*nu12/E1)*s**2*c**2)
    Ey = 1 / (s**4/E1 + c**4/E2 + (1/G12 - 2*nu12/E1)*s**2*c**2)
    Gxy = 1 / (4*(s**2*c**2/E1 + s**2*c**2/E2 + (1/G12 - 2*nu12/E1)*(s**2-c**2)**2/4))
    nuxy = Ex * (nu12/E1*(c**4 + s**4) - (1/E1 - 1/E2 - 2*nu12/E1)*s**2*c**2)
    
    return {
        'Ex': Ex,
        'Ey': Ey,
        'Gxy': Gxy,
        'nuxy': nuxy,
        'angle': theta
    }

def pressure_vessel_stress(
    pressure: float,
    radius: float,
    thickness: float,
    vessel_type: str = 'thin_cylinder'
) -> Dict[str, float]:
    """
    Calculate stresses in pressure vessels
    
    Args:
        pressure: Internal pressure (Pa)
        radius: Vessel radius (m)
        thickness: Wall thickness (m)
        vessel_type: 'thin_cylinder', 'thick_cylinder', or 'sphere'
    """
    if vessel_type == 'thin_cylinder':
        hoop_stress = pressure * radius / thickness
        longitudinal_stress = pressure * radius / (2 * thickness)
        return {
            'hoop_stress': hoop_stress,
            'longitudinal_stress': longitudinal_stress,
            'von_mises_stress': np.sqrt(hoop_stress**2 - hoop_stress*longitudinal_stress + longitudinal_stress**2)
        }
    elif vessel_type == 'thick_cylinder':
        r_o = radius + thickness
        r_i = radius
        c = r_o**2 / r_i**2
        
        hoop_stress_inner = pressure * (c + 1) / (c - 1)
        hoop_stress_outer = 2 * pressure / (c - 1)
        radial_stress_inner = -pressure
        radial_stress_outer = 0
        
        return {
            'hoop_stress_inner': hoop_stress_inner,
            'hoop_stress_outer': hoop_stress_outer,
            'radial_stress_inner': radial_stress_inner,
            'radial_stress_outer': radial_stress_outer
        }
    elif vessel_type == 'sphere':
        hoop_stress = pressure * radius / (2 * thickness)
        return {
            'hoop_stress': hoop_stress,
            'von_mises_stress': hoop_stress
        }
    else:
        raise ValueError("Invalid vessel type. Choose 'thin_cylinder', 'thick_cylinder', or 'sphere'")

def thermal_stress(
    temperature_change: float,
    thermal_expansion: float,
    youngs_modulus: float,
    constraint: str = 'full'
) -> Dict[str, float]:
    """
    Calculate thermal stresses
    
    Args:
        temperature_change: Change in temperature (K)
        thermal_expansion: Coefficient of thermal expansion (1/K)
        youngs_modulus: Young's modulus (Pa)
        constraint: 'full' or 'partial'
    """
    if constraint == 'full':
        stress = -thermal_expansion * youngs_modulus * temperature_change
        strain = 0
    else:  # partial constraint
        stress = -0.5 * thermal_expansion * youngs_modulus * temperature_change
        strain = 0.5 * thermal_expansion * temperature_change
    
    return {
        'thermal_stress': stress,
        'thermal_strain': strain
    }
