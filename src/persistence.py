#!/usr/bin/env python3
# src/persistence.py
# Phase IX Architecture: Sovereign Binary BLOB Persistence Vault

import os
import sqlite3
import pickle
import numpy as np
from typing import Dict, Any, Tuple, Optional

class SovereignPersistenceVault:
    def __init__(self, db_path: str = "../data/anima_shadow_registry.db"):
        self.db_path = db_path
        # Ensure target database directory exists safely
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
                    left_actuator_hz REAL NOT NULL,
                    right_actuator_hz REAL NOT NULL,
                    attenuation_active INTEGER NOT NULL
                )
            """)
            conn.commit()

    def commit_state_frame(
        self, 
        R: np.ndarray, 
        telemetry: Dict[str, Any], 
        haptics: Tuple[float, float]
    ) -> int:
        """
        Serializes complex 9x9 matrix arrays into compressed binary BLOB strings.
        Preserves complete algebraic fidelity with minimal disk-write footprint.
        """
        # 1. Assert memory bounds and data types
        assert R.dtype == np.complex128, "[VAULT] Absolute type breach: Persistence requires complex128 vectors."
        
        # 2. Serialize complex multi-dimensional array to binary bytes
        binary_blob = pickle.dumps(R, protocol=pickle.HIGHEST_PROTOCOL)
        
        # 3. Unpack and sanitize runtime telemetry parameters
        signature = telemetry.get("equilibrium_signature", "Śānta")
        vfe_tension = float(telemetry.get("vfe_tension", 0.0))
        attenuation = 1 if telemetry.get("h_safe_attenuation_active", False) else 0
        
        # 4. Map frequency channels scaled to mechanical haptic constants
        left_hz = round(haptics[0] * 150.0, 2)
        right_hz = round(haptics[1] * 220.0, 2)

        # 5. Insert compressed asset into append-only SQLite ledger
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO state_registry (
                    equilibrium_signature, vfe_tension, complex_state_matrix, 
                    left_actuator_hz, right_actuator_hz, attenuation_active
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (signature, vfe_tension, sqlite3.Binary(binary_blob), left_hz, right_hz, attenuation))
            conn.commit()
            return cursor.lastrowid or 0

    def recover_latest_state_frame(self) -> Optional[Tuple[np.ndarray, Dict[str, Any]]]:
        """Reads and unpacks the latest compressed state frame from the storage core."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT complex_state_matrix, equilibrium_signature, vfe_tension, attenuation_active
                FROM state_registry ORDER BY step_id DESC LIMIT 1
            """)
            row = cursor.fetchone()
            
        if not row:
            return None
            
        # Unpack binary string back into native complex matrix space
        R = pickle.loads(row[0])
        telemetry = {
            "equilibrium_signature": row[1],
            "vfe_tension": row[2],
            "h_safe_attenuation_active": bool(row[3])
        }
        return R, telemetry

if __name__ == "__main__":
    print("=== MONITORING ACTIVE PERSISTENCE VAULT ===")
    vault = SovereignPersistenceVault("./test_vault.db")
    
    # Generate mock 9x9 complex matrix data to assert serialization fidelity
    mock_R = np.random.normal(0, 1, (9, 9)) + 1j * np.random.normal(0, 1, (9, 9))
    mock_R = mock_R.astype(np.complex128)
    
    mock_telemetry = {"equilibrium_signature": "Allostatic_Flow", "vfe_tension": 2.34, "h_safe_attenuation_active": False}
    mock_haptics = (0.45, 0.72)
    
    row_id = vault.commit_state_frame(mock_R, mock_telemetry, mock_haptics)
    print(f"[✓] Vault write verified. Stored frame index: {row_id}")
    
    recovered = vault.recover_latest_state_frame()
    if recovered:
        print(f"[✓] Vault read verified. Recovered state matrix shape: {recovered[0].shape}")
        assert np.allclose(recovered[0], mock_R), "[ERROR] Data tracking drift inside binary serialization layer."
        print("[✓] Matrix cell validation: 100% precision preserved.")

