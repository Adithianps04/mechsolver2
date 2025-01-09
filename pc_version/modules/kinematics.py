"""
Kinematics Module - Handles motion and dynamics calculations
"""
import numpy as np
from typing import Dict, Union, Optional, List

def solve_motion(
    velocity: Optional[float] = None,
    acceleration: Optional[float] = None,
    time: Optional[float] = None,
    displacement: Optional[float] = None
) -> Dict[str, float]:
    """Solves basic motion equations"""
    results = {}
    
    if velocity is not None and acceleration is not None and time is not None:
        results['displacement'] = velocity * time + 0.5 * acceleration * time**2
        results['final_velocity'] = velocity + acceleration * time
    elif velocity is not None and displacement is not None and acceleration is not None:
        results['final_velocity'] = np.sqrt(velocity**2 + 2 * acceleration * displacement)
        results['time'] = (-velocity + np.sqrt(velocity**2 + 2 * acceleration * displacement)) / acceleration
    
    return results

def projectile_motion(
    initial_velocity: float,
    angle: float,
    height: float = 0,
    g: float = 9.81,
    air_resistance: bool = False,
    drag_coefficient: float = 0.1
) -> Dict[str, Union[float, List[float]]]:
    """Enhanced projectile motion with air resistance option"""
    theta = np.radians(angle)
    v0x = initial_velocity * np.cos(theta)
    v0y = initial_velocity * np.sin(theta)
    
    if not air_resistance:
        time_flight = (v0y + np.sqrt(v0y**2 + 2*g*height)) / g
        max_height = height + (v0y**2) / (2*g)
        horizontal_range = v0x * time_flight
        
        # Calculate trajectory points
        t = np.linspace(0, time_flight, 100)
        x = v0x * t
        y = height + v0y*t - 0.5*g*t**2
        
        return {
            'max_height': max_height,
            'range': horizontal_range,
            'time_of_flight': time_flight,
            'trajectory_x': x.tolist(),
            'trajectory_y': y.tolist()
        }
    else:
        # Numerical solution with air resistance
        dt = 0.01
        x, y = [0], [height]
        vx, vy = [v0x], [v0y]
        t = [0]
        
        while y[-1] >= 0:
            # Air resistance force components
            v = np.sqrt(vx[-1]**2 + vy[-1]**2)
            fx = -drag_coefficient * v * vx[-1]
            fy = -drag_coefficient * v * vy[-1] - g
            
            # Update velocities and positions
            vx.append(vx[-1] + fx*dt)
            vy.append(vy[-1] + fy*dt)
            x.append(x[-1] + vx[-1]*dt)
            y.append(y[-1] + vy[-1]*dt)
            t.append(t[-1] + dt)
        
        return {
            'max_height': max(y),
            'range': x[-1],
            'time_of_flight': t[-1],
            'trajectory_x': x,
            'trajectory_y': y
        }

def simple_harmonic_motion(
    amplitude: float,
    frequency: float,
    time: Union[float, List[float]],
    phase: float = 0
) -> Dict[str, Union[float, List[float]]]:
    """Calculate simple harmonic motion parameters"""
    omega = 2 * np.pi * frequency
    
    if isinstance(time, (int, float)):
        displacement = amplitude * np.sin(omega * time + phase)
        velocity = amplitude * omega * np.cos(omega * time + phase)
        acceleration = -amplitude * omega**2 * np.sin(omega * time + phase)
        
        return {
            'displacement': displacement,
            'velocity': velocity,
            'acceleration': acceleration,
            'period': 1/frequency,
            'angular_frequency': omega
        }
    else:
        t = np.array(time)
        displacement = amplitude * np.sin(omega * t + phase)
        velocity = amplitude * omega * np.cos(omega * t + phase)
        acceleration = -amplitude * omega**2 * np.sin(omega * t + phase)
        
        return {
            'displacement': displacement.tolist(),
            'velocity': velocity.tolist(),
            'acceleration': acceleration.tolist(),
            'period': 1/frequency,
            'angular_frequency': omega
        }

def four_bar_mechanism(
    crank_length: float,
    coupler_length: float,
    rocker_length: float,
    ground_length: float,
    crank_angle: Union[float, List[float]]
) -> Dict[str, Union[float, List[float]]]:
    """Analyze four-bar mechanism kinematics"""
    def solve_position(theta):
        a, b, c, d = crank_length, coupler_length, rocker_length, ground_length
        
        # Complex number method for position analysis
        A = 2 * a * d * np.cos(theta)
        B = 2 * a * d * np.sin(theta)
        C = a**2 + d**2 - b**2 + c**2 + 2*a*d*np.cos(theta)
        
        beta = 2 * np.arctan((-B + np.sqrt(A**2 + B**2 - C**2)) / (C - A))
        
        # Coupler and rocker angles
        gamma = np.arctan2(
            c*np.sin(beta) - a*np.sin(theta),
            c*np.cos(beta) - a*np.cos(theta)
        )
        
        return beta, gamma
    
    if isinstance(crank_angle, (int, float)):
        beta, gamma = solve_position(np.radians(crank_angle))
        return {
            'rocker_angle': np.degrees(beta),
            'coupler_angle': np.degrees(gamma)
        }
    else:
        angles = np.radians(crank_angle)
        betas, gammas = [], []
        for angle in angles:
            beta, gamma = solve_position(angle)
            betas.append(np.degrees(beta))
            gammas.append(np.degrees(gamma))
        
        return {
            'rocker_angles': betas,
            'coupler_angles': gammas
        }

def gear_train_analysis(
    gear_teeth: List[int],
    input_speed: float,
    efficiency: float = 1.0
) -> Dict[str, float]:
    """Analyze gear train system"""
    if len(gear_teeth) < 2:
        raise ValueError("Need at least 2 gears in the train")
    
    # Calculate overall ratio
    ratio = 1
    for i in range(0, len(gear_teeth)-1, 2):
        ratio *= gear_teeth[i+1] / gear_teeth[i]
    
    # Output speed
    output_speed = input_speed / ratio
    
    # Pitch line velocities (assuming module = 1 for simplicity)
    pitch_velocities = []
    for teeth in gear_teeth:
        pitch_velocities.append((teeth * input_speed * np.pi) / 60)
    
    # Power transmission (assuming input power = 1 unit)
    input_power = 1
    output_power = input_power * efficiency**(len(gear_teeth)-1)
    
    return {
        'gear_ratio': ratio,
        'output_speed': output_speed,
        'pitch_velocities': pitch_velocities,
        'output_power': output_power,
        'efficiency': efficiency**(len(gear_teeth)-1)
    }

def cam_analysis(
    base_circle_radius: float,
    lift: float,
    angle: Union[float, List[float]],
    cam_type: str = 'simple_harmonic'
) -> Dict[str, Union[float, List[float]]]:
    """Analyze cam motion for different profiles"""
    def simple_harmonic_lift(theta):
        return lift * (1 - np.cos(theta)) / 2
    
    def cycloidal_lift(theta):
        return lift * (theta/(2*np.pi) - np.sin(theta)/(2*np.pi))
    
    def parabolic_lift(theta):
        if theta < np.pi:
            return 2 * lift * (theta/np.pi)**2
        else:
            return 2 * lift * (2 - theta/np.pi)**2
    
    lift_functions = {
        'simple_harmonic': simple_harmonic_lift,
        'cycloidal': cycloidal_lift,
        'parabolic': parabolic_lift
    }
    
    if cam_type not in lift_functions:
        raise ValueError(f"Unsupported cam type. Choose from: {list(lift_functions.keys())}")
    
    lift_func = lift_functions[cam_type]
    
    if isinstance(angle, (int, float)):
        theta = np.radians(angle)
        displacement = lift_func(theta)
        return {
            'displacement': displacement,
            'base_circle_radius': base_circle_radius,
            'total_radius': base_circle_radius + displacement
        }
    else:
        theta = np.radians(np.array(angle))
        displacement = [lift_func(t) for t in theta]
        return {
            'displacement': displacement,
            'base_circle_radius': base_circle_radius,
            'total_radius': [base_circle_radius + d for d in displacement]
        }
