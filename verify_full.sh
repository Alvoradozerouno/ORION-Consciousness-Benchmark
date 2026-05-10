#!/usr/bin/env bash
# verify_full.sh – run the Isabelle/HOL proof check for EIRA_Refinement_Complete
# Usage: ./verify_full.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}/isabelle"

isabelle build -v -d . EIRA_Refinement_Complete
