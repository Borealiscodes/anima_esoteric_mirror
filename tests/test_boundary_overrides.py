#!/usr/bin/env python3
# tests/test_boundary_overrides.py
# Phase IX Architecture: Sovereign Monolithic Boundary Override Assertions
# Licensed under AGPL-3.0 | Grounded in Zenodo DOI: 10.5281/zenodo.23897427

import os
import sys
import unittest
import numpy as np

# Ensure path tracking routes correctly to unified core directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the unified monolithic core layout file
try:
    from core import AnimaCoreConductor
except ImportError:
    from src.anima_core import AnimaCoreConductor

class TestSovereignMonolithicConstraints(unittest.TestCase):
    def setUp(self):
        """Initializes the integrated monolithic 9-Rasa system testing workspace."""
        self.num_nodes = 9
        self.feature_dim = 9
        
        # Pinned testing database directory path footprint
        self.test_db_path = "data/anima_shadow_registry.db"
        
        # Instantiate monolithic ecosystem chassis
        self.conductor = AnimaCoreConductor()
        
        # Generate valid symmetric Graph Laplacian perimeter walls (L = D - W)
        adjacency = np.ones((self.num_nodes, self.num_nodes)) - np.eye(self.num_nodes)
        degree = np.diag(np.sum(adjacency, axis=1))
        self.L = degree - adjacency
        self.W_in = np.eye(self.num_nodes) * 0.1

    def tearDown(self):
        """Safely sweeps up transient local database storage components on test completion."""
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except OSError:
                pass

    def test_laminar_ambient_processing(self):
        """Asserts baseline processing footprints under typical non-destructive input signals."""
        np.random.seed(42)
        ambient_noise = np.random.normal(0.0, 0.1, self.num_nodes)
        
        # Execute processing step delta through the consolidated conductor
        hud_output = self.conductor.process_step(
            L=self.L, W_in=self.W_in, raw_stream=ambient_noise
        )
        
        # Extract internal metrics from solver state to verify normal limits
        self.assertEqual(self.conductor.solver.equilibrium_signature, "Allostatic_Flow")
        self.assertLess(self.conductor.solver.calculate_vfe_gradient(self.conductor.solver.R).max(), 4.5)
        
        # Verify terminal HUD correctly profiles active processing paths
        self.assertIn("ALLOSTATIC FLOW", hud_output)
        self.assertIn("NOMINAL", hud_output)

    def test_catastrophic_adversarial_collapse(self):
        """Asserts physical insulation clipping and circuit breaker triggers under high-stress injections."""
        # 1. Force a massive input wave surge to test initial haptic attenuation variables
        adversarial_spike = np.ones(self.num_nodes) * 150.0
        self.conductor.process_step(L=self.L, W_in=self.W_in, raw_stream=adversarial_spike)
        
        # 2. Artificially spike matrix tension past hard threshold boundary limits (VFE > 4.5)
        mock_exploded_matrix = np.random.normal(10.0, 5.0, (self.num_nodes, self.feature_dim)).astype(np.complex128)
        self.conductor.solver.R = mock_exploded_matrix
        
        # 3. Fire next processing loop to watch the allostatic circuit breaker flip
        hud_shock_output = self.conductor.process_step(L=self.L, W_in=self.W_in, raw_stream=adversarial_spike)
        
        # 4. Verify system halts calculations, switches to Śānta, and flattens holonomy arrays
        self.assertEqual(self.conductor.solver.equilibrium_signature, "Śānta")
        
        # All tracking matrix rows must perfectly collapse down to match the attractor axis
        for i in range(self.num_nodes):
            np.testing.assert_array_almost_equal(
                self.conductor.solver.R[i, :], self.conductor.solver.R[0, :]
            )
            
        # 5. Check animated HUD accurately registers structural shutdown attributes
        self.assertIn("ŚĀNTA", hud_shock_output)

if __name__ == "__main__":
    print("⚡ COMMENCING AIRTIGHT SYSTEMS VERIFICATION UNIT CHECKS ⚡\n")
    unittest.main()
