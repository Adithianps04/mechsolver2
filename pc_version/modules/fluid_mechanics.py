"""
Fluid Mechanics Module - Handles fluid flow and hydraulic calculations
"""
import numpy as np
from typing import Dict, Union, Optional, List, Tuple

def reynolds_number(
    velocity: float,
    characteristic_length: float,
    kinematic_viscosity: float
) -> float:
    """Calculate Reynolds number"""
    return (velocity * characteristic_length) / kinematic_viscosity

def pipe_head_loss(
    length: float,
    diameter: float,
    velocity: float,
    friction_factor: float,
    minor_losses: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Calculate head loss in a pipe including minor losses
    
    Args:
        length: Pipe length (m)
        diameter: Pipe diameter (m)
        velocity: Flow velocity (m/s)
        friction_factor: Darcy friction factor
        minor_losses: Dictionary of minor loss coefficients and counts
    """
    # Major losses (Darcy-Weisbach equation)
    major_loss = friction_factor * length * velocity**2 / (diameter * 2 * 9.81)
    
    # Minor losses
    minor_loss = 0
    if minor_losses:
        for k, count in minor_losses.items():
            minor_loss += count * velocity**2 / (2 * 9.81)
    
    total_loss = major_loss + minor_loss
    
    return {
        'major_loss': major_loss,
        'minor_loss': minor_loss,
        'total_loss': total_loss
    }

def flow_rate_to_velocity(
    flow_rate: float,
    diameter: float
) -> float:
    """Convert volumetric flow rate to velocity"""
    area = np.pi * (diameter/2)**2
    return flow_rate / area

def pump_power(
    flow_rate: float,
    head: float,
    efficiency: float,
    fluid_density: float = 1000
) -> Dict[str, float]:
    """Calculate pump power requirements"""
    hydraulic_power = fluid_density * 9.81 * flow_rate * head
    shaft_power = hydraulic_power / efficiency
    
    return {
        'hydraulic_power': hydraulic_power,
        'shaft_power': shaft_power,
        'efficiency': efficiency
    }

def orifice_flow(
    pressure_diff: float,
    diameter: float,
    discharge_coeff: float = 0.61,
    fluid_density: float = 1000
) -> Dict[str, float]:
    """
    Calculate flow through an orifice
    
    Args:
        pressure_diff: Pressure difference across orifice (Pa)
        diameter: Orifice diameter (m)
        discharge_coeff: Discharge coefficient
        fluid_density: Fluid density (kg/m³)
    """
    area = np.pi * (diameter/2)**2
    velocity = discharge_coeff * np.sqrt(2 * pressure_diff / fluid_density)
    flow_rate = velocity * area
    
    return {
        'velocity': velocity,
        'flow_rate': flow_rate,
        'reynolds_number': reynolds_number(velocity, diameter, 1e-6)  # Assuming water
    }

def nozzle_thrust(
    mass_flow_rate: float,
    exit_velocity: float,
    exit_pressure: float,
    ambient_pressure: float,
    exit_area: float
) -> Dict[str, float]:
    """
    Calculate thrust produced by a nozzle
    
    Args:
        mass_flow_rate: Mass flow rate (kg/s)
        exit_velocity: Exit velocity (m/s)
        exit_pressure: Exit pressure (Pa)
        ambient_pressure: Ambient pressure (Pa)
        exit_area: Exit area (m²)
    """
    momentum_thrust = mass_flow_rate * exit_velocity
    pressure_thrust = (exit_pressure - ambient_pressure) * exit_area
    total_thrust = momentum_thrust + pressure_thrust
    
    return {
        'momentum_thrust': momentum_thrust,
        'pressure_thrust': pressure_thrust,
        'total_thrust': total_thrust
    }

def drag_force(
    velocity: float,
    fluid_density: float,
    reference_area: float,
    drag_coefficient: float
) -> Dict[str, float]:
    """Calculate drag force"""
    dynamic_pressure = 0.5 * fluid_density * velocity**2
    drag = drag_coefficient * dynamic_pressure * reference_area
    
    return {
        'drag_force': drag,
        'dynamic_pressure': dynamic_pressure
    }

def bernoulli_equation(
    height1: float,
    velocity1: float,
    pressure1: float,
    height2: float,
    velocity2: Optional[float] = None,
    pressure2: Optional[float] = None,
    fluid_density: float = 1000
) -> Dict[str, float]:
    """Apply Bernoulli's equation between two points"""
    g = 9.81
    
    if velocity2 is None and pressure2 is None:
        # Calculate missing velocity
        term1 = pressure1/(fluid_density*g) + height1 + velocity1**2/(2*g)
        velocity2 = np.sqrt(2*g*(term1 - height2))
        pressure2 = pressure1
    elif velocity2 is None:
        # Calculate missing velocity
        term1 = pressure1/(fluid_density*g) + height1 + velocity1**2/(2*g)
        term2 = pressure2/(fluid_density*g) + height2
        velocity2 = np.sqrt(2*g*(term1 - term2))
    elif pressure2 is None:
        # Calculate missing pressure
        term1 = pressure1/(fluid_density*g) + height1 + velocity1**2/(2*g)
        pressure2 = fluid_density*g*(term1 - height2 - velocity2**2/(2*g))
    
    return {
        'velocity2': velocity2,
        'pressure2': pressure2,
        'height2': height2
    }

def open_channel_flow(
    channel_width: float,
    flow_depth: float,
    slope: float,
    manning_n: float,
    channel_type: str = 'rectangular'
) -> Dict[str, float]:
    """
    Calculate open channel flow parameters
    
    Args:
        channel_width: Width of channel (m)
        flow_depth: Depth of flow (m)
        slope: Channel slope (m/m)
        manning_n: Manning's roughness coefficient
        channel_type: 'rectangular' or 'trapezoidal'
    """
    if channel_type == 'rectangular':
        area = channel_width * flow_depth
        wetted_perimeter = channel_width + 2*flow_depth
        hydraulic_radius = area / wetted_perimeter
        
        # Manning's equation
        velocity = (1/manning_n) * hydraulic_radius**(2/3) * np.sqrt(slope)
        flow_rate = velocity * area
        
        # Froude number
        froude = velocity / np.sqrt(9.81 * flow_depth)
        
        return {
            'flow_rate': flow_rate,
            'velocity': velocity,
            'froude_number': froude,
            'flow_type': 'subcritical' if froude < 1 else 'supercritical'
        }
    else:
        raise ValueError("Only rectangular channels are currently supported")

def weir_flow(
    weir_height: float,
    weir_width: float,
    head: float,
    weir_type: str = 'rectangular'
) -> Dict[str, float]:
    """
    Calculate flow over a weir
    
    Args:
        weir_height: Height of weir (m)
        weir_width: Width of weir (m)
        head: Head above weir crest (m)
        weir_type: 'rectangular' or 'v-notch'
    """
    g = 9.81
    
    if weir_type == 'rectangular':
        # Francis formula for rectangular weir
        discharge_coeff = 0.61
        flow_rate = (2/3) * discharge_coeff * weir_width * np.sqrt(2*g) * head**(3/2)
        
        return {
            'flow_rate': flow_rate,
            'discharge_coefficient': discharge_coeff
        }
    elif weir_type == 'v-notch':
        # Thomson formula for v-notch weir
        theta = np.radians(90)  # Assuming 90-degree v-notch
        discharge_coeff = 0.59
        flow_rate = (8/15) * discharge_coeff * np.tan(theta/2) * np.sqrt(2*g) * head**(5/2)
        
        return {
            'flow_rate': flow_rate,
            'discharge_coefficient': discharge_coeff
        }
    else:
        raise ValueError("Invalid weir type. Choose 'rectangular' or 'v-notch'")

def wave_properties(
    wavelength: float,
    water_depth: float,
    fluid_density: float = 1000
) -> Dict[str, float]:
    """
    Calculate water wave properties
    
    Args:
        wavelength: Wave length (m)
        water_depth: Water depth (m)
        fluid_density: Fluid density (kg/m³)
    """
    g = 9.81
    k = 2 * np.pi / wavelength  # Wave number
    
    # Dispersion relation
    omega = np.sqrt(g * k * np.tanh(k * water_depth))
    period = 2 * np.pi / omega
    wave_speed = wavelength / period
    
    # Group velocity
    n = 0.5 * (1 + 2*k*water_depth / np.sinh(2*k*water_depth))
    group_velocity = n * wave_speed
    
    return {
        'wave_speed': wave_speed,
        'group_velocity': group_velocity,
        'period': period,
        'frequency': 1/period
    }
