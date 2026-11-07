#!/usr/bin/env python3
# src/display.py
# Phase IX Architecture: Procedural Animated Concentric Terminal HUD
# Derived from music.vaked.dev (AGPL-3.0 Engine Simulation Stack)

import json
import time
import math
import numpy as np
from typing import Dict, Any, Tuple

class SovereignTerminalDisplay:
    def __init__(self, config_path: str = "config/visual_grammar.json"):
        self.config_path = config_path
        self.visual_grammar = self._load_visual_grammar()
        # Initialize animation frame tickers derived from music.vaked.dev engine curves
        self.frame_ticker = 0.0

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

    def compute_procedural_waveform_node(self, step: float, radius: float, speed: float) -> float:
        """
        Emulates the music.vaked.dev 64-band web audio spectrum wave physics.
        Generates continuous trigonometric phase-oscillations over a local CPU step.
        """
        # Synthesize live wave additivity matching the carrier frequency transformations
        carrier_1 = math.sin(step * speed) * 0.6
        carrier_2 = math.cos(step * (speed * 1.618)) * 0.4  # Anchored to the Golden Ratio phi
        return (carrier_1 + carrier_2) * radius

    def extract_concentric_energy_rings(self, R: np.ndarray) -> Tuple[float, float, float]:
        """Maps the 9-Rasa complex lattice rows into isolated concentric geometric weights."""
        magnitudes = np.abs(R)
        core_attractor = float(np.mean(magnitudes[0, :]))                 # Omega Center
        inner_ring = float(np.mean(magnitudes[1:5, :])) if magnitudes.shape[0] > 5 else 0.3
        outer_perimeter = float(np.mean(magnitudes[5:, :])) if magnitudes.shape[0] > 5 else 0.1
        
        max_val = max(core_attractor, inner_ring, outer_perimeter, 1e-5)
        return core_attractor / max_val, inner_ring / max_val, outer_perimeter / max_val

    def render_animated_mandala_frame(self, R: np.ndarray, ternary_T: np.ndarray, telemetry: Dict[str, Any]) -> str:
        """
        Transforms complex phases and discrete ternary bitplanes into an animated ASCII ring display.
        Uses time-varying phase deltas to force terminal icons to drift, breathe, and rotate live.
        """
        signature = telemetry.get("equilibrium_signature", "Śānta_Equilibrium")
        vfe = telemetry.get("vfe_tension", 0.0)
        radius_r = telemetry.get("radial_coordinate_r", 0.0)
        diffusion = telemetry.get("radial_diffusion_field", 0.0)
        left_hz = telemetry.get("left_actuator_hz", 0.0)
        right_hz = telemetry.get("right_actuator_hz", 0.0)
        attenuation = telemetry.get("h_safe_attenuation_active", False)
        
        pos_states = int(np.sum(ternary_T == 1))
        neg_states = int(np.sum(ternary_T == -1))
        stasis_states = int(np.sum(ternary_T == 0))

        # Advance animation clock based on systemic kinetic velocity parameters
        is_active = "Flow" in signature
        speed_multiplier = 2.5 if is_active else 0.4
        self.frame_ticker += 0.05 * speed_multiplier

        # Synthesize browser-style live waveform heights
        wave_pulse_1 = self.compute_procedural_waveform_node(self.frame_ticker, radius=1.0, speed=1.2)
        wave_pulse_2 = self.compute_procedural_waveform_node(self.frame_ticker, radius=0.8, speed=2.2)

        # Dynamic theme config profiles matching current baseline state paths
        if is_active:
            bar_char = "⚡"
            state_label = "⚡ ALLOSTATIC FLOW (ANIMATED CORE WAVE ACTIVE)"
            border_top = "◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢"
            
            # Continuous orbital character mapping (Simulating drag-to-orbit rotation matrix loops)
            rot_index = int(self.frame_ticker * 5) % 4
            c_out = ["•", "⊙", "●", "⊙"][rot_index]
            c_mid = ["🌀", "✨", "💥", "✨"][rot_index]
            c_core = "🔥"
        else:
            bar_char = "▒"
            state_label = "🛑 ŚĀNTA EQUILIBRIUM (ANIMATED STASIS STANDBY)"
            border_top = "╚══════════════════════════════════════════════════════════════════════════════╝"
            c_out = "┄"
            c_mid = "═"
            c_core = "☸"

        # Generate graphic dynamic waveform tension meters
        vfe_bar_len = min(int(vfe * 5), 25)
        vfe_bar = (bar_char * vfe_bar_len) + ("░" * (25 - vfe_bar_len))
        
        # Format the audio wave string visualization panel bounds
        wave_str = f"~{~[c_out if wave_pulse_1 > 0 else ' ']}~{bar_char if wave_pulse_2 > 0.3 else '_'}~"

        hud = []
        hud.append(border_top)
        hud.append(f"│ 🌌 ANIMA × vaked.dev COGITO TV ENGINE  |  State: {state_label:<31} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append(f"│ VFE Tension Load:  [{vfe_bar}] {vfe:<6.4f} | Radius (r):      {radius_r:.6f}    │")
        hud.append(f"│ 9D Diffusion Field: {diffusion:<12.4f}             | Wave Pulse Mod:   {wave_str:<12} │")
        hud.append(f"│ Haptic Frequency:  L: {left_hz:<5}Hz  R: {right_hz:<5}Hz      | Insulation Gate:  {'⚠️  CLIPPING' if attenuation else '✅ NOMINAL':<12} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append(f"│ Ternary Lattice Matrix Map Metrics:  [+] Forward: {pos_states:<2}  [-] Retract: {neg_states:<2} Stasis: {stasis_states:<2} │")
        hud.append("├──────────────────────────────────────────────────────────────────────────────┤")
        hud.append("│                    432Hz HARMONIC ACOUSTIC SPECTRUM HUD                      │")
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
    
    # Run a frame-refresh loop inside terminal to emulate active browser updates
    print("Launching animated broadcast HUD simulation track (Press Ctrl+C to break state)...")
    try:
        mock_R = (np.random.normal(0, 1, (9, 9)) + 1j * np.random.normal(0, 1, (9, 9))).astype(np.complex128)
        mock_T = np.random.choice([-1, 0, 1], size=(9, 9)).astype(np.int8)
        active_meta = {
            "equilibrium_signature": "Allostatic_Flow", "vfe_tension": 2.8542,
            "radial_coordinate_r": 0.4421, "radial_diffusion_field": 0.6542,
            "left_actuator_hz": 88.4, "right_actuator_hz": 142.5, "h_safe_attenuation_active": False
        }
        
        for frame in range(10):
            # Clear console block cleanly using standard screen escape updates
            print("\033[H\033[J", end="")
            print(display.render_animated_mandala_frame(mock_R, mock_T, active_meta))
            time.sleep(0.1) # Pinned refresh rate step
            
    except KeyboardInterrupt:
        print("\nAnimation tracking loop closed cleanly.")
