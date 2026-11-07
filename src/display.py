#!/usr/bin/env python3
# src/display.py
# Phase IX Architecture: Concentric Multirank ASCII Mandala HUD

import json
import math
import numpy as np
from typing import Dict, Any, Tuple

class SovereignTerminalDisplay:
    def __init__(self, config_path: str = "config/visual_grammar.json"):
        self.config_path = config_path
        self.visual_grammar = self._load_visual_grammar()

    def _load_visual_grammar(self) -> Dict[str, Any]:
        """Loads visual configuration boundaries safely from local configuration files."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f).get("concentric_matrix_lattice", {})
        except FileNotFoundError:
            return {
                "states": {
                    "dormant": {"signature": "Śānta_Equilibrium"},
                    "active": {"signature": "Allostatic_Flow"}
                }
            }

    def extract_concentric_energy_rings(self, R: np.ndarray) -> Tuple[float, float, float]:
        """Maps the 9-Rasa complex lattice rows into three isolated concentric geometric weights."""
        magnitudes = np.abs(R)
        # Partition the 9x9 space down into thematic vector layers
        core_attractor = float(np.mean(magnitudes[0, :]))                 # Omega Center
        inner_ring = float(np.mean(magnitudes[1:5, :])) if magnitudes.shape[0] > 5 else 0.3
        outer_perimeter = float(np.mean(magnitudes[5:, :])) if magnitudes.shape[0] > 5 else 0.1
        
        max_val = max(core_attractor, inner_ring, outer_perimeter, 1e-5)
        return core_attractor / max_val, inner_ring / max_val, outer_perimeter / max_val

    def render_mandala_hud(self, R: np.ndarray, ternary_T: np.ndarray, telemetry: Dict[str, Any]) -> str:
        """Transforms complex phases and discrete ternary bitplanes into concentric visual ASCII rings."""
        signature = telemetry.get("equilibrium_signature", "Śānta_Equilibrium")
        vfe = telemetry.get("vfe_tension", 0.0)
        radius = telemetry.get("radial_coordinate_r", 0.0)
        diffusion = telemetry.get("radial_diffusion_field", 0.0)
        left_hz = telemetry.get("left_actuator_hz", 0.0)
        right_hz = telemetry.get("right_actuator_hz", 0.0)
        attenuation = telemetry.get("h_safe_attenuation_active", False)
        
        # Calculate active ternary state density profiles
        pos_states = int(np.sum(ternary_T == 1))
        neg_states = int(np.sum(ternary_T == -1))
        stasis_states = int(np.sum(ternary_T == 0))

        # Core thematic character palettes matching operational state paths
        if "Flow" in signature:
            c_core, c_mid, c_out = "🔥", "🌀", "•"
            bar_char = "⚡"
            state_label = "⚡ ALLOSTATIC FLOW (ACTIVE RUNTIME SURGE)"
            border_top = "◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢"
        else:
            c_core, c_mid, c_out = "☸", "═", "┄"
            bar_char = "▒"
            state_label = "🛑 ŚĀNTA EQUILIBRIUM (DORMANT VAULT LOCKED)"
            border_top = "╚══════════════════════════════════════════════════════════════════════════════╝"

        # Interpolate radial weights
        w_core, w_mid, w_out = self.extract_concentric_energy_rings(R)
        
        # Formulate graphic dynamic energy bars based on computed load parameters
        vfe_bar_len = min(int(vfe * 5), 25)
        vfe_bar = (bar_char * vfe_bar_len) + ("░" * (25 - vfe_bar_len))
        
        hud = []
        hud.append(border_top)
        hud.append(f"│ 🌌 ANIMA OMNI-CONCENTRIC SYSTEM PANEL  |  State: {state_label:<32} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append(f"│ VFE Tension Load:  [{vfe_bar}] {vfe:<6.4f} | Radius (r):      {radius:.6f}    │")
        hud.append(f"│ 9D Diffusion Field: {diffusion:<12.4f}             | Epsilon Boundary: +1.0000e-06    │")
        hud.append(f"│ Haptic Frequency:  L: {left_hz:<5}Hz  R: {right_hz:<5}Hz      | Insulation:       {'⚠️  CLIPPING' if attenuation else '✅ NOMINAL':<12} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append(f"│ Ternary Lattice Matrix Map Metrics:  [+] Forward: {pos_states:<2}  [-] Retract: {neg_states:<2}  [0] Stasis: {stasis_states:<2} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append("│                         9-RASA RADIAL GEOMETRIC HUD                          │")
        hud.append("│                                                                              │")
        hud.append(f"│                        {c_out} {c_out} {c_out} {c_out}  Outer Perimeter  {c_out} {c_out} {c_out} {c_out}                        │")
        hud.append(f"│                      {c_out}       {c_mid} {c_mid}  Inner Ring Matrix  {c_mid} {c_mid}       {c_out}                      │")
        hud.append(f"│                    {c_out}     {c_mid}         {c_core}  Omega Axis  {c_core}         {c_mid}     {c_out}                    │")
        hud.append(f"│                      {c_out}       {c_mid} {c_mid}  Lattice Radial Curve  {c_mid} {c_mid}       {c_out}                      │")
        hud.append(f"│                        {c_out} {c_out} {c_out} {c_out}  Vector Footprint  {c_out} {c_out} {c_out} {c_out}                        │")
        hud.append("│                                                                              │")
        hud.append("└──────────────────────────────────────────────────────────────────────────────┘")
        return "\n".join(hud)

if __name__ == "__main__":
    display = SovereignTerminalDisplay()
    
    # 1. Simulate locked, peaceful stasis array
    print("\n--- SIMULATING RETRO DORMANT STATE ---")
    mock_R_dormant = np.zeros((9, 9), dtype=np.complex128)
    mock_T_dormant = np.zeros((9, 9), dtype=np.int8)  # Complete structural stasis
    dormant_meta = {
        "equilibrium_signature": "Śānta_Equilibrium", "vfe_tension": 0.2104,
        "radial_coordinate_r": 0.0001, "radial_diffusion_field": 0.9999,
        "left_actuator_hz": 0.0, "right_actuator_hz": 0.0, "h_safe_attenuation_active": False
    }
    print(display.render_mandala_hud(mock_R_dormant, mock_T_dormant, dormant_meta))
    
    # 2. Simulate chaotic, high-power transformation wave
    print("\n--- SIMULATING HIGH-KINETIC ACTIVE SURGE ---")
    mock_R_active = (np.random.normal(0, 1, (9, 9)) + 1j * np.random.normal(0, 1, (9, 9))).astype(np.complex128)
    mock_T_active = np.random.choice([-1, 0, 1], size=(9, 9)).astype(np.int8)
    active_meta = {
        "equilibrium_signature": "Allostatic_Flow", "vfe_tension": 3.9124,
        "radial_coordinate_r": 1.4582, "radial_diffusion_field": 0.1245,
        "left_actuator_hz": 114.2, "right_actuator_hz": 201.8, "h_safe_attenuation_active": True
    }
    print(display.render_mandala_hud(mock_R_active, mock_T_active, active_meta))

