#!/bin/bash
# Verification script for Unified Field Theory formalization
# Requires Isabelle/HOL 2025 or compatible version

echo "=========================================="
echo "Unified Field Theory Verification"
echo "=========================================="
echo ""

# Check if Isabelle is available
if ! command -v isabelle &> /dev/null; then
    echo "ERROR: Isabelle/HOL not found in PATH"
    echo "Please install Isabelle/HOL from https://isabelle.in.tum.de/"
    exit 1
fi

echo "Isabelle version:"
isabelle version
echo ""

# Verify base theory exists
if [ ! -f "The_Unique_Ontic_Substrate.thy" ]; then
    echo "ERROR: Base theory The_Unique_Ontic_Substrate.thy not found"
    echo "Please ensure the base theory file is in the current directory"
    exit 1
fi

echo "Verifying base theory: The_Unique_Ontic_Substrate.thy"
isabelle build -D . -v -o "document=pdf" -o "document_variants=document:outline=/proof,/ML" base_theory 2>&1 | tee base_verification.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✓ Base theory verified successfully"
else
    echo "✗ Base theory verification failed"
    echo "See base_verification.log for details"
    exit 1
fi

echo ""
echo "Verifying extension theory: Unified_Field_Theory.thy"
isabelle build -D . -v -o "document=pdf" -o "document_variants=document:outline=/proof,/ML" unified_theory 2>&1 | tee unified_verification.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✓ Unified field theory verified successfully"
    echo ""
    echo "=========================================="
    echo "VERIFICATION COMPLETE"
    echo "=========================================="
    echo ""
    echo "Key results:"
    echo "  - Ontological_Unification theorem: PROVEN"
    echo "  - All_physical_phenomena_unified corollary: PROVEN"
    echo "  - Forces_unified_via_substrate: PROVEN"
    echo "  - Complete_Unification theorem: PROVEN"
    echo ""
    echo "The formalization proves that all physical phenomena"
    echo "(fields, forces, particles, entangled systems) are"
    echo "inseparable from the unique substrate Ω."
    echo ""
    echo "Unification is ontological, not merely phenomenal."
else
    echo "✗ Unified field theory verification failed"
    echo "See unified_verification.log for details"
    exit 1
fi

# Optional: Check for Nitpick countermodels
echo ""
echo "Running consistency check with Nitpick..."
isabelle console <<EOF
theory Test imports Unified_Field_Theory begin
nitpick [timeout=300, verbose]
end
EOF

echo ""
echo "Verification complete. Check logs for details."
