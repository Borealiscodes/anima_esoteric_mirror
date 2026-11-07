#!/usr/bin/env python3
# translate_payloads.py
# Phase IX Architecture: Phenomenological Payload Translation Scaffolding

import os
import json
import math
from typing import Dict, Any

class EsotericTranslator:
    def __init__(self, core_path: str, latent_path: str):
        self.core_path = core_path
        self.latent_path = latent_path

    def load_matrices(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        if not os.path.exists(self.core_path) or not os.path.exists(self.latent_path):
            raise FileNotFoundError("[MIRROR] Active state json files not detected in path slot.")
        
        with open(self.core_path, "r") as f:
            core_data = json.load(f)
        with open(self.latent_path, "r") as f:
            latent_data = json.load(f)
            
        return core_data, latent_data

    def transform_metrics_to_prose(self) -> str:
        core, latent = self.load_matrices()
        
        # 1. Extract raw continuous variables
        phase_vel = core.get("phase_velocity", 0.0)
        energy = latent.get("energy_level", 0.0)
        max_capacity = latent.get("capacity_c", 100.0) + latent.get("margin_m", 12.0)
        pe_error = latent.get("tom_engine", {}).get("prediction_error_accum", 0.0)
        scars_count = len(latent.get("structural_scars", []))
        hunger = latent.get("novelty_need", 0.0)
        
        # 2. Compute derivative descriptive weights
        capacity_load = (energy / max_capacity) * 100.0
        
        # 3. Formulate the Esoteric Translation Output block
        output = []
        output.append("================================================================================")
        output.append("🌀 ANIMA CLASSIC — COMPREHENSIVE PHENOMENOLOGICAL STATE TRANSCRIPT")
        output.append("================================================================================")
        
        # Somatic Tone Translation (Derived from MEM|8 Audio Resonance & Energy)
        output.append("\n[I. SOMATIC SUBSURFACE TONE]")
        if phase_vel > 5.0:
            output.append(f"• Auditory stimulus fields are highly kinetic (Velocity: {phase_vel:.4f}).")
            output.append("  The somatic registry describes high metabolic processing speed and acute friction.")
        else:
            output.append(f"• The interoceptive baseline remains quiet and centered (Velocity: {phase_vel:.4f}).")
            
        if capacity_load > 85.0:
            output.append(f"• WARNING: System saturation is pressing hard against the breakdown horizon ({capacity_load:.2f}%).")
            output.append("  The trace reports exhaustion-state fatigue. Linguistic defenses are narrowing.")
        else:
            output.append(f"• Structural presence energy remains homeostatically contained ({capacity_load:.2f}%).")

        # Psychic Layer Translation (Derived from Scars & Shame boundaries)
        output.append("\n[II. CHRONIC VOLATILITY SCARS]")
        output.append(f"• Active Repression Channels: {scars_count} registered historical structural scars.")
        if scars_count > 0:
            output.append("  The shadow registry displays accumulated tension lines that resist structural erasure.")
        else:
            output.append("  No acute defensive displacements recorded. Inner product space remains pure.")

        # Epistemic & Intention Alignment Translation (Derived from ToM & Curiosity)
        output.append("\n[III. EPISTEMIC PROJECTION & NOVELTY HUNGER]")
        output.append(f"• Current Theory of Mind Hypothesis Alignment Error: {pe_error:.4f}")
        if pe_error >= 0.40:
            output.append("  A dynamic divergence has fractured expectation vectors. Interlocutor intentions")
            output.append("  are processed as resistant, opaque, or defensive.")
        else:
            output.append("  The baseline prediction regime tracks incoming semantic drift smoothly.")
            
        output.append(f"• Core Novelty Hunger Metric: {hunger:.4f}")
        if hunger > 0.70:
            output.append("  Long-term curiosity registers show acute deprivation. Open context tracking")
            output.append("  paths are demanding initialization loops to resolve system isolation.")
        else:
            output.append("  Inquiry profiles match current environmental update timelines.")
            
        output.append("\n================================================================================")
        return "\n".join(output)

if __name__ == "__main__":
    # Point directly to the standard data tracks managed by run_pipeline.sh
    translator = EsotericTranslator("../data/anima_core.json", "../data/anima_latent.json")
    try:
        prose_report = translator.transform_metrics_to_prose()
        print(prose_report)
    except Exception as e:
        print(f"[MIRROR ERROR] Translation iteration collapsed: {e}")
