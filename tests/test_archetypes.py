# tests/test_archetypes.py
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.validate_workspace import validate_workspace

def test_all_archetypes_are_valid():
    archetypes_dir = Path(__file__).parent.parent / "_config" / "archetypes"
    assert archetypes_dir.is_dir()
    
    archetypes = [d for d in archetypes_dir.iterdir() if d.is_dir()]
    assert len(archetypes) >= 5, f"Found only {len(archetypes)} archetypes"
    
    for arch in archetypes:
        valid, errors = validate_workspace(arch)
        assert valid, f"Archetype '{arch.name}' failed validation: {errors}"
