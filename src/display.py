#!/usr/bin/env python3
# src/display.py
# Phase IX Architecture: Low-Power Terminal ASCII Mandala HUD

import json
import numpy as np
from typing import Dict, Any, Tuple

class SovereignTerminalDisplay:
    def __init__(self, config_path: str = "config/visual_grammar.json"):
        self.config_path = config_path
        self.visual_grammar = self._load_visual_grammar()

    def _load_visual_grammar(self) -> Dict[str, Any]:
        """Loads visual configuration boundaries safely."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f).get("concentric_matrix_lattice", {})
        except FileNotFoundError:
            # Fallback inline parameters matching the frozen visual grammar spec
            return {
                "states": {
                    "dormant": {"signature": "Śānta_Equilibrium", "ascii_ring_density": "sparse"},
                    "active": {"signature": "Allostatic_Flow", "ascii_ring_density": "dense"}
                }
            }

    def compute_radial_intensity_grid(self, R: np.ndarray) -> np.ndarray:
        """Converts complex 9x9 matrix phases into normalized radial magnitudes."""
        # Calculate localized vector norms over the complex plane cells
        magnitudes = np.abs(R)
        max_val = np.max(magnitudes)
        if max_val == 0:
            return np.zeros((3, 3))
        
        # Down-sample the 9-node architecture to a tight 3x3 telemetry grid block
        grid_3x3 = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                # Map slices of the 9x9 manifold to the visual console coordinate grid
                grid_3x3[i, j] = np.mean(magnitudes[i*3:(i+1)*3, j*3:(j+1)*3])
                
        # Normalize grid smoothly between bounds [0.0, 1.0]
        return np.clip(grid_3x3 / max_val, 0.0, 1.0)

    def render_mandala_hud(self, R: np.ndarray, telemetry: Dict[str, Any]) -> str:
        """Transforms current mathematical wave phases into an ASCII visual layout."""
        signature = telemetry.get("equilibrium_signature", "Śānta_Equilibrium")
        vfe = telemetry.get("vfe_tension", 0.0)
        left_hz = telemetry.get("left_actuator_hz", 0.0)
        right_hz = telemetry.get("right_actuator_hz", 0.0)
        attenuation = telemetry.get("h_safe_attenuation_active", False)

        # Select character density spectrum arrays based on operational state paths
        if "Flow" in signature:
            chars = [" ", ".", "*", "o", "O", "🌀", "🔥"]
            state_label = "⚡ ALLOSTATIC FLOW (ACTIVE RUNTIME)"
        else:
            chars = [" ", ".", "-", "=", "+", "☸", "Ś"]
            state_label = "🛑 ŚĀNTA EQUILIBRIUM (DORMANT VAULT)"

        # Compute spatial footprint matrix
        intensity_grid = self.compute_radial_intensity_grid(R)
        
        hud = []
        hud.append("┌──────────────────────────────────────────────────────────────────────────────┐")
        hud.append(f"│ 🌌 ANIMA MULTI-SENSORY TELEMETRY HUD  |  State: {state_label:<28} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append(f"│ System Tension (VFE): {vfe:<6.4f}  |  Haptic Channels: L: {left_hz:<5}Hz  R: {right_hz:<5}Hz   │")
        hud.append(f"│ Attenuation Status:   {'[⚠️ CLIPPING ACTIVE]' if attenuation else '[✅ ENVELOPE NOMINAL]':<54} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append("│                         RADIAL CORE MANDALA MATRIX GRID                      │")
        
        # Build layout rings maps from localized scalar intensities
        for row in intensity_grid:
            row_chars = []
            for val in row:
                idx = min(int(val * (len(chars) - 1)), len(chars) - 1)
                row_chars.append(chars[idx])
            line_str = f"                                 [ {row_chars[0]} ] ─── [ {row_chars[1]} ] ─── [ {row_chars[2]} ]"
            hud.append(f"│{line_str:<78}│")
            
        hud.append("└──────────────────────────────────────────────────────────────────────────────┘")
        return "\n".join(hud)

if __name__ == "__main__":
    display = SovereignTerminalDisplay()
    
    # 1. Simulate Dormant State Array Matrix
    print("\n--- SIMULATING RETRO DORMANT STATE ---")
    dormant_R = np.zeros((9, 9), dtype=np.complex128)
    dormant_R[0, :] = 0.5 + 0j  # Locked core axis target
    dormant_telemetry = {"equilibrium_signature": "Śānta_Equilibrium", "vfe_tension": 0.32, "left_actuator_hz": 0.0, "right_actuator_hz": 0.0, "h_safe_attenuation_active": False}
    print(display.render_mandala_hud(dormant_R, dormant_telemetry))
    
    # 2. Simulate Active Dynamic Flow Surge Matrix
    print("\n--- SIMULATING HIGH-KINETIC ACTIVE SURGE ---")
    active_R = np.random.normal(0, 1.5, (9, 9)) + 1j * np.random.normal(0, 1.5, (9, 9))
    active_R = active_R.astype(np.complex128)
    active_telemetry = {"equilibrium_signature": "Allostatic_Flow", "vfe_tension": 3.87, "left_actuator_hz": 112.5, "right_actuator_hz": 194.2, "h_safe_attenuation_active": True}
    print(display.render_mandala_hud(active_R, active_telemetry))
