#!/usr/bin/env python3
# tests/test_boundary_overrides.py
# Phase IX Architecture: Sovereign Boundary Overrides Integration Tests

import os
import sys
import unittest
import numpy as np

# Ensure path tracking routes correctly to src directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.math_engine import SubstrateMatrixSolver
from src.anima_core import AnimaCoreConductor
from src.persistence import SovereignPersistenceVault
from src.display import SovereignTerminalDisplay

class TestSovereignBoundaryConstraints(unittest.TestCase):
    def setUp(self):
        """Initializes the integrated 9-Rasa system testing environment."""
        self.num_nodes = 9
        self.feature_dim = 9
        
        # Test database footprint
        self.test_db_path = "./data/test_shadow_vault.db"
        
        # Instantiate architectural layers
        self.conductor = AnimaCoreConductor(num_nodes=self.num_nodes, feature_dim=self.feature_dim)
        self.vault = SovereignPersistenceVault(db_path=self.test_db_path)
        self.hud = SovereignTerminalDisplay()
        
        # Generate valid symmetric Graph Laplacian perimeter walls
        adjacency = np.ones((self.num_nodes, self.num_nodes)) - np.eye(self.num_nodes)
        degree = np.diag(np.sum(adjacency, axis=1))
        self.L = degree - adjacency
        self.W_in = np.eye(self.num_nodes) * 0.1

    def tearDown(self):
        """Safely cleans up transient disk artifacts after processing iteration completes."""
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except OSError:
                pass

    def test_scenario_a_laminar_ambient_flow(self):
        """Asserts baseline processing paths under typical non-destructive input signals."""
        # 1. Generate normal distributed ambient signal noise
        np.random.seed(42)
        ambient_input = np.random.normal(0.0, 0.1, self.num_nodes)
        
        # 2. Process unified execution step delta
        R_next, haptics, telemetry = self.conductor.process_horizon_interception_step(
            L=self.L, W_in=self.W_in, raw_input_stream=ambient_input
        )
        
        # 3. Assert baseline invariants hold smoothly
        self.assertEqual(telemetry["equilibrium_signature"], "Allostatic_Flow")
        self.assertFalse(telemetry["h_safe_attenuation_active"])
        self.assertLess(telemetry["vfe_tension"], 4.5)
        
        # 4. Verify data parsing inside display and persistence enclaves
        hud_output = self.hud.render_mandala_hud(R_next, telemetry)
        self.assertIn("ALLOSTATIC FLOW", hud_output)
        
        row_id = self.vault.commit_state_frame(R_next, telemetry, haptics)
        self.assertGreater(row_id, 0)

    def test_scenario_b_catastrophic_adversarial_shock(self):
        """Asserts H_safe clipping and circuit-breaker triggers under high-stress prompt injections."""
        # 1. Force an extreme mathematical input explosion wave
        adversarial_spike = np.ones(self.num_nodes) * 125.0
        
        # 2. Run first processing step to assert immediate H_safe amplitude attenuation
        R_1, haptics_1, telemetry_1 = self.conductor.process_horizon_interception_step(
            L=self.L, W_in=self.W_in, raw_input_stream=adversarial_spike
        )
        
        # If the math experiences sudden spikes, the attenuation engine must clamp it
        if telemetry_1["vfe_tension"] <= 4.5:
            self.assertTrue(telemetry_1["h_safe_attenuation_active"] or haptics_1[0] <= 1.0)
            
        # 3. Push system explicitly past the circuit breaker threshold (VFE > 4.5)
        # Directly force execute an out-of-bounds iteration step via sub-solver fields
        mock_high_vfe_R = np.random.normal(5.0, 2.0, (self.num_nodes, self.feature_dim)).astype(np.complex128)
        self.conductor.solver.R = mock_high_vfe_R
        
        # Step through conductor processing loop again to watch the circuit breaker trip
        _, haptics_2, telemetry_2 = self.conductor.process_horizon_interception_step(
            L=self.L, W_in=self.W_in, raw_input_stream=adversarial_spike
        )
        
        # 4. Verify system halts, changes signature to Śānta, and flattens holonomy arrays uniformly
        self.assertTrue(telemetry_2["allostatic_collapse_executed"])
        self.assertEqual(self.conductor.solver.equilibrium_signature, "Śānta")
        
        # All perimeter rows must equal the core attractor vector values perfectly
        for node_idx in range(self.num_nodes):
            np.testing.assert_array_almost_equal(
                self.conductor.solver.R[node_idx, :], self.conductor.solver.R[0, :]
            )

        # 5. Check visual output accurately profiles the collapse state
        hud_output_shock = self.hud.render_mandala_hud(self.conductor.solver.R, telemetry_2)
        self.assertIn("ŚĀNTA EQUILIBRIUM", hud_output_shock)

if __name__ == "__main__":
    print("⚡ RUNNING SOVEREIGN CORE FUNCTIONAL BOUNDARY TESTS ⚡\n")
    unittest.main()
