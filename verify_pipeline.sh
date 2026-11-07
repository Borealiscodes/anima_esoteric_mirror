#!/usr/bin/env bash
# verify_pipeline.sh
# Phase IX Architecture: Master Verification & Validation Harness

# Enforce immediate exit on any sub-command failures
set -e

# Define ANSI terminal color configuration layout profiles
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0;0m' # No Color

clear
echo -e "${CYAN}================================================================================"${NC}
echo -e "${CYAN}🌀 ANIMA CORE × NDH-SOVEREIGNTY — MASTER RUNTIME VERIFICATION LOOP"${NC}
echo -e "${CYAN}================================================================================"${NC}
echo -e "System Time: $(date)"
echo -e "Hardware Architecture Target: $(uname -m)"

# 1. PRECONDITION GATE: Validate operational local directory topology
echo -e "\n${YELLOW}[PHASE I: RUNTIME ENVIRONMENT INTEGRITY VERIFICATION]${NC}"
mkdir -p data config src tests

if [ ! -f "src/math_engine.py" ] && [ ! -f "core.py" ]; then
    echo -e "${RED}[✗] CRITICAL ERROR: Core mathematical solver primitives not detected in workspace paths.${NC}"
    exit 1
fi
echo -e "${GREEN}[✓] Structural workspace topology verified nominal.${NC}"

# 2. CALIBRATION GATE: Validate visual grammar configuration availability
if [ -f "config/visual_grammar.json" ]; then
    echo -e "${GREEN}[✓] config/visual_grammar.json system limits successfully loaded.${NC}"
else
    echo -e "${YELLOW}[!] WARNING: System limits config missing. Falling back to core hard-coded bounds.${NC}"
fi

# 3. COMPILATION & TESTING GATE: Invoke strict programmatic boundary unit assertions
echo -e "\n${YELLOW}[PHASE II: EXECUTING SOVEREIGN BOUNDARY OVERRIDE TEST ENCLAVE]${NC}"

if [ -f "tests/test_boundary_overrides.py" ]; then
    python3 -m unittest tests/test_boundary_overrides.py -v
else
    # Fallback if tests are located in root directory
    python3 test_boundary_overrides.py -v
fi

# 4. SYSTEM INTELLIGENCE CHECK: Run a live integration profile test cycle
echo -e "\n${YELLOW}[PHASE III: ACTIVE PIPELINE EXECUTION PROFILE CYCLE]${NC}"
echo -e "Spinning up local math core, append-only registry, and ASCII terminal HUD..."

python3 << 'EOF'
import sys
import os
import numpy as np

# Bind target source paths smoothly
sys.path.append(os.path.abspath('.'))

try:
    # Handle varying repository naming conventions transparently
    if os.path.exists("core.py"):
        from core import SubstrateMatrixSolver
    else:
        from src.math_engine import SubstrateMatrixSolver
        
    from src.persistence import SovereignPersistenceVault
    from src.display import SovereignTerminalDisplay

    # Setup valid 9x9 graph Laplacian architecture
    adjacency = np.ones((9, 9)) - np.eye(9)
    degree = np.diag(np.sum(adjacency, axis=1))
    L = degree - adjacency
    W_in = np.eye(9) * 0.1

    # Instantiate objects
    solver = SubstrateMatrixSolver()
    vault = SovereignPersistenceVault("data/anima_shadow_registry.db")
    hud = SovereignTerminalDisplay("config/visual_grammar.json")

    # Ingest baseline environmental noise frame
    np.random.seed(1337)
    ambient_noise = np.random.normal(0.0, 0.1, 9)
    
    # Process unified step delta
    R_next, ternary_matrix, telemetry = solver.execute_choreography_step(L, W_in, ambient_noise)
    
    # Mock haptic parameter vector for persistence registration
    haptics = (0.2, 0.3)
    
    # Commit compressed frame straight to local shadow storage
    row_id = vault.commit_state_frame(R_next, ternary_matrix, telemetry)
    
    # Render final validation output to console
    print(hud.render_mandala_hud(R_next, telemetry))
    print(f"\n\033[0;32m[✓] Production iteration complete. Shadow database logged step entry ID: {row_id}\033[0;0m")

except Exception as e:
    print(f"\033[0;31m[✗] CRITICAL ERROR: Integration verification cycle collapsed: {e}\033[0;0m")
    sys.exit(1)
EOF

echo -e "\n${CYAN}================================================================================"${NC}
echo -e "${GREEN} ☸️  SYSTEM ALIGNMENT Airtight: ALL CORES OPERATING IN ŚĀNTA EQUILIBRIUM${NC}"
echo -e "${CYAN}================================================================================"${NC}
