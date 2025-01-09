# 🛠️ MechSolver

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Desktop-orange.svg)

*A comprehensive mechanical engineering calculator available for both Desktop and Mobile platforms*

</div>

## 📱 Two Versions, One Solution

### Desktop Version (`pc_version/`)
- Full scientific computing capabilities with NumPy/SciPy
- Advanced visualization and plotting
- High-precision calculations
- Perfect for professional use and detailed analysis

### Mobile Version (`termux_version/`)
- Lightweight implementation for Android/Termux
- No heavy dependencies
- Works completely offline
- Optimized for mobile screens
- Same features, simplified calculations

## 🎯 Features

### 1. 📊 Kinematics
- Basic Motion Analysis
- Projectile Motion
- Simple Harmonic Motion
- Four-bar Mechanism
- Gear Train Analysis
- Cam Analysis

### 2. 💪 Stress Analysis
- Normal Stress and Strain
- Beam Bending
- Combined Stress
- Torsional Stress
- Fatigue Analysis
- Pressure Vessel
- Thermal Stress

### 3. 💨 Fluid Mechanics
- Reynolds Number
- Pipe Flow
- Pump Analysis
- Drag Force
- Bernoulli Equation
- Open Channel Flow
- Weir Flow
- Wave Properties

### 4. 🌡️ Thermodynamics
- Ideal Gas Law
- Heat Transfer
- Steam Properties
- Power Cycles
- HVAC Systems

### 5. ⚙️ Machine Design
- Gear Design
- Shaft Analysis
- Bearing Selection
- Spring Design
- Belt Drive Systems

### 6. 🔧 Materials Engineering
- Material Properties Database
- Stress-Strain Analysis
- Thermal Properties
- Cost Estimation
- Material Selection

## 💻 Installation

### Desktop Version
```bash
# Clone repository
git clone https://github.com/yourusername/mechsolver.git
cd mechsolver/pc_version

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the program
python mechsolver.py
```

### Termux Version
```bash
# Install Termux from F-Droid
# Open Termux and run:

# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python git

# Clone repository
git clone https://github.com/Adithianps04/mechsolver2
cd mechsolver/termux_version

# Install dependencies
pip install -r requirements.txt

# Run the program
python mechsolver.py
```

## 📖 Usage Examples

### Desktop Version
```python
# Stress Analysis Example
from modules.stress_analysis import combined_stress

result = combined_stress(
    sigma_x=100,  # MPa
    sigma_y=50,   # MPa
    tau_xy=25     # MPa
)
print(f"Principal Stress 1: {result['sigma_1']} MPa")
```

### Termux Version
```python
# Interactive Mode
python mechsolver.py

# Show About Information
python mechsolver.py --about
```

## 🔢 Key Equations

### Kinematics
```math
v = v₀ + at
s = ut + ½at²
v² = u² + 2as
```

### Stress Analysis
```math
σ = F/A
τ = VQ/It
ε = σ/E
```

### Fluid Mechanics
```math
Re = ρvD/μ
P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂
```

### Thermodynamics
```math
PV = nRT
Q = mcΔT
η = W/Q
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📅 Roadmap

### Q1 2025
- [ ] GUI Implementation
- [ ] Mobile App Development
- [ ] Cloud Integration
- [ ] Advanced Visualization

### Q2 2025
- [ ] Machine Learning Integration
- [ ] Real-time Analysis
- [ ] Database Expansion
- [ ] API Development

## 📝 Version History

- v1.0.0 (Current)
  - Initial release
  - Core modules implementation
  - Both PC and Termux versions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Contributors & Community
- Academic References
- Industry Standards
- Open Source Projects

## 📞 Contact & Support

- 📧 Email: support@mechsolver.org
- 💬 Discord: [Join our server](https://discord.gg/mechsolver)
- 🌐 Website: [www.mechsolver.org](https://www.mechsolver.org)

---

<div align="center">



[⬆ Back to top](#-mechsolver)

</div>
