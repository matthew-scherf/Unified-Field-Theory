#!/usr/bin/env python3
"""
Structural analysis of Unified Field Theory formalization
Validates syntax, counts definitions, and checks dependencies
"""

import re
from pathlib import Path
from collections import defaultdict

def analyze_theory_file(filepath):
    """Analyze an Isabelle theory file for structural properties"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    results = {
        'filename': filepath.name,
        'total_lines': len(content.split('\n')),
        'sections': [],
        'axioms': [],
        'lemmas': [],
        'theorems': [],
        'corollaries': [],
        'type_declarations': [],
        'constants': [],
        'imports': []
    }
    
    # Find imports
    import_match = re.search(r'imports\s+([\w\s]+)', content)
    if import_match:
        results['imports'] = import_match.group(1).split()
    
    # Find sections
    sections = re.findall(r'section\s*⟨(.+?)⟩', content)
    results['sections'] = sections
    
    # Find type declarations
    typedecls = re.findall(r'typedecl\s+(\w+)', content)
    results['type_declarations'] = typedecls
    
    # Find constants
    const_blocks = re.findall(r'consts\s+(.*?)(?=axiomatization|section|theorem|lemma|end)', content, re.DOTALL)
    for block in const_blocks:
        consts = re.findall(r'(\w+)\s*::', block)
        results['constants'].extend(consts)
    
    # Find axioms
    axiom_matches = re.finditer(r'(\w+):\s*"(.+?)"(?=\s+and|\s+axiomatization)', content, re.DOTALL)
    for match in axiom_matches:
        results['axioms'].append(match.group(1))
    
    # Find lemmas
    lemmas = re.findall(r'lemma\s+(\w+):', content)
    results['lemmas'] = lemmas
    
    # Find theorems
    theorems = re.findall(r'theorem\s+(\w+):', content)
    results['theorems'] = theorems
    
    # Find corollaries
    corollaries = re.findall(r'corollary\s+(\w+):', content)
    results['corollaries'] = corollaries
    
    return results

def print_analysis(analysis):
    """Pretty print the analysis results"""
    print(f"\n{'='*70}")
    print(f"Analysis of {analysis['filename']}")
    print(f"{'='*70}\n")
    
    print(f"Total lines: {analysis['total_lines']}")
    print(f"Imports: {', '.join(analysis['imports'])}\n")
    
    print(f"Sections ({len(analysis['sections'])}):")
    for i, section in enumerate(analysis['sections'], 1):
        print(f"  {i}. {section}")
    
    print(f"\nType declarations ({len(analysis['type_declarations'])}):")
    for typ in analysis['type_declarations']:
        print(f"  - {typ}")
    
    print(f"\nConstants ({len(analysis['constants'])}):")
    for const in analysis['constants']:
        print(f"  - {const}")
    
    print(f"\nAxioms ({len(analysis['axioms'])}):")
    for axiom in analysis['axioms']:
        print(f"  - {axiom}")
    
    print(f"\nLemmas ({len(analysis['lemmas'])}):")
    for lemma in analysis['lemmas']:
        print(f"  - {lemma}")
    
    print(f"\nTheorems ({len(analysis['theorems'])}):")
    for theorem in analysis['theorems']:
        print(f"  - {theorem}")
    
    if analysis['corollaries']:
        print(f"\nCorollaries ({len(analysis['corollaries'])}):")
        for corollary in analysis['corollaries']:
            print(f"  - {corollary}")

def validate_dependencies(base_analysis, extension_analysis):
    """Check that extension properly depends on base theory"""
    print(f"\n{'='*70}")
    print("Dependency Validation")
    print(f"{'='*70}\n")
    
    # Check if extension imports base
    base_name = base_analysis['filename'].replace('.thy', '')
    if base_name in extension_analysis['imports']:
        print(f"✓ Extension properly imports base theory '{base_name}'")
    else:
        print(f"✗ WARNING: Extension does not import base theory '{base_name}'")
        return False
    
    # Check that extension uses base concepts
    base_constants = set(base_analysis['constants'])
    extension_content = Path(extension_analysis['filename']).read_text()
    
    used_base_constants = []
    for const in base_constants:
        if const in extension_content:
            used_base_constants.append(const)
    
    print(f"\n✓ Extension uses {len(used_base_constants)} constants from base theory:")
    for const in sorted(used_base_constants)[:10]:  # Show first 10
        print(f"  - {const}")
    if len(used_base_constants) > 10:
        print(f"  ... and {len(used_base_constants) - 10} more")
    
    return True

def check_theorem_structure(analysis):
    """Verify theorem structure and coverage"""
    print(f"\n{'='*70}")
    print("Theorem Structure Analysis")
    print(f"{'='*70}\n")
    
    total_proofs = len(analysis['lemmas']) + len(analysis['theorems']) + len(analysis['corollaries'])
    print(f"Total proven results: {total_proofs}")
    print(f"  - Lemmas: {len(analysis['lemmas'])}")
    print(f"  - Theorems: {len(analysis['theorems'])}")
    print(f"  - Corollaries: {len(analysis['corollaries'])}")
    
    # Check for key theorems in unified field theory
    key_theorems = [
        'Ontological_Unification',
        'Complete_Unification',
        'Forces_unified_via_substrate',
        'Framework_accommodates_all_forces',
        'Framework_explains_entanglement'
    ]
    
    print(f"\nKey unification theorems:")
    for thm in key_theorems:
        if thm in analysis['theorems']:
            print(f"  ✓ {thm}")
        else:
            print(f"  ✗ MISSING: {thm}")
    
    # Check for supporting lemmas
    key_lemmas = [
        'Field_channels_structure_presentation',
        'Gauge_indexing_preserves_nonduality',
        'Force_phenomena_nondual',
        'Entanglement_nonlocal_via_substrate'
    ]
    
    print(f"\nKey supporting lemmas:")
    for lem in key_lemmas:
        if lem in analysis['lemmas']:
            print(f"  ✓ {lem}")
        else:
            print(f"  ✗ MISSING: {lem}")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║   Unified Field Theory - Structural Analysis                         ║
║   Non-Dual Ontology Formalization in Isabelle/HOL                   ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Analyze base theory
    base_file = Path('The_Unique_Ontic_Substrate.thy')
    if base_file.exists():
        print("Analyzing base theory...")
        base_analysis = analyze_theory_file(base_file)
        print_analysis(base_analysis)
    else:
        print(f"WARNING: Base theory file '{base_file}' not found")
        base_analysis = None
    
    # Analyze extension
    extension_file = Path('Unified_Field_Theory.thy')
    if extension_file.exists():
        print("\nAnalyzing unified field theory extension...")
        extension_analysis = analyze_theory_file(extension_file)
        print_analysis(extension_analysis)
        check_theorem_structure(extension_analysis)
        
        # Validate dependencies if base exists
        if base_analysis:
            validate_dependencies(base_analysis, extension_analysis)
    else:
        print(f"ERROR: Extension theory file '{extension_file}' not found")
        return 1
    
    print(f"\n{'='*70}")
    print("Summary")
    print(f"{'='*70}\n")
    
    if base_analysis:
        print(f"Base theory: {len(base_analysis['axioms'])} axioms, "
              f"{len(base_analysis['lemmas'])} lemmas, "
              f"{len(base_analysis['theorems'])} theorems")
    
    if extension_analysis:
        print(f"Extension: {len(extension_analysis['axioms'])} axioms, "
              f"{len(extension_analysis['lemmas'])} lemmas, "
              f"{len(extension_analysis['theorems'])} theorems")
    
    print(f"\n{'='*70}")
    print("Structural Analysis Complete")
    print(f"{'='*70}")
    print("\nNext steps:")
    print("1. Verify theories with Isabelle/HOL: ./verify_unified_theory.sh")
    print("2. Review README.md for detailed documentation")
    print("3. Check individual theorem proofs in the .thy files")
    
    return 0

if __name__ == '__main__':
    exit(main())
