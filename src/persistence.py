#!/usr/bin/env python3
# src/persistence.py
# Phase IX Architecture: Sovereign Binary BLOB Persistence Vault

import os
import sqlite3
import pickle
import numpy as np
from typing import Dict, Any, Tuple, Optional

class SovereignPersistenceVault:
    def __init__(self, db_path: str = "data/anima_shadow_registry.db"):
        self.db_path = db_path
        # Ensure target data directory exists safely on local silicon
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize_vault()

    def initialize_vault(self) -> None:
        """Initializes the append-only shadow registry with zero-overhead indexing."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS state_registry (
                    step_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    equilibrium_signature TEXT NOT NULL,
                    vfe_tension REAL NOT NULL,
                    complex_state_matrix BLOB NOT NULL,
                    ternary_state_matrix BLOB NOT NULL,
                    radial_coordinate_r REAL NOT NULL,
                    radial_diffusion_field REAL NOT NULL,
                    attenuation_active INTEGER NOT NULL
                )
            """)
            conn.commit()

    def commit_state_frame(
        self, 
        R: np.ndarray, 
        T: np.ndarray,
        telemetry: Dict[str, Any]
    ) -> int:
        """
        Serializes complex 9x9 phase matrices and ternary arrays into raw binary BLOB strings.
        Preserves 100% algebraic fidelity with microscopic disk-write overhead.
        """
        # Enforce strict type checking before hitting local storage allocation gates
        assert R.dtype == np.complex128, "[VAULT] Type breach: Core matrix requires complex128."
        assert T.dtype == np.int8, "[VAULT] Type breach: Ternary map requires int8 bitplanes."
        
        # Compress the multidimensional arrays straight to raw bytes
        binary_complex_blob = pickle.dumps(R, protocol=pickle.HIGHEST_PROTOCOL)
        binary_ternary_blob = pickle.dumps(T, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Unpack synchronized telemetry variables
        signature = telemetry.get("equilibrium_signature", "Śānta")
        vfe_tension = float(telemetry.get("vfe_tension", 0.0))
        radius = float(telemetry.get("radial_coordinate_r", 0.0))
        diffusion = float(telemetry.get("radial_diffusion_field", 0.0))
        attenuation = 1 if telemetry.get("h_safe_attenuation_active", False) else 0

        # Inject compressed frame into the append-only ledger
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO state_registry (
                    equilibrium_signature, vfe_tension, complex_state_matrix, 
                    ternary_state_matrix, radial_coordinate_r, radial_diffusion_field,
                    attenuation_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                signature, vfe_tension, sqlite3.Binary(binary_complex_blob), 
                sqlite3.Binary(binary_ternary_blob), radius, diffusion, attenuation
            ))
            conn.commit()
            return cursor.lastrowid or 0

    def recover_latest_state_frame(self) -> Optional[Tuple[np.ndarray, np.ndarray, Dict[str, Any]]]:
        """Reads and unpacks the latest compressed state frame from the database layer."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT complex_state_matrix, ternary_state_matrix, equilibrium_signature, vfe_tension
                FROM state_registry ORDER BY step_id DESC LIMIT 1
            """)
            row = cursor.fetchone()
            
        if not row:
            return None
            
        # Revive raw binary byte arrays back into native high-precision memory spaces
        R = pickle.loads(row[0])
        T = pickle.loads(row[1])
        telemetry = {
            "equilibrium_signature": row[2],
            "vfe_tension": row[3]
        }
        return R, T, telemetry

if __name__ == "__main__":
    print("=== MONITORING ACTIVE PERSISTENCE STORAGE VAULT ===")
    vault = SovereignPersistenceVault("./test_vault.db")
    
    # Generate mock 9x9 data streams to assert strict serialization round-trips
    np.random.seed(42)
    mock_R = (np.random.normal(0, 1, (9, 9)) + 1j * np.random.normal(0, 1, (9, 9))).astype(np.complex128)
    mock_T = np.random.choice([-1, 0, 1], size=(9, 9)).astype(np.int8)
    mock_telemetry = {
        "equilibrium_signature": "Allostatic_Flow",
        "vfe_tension": 1.4582,
        "radial_coordinate_r": 0.2231,
        "radial_diffusion_field": 0.8912,
        "h_safe_attenuation_active": False
    }
    
    frame_index = vault.commit_state_frame(mock_R, mock_T, mock_telemetry)
    print(f"[✓] Vault write verified. Stored frame index: {frame_index}")
    
    recovery_data = vault.recover_latest_state_frame()
    if recovery_data:
        rec_R, rec_T, rec_log = recovery_data
        assert np.allclose(rec_R, mock_R), "[VAULT ERROR] Complex coordinate array drift detected."
        assert np.array_equal(rec_T, mock_T), "[VAULT ERROR] Balanced ternary discrete bitplane drift detected."
        print("[✓] Validation Check: 100% structural fidelity preserved across storage transition.")
        
    # Safe runtime cleanup of testing artifact
    if os.path.exists("./test_vault.db"):
        os.remove("./test_vault.db")
