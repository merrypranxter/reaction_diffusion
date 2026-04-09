"""
Test preset parameter validity.
"""
import json
import pytest
from pathlib import Path


class TestPresetJSON:
    """Validate preset JSON files."""
    
    def test_pearson_types_loads(self):
        """Pearson types JSON should load and validate."""
        preset_path = Path(__file__).parent.parent / "presets" / "pearson-types.json"
        with open(preset_path) as f:
            data = json.load(f)
        
        assert data["model"] == "gray-scott"
        assert "pearson_types" in data
        assert len(data["pearson_types"]) == 17  # 17 types total
    
    def test_all_types_have_required_fields(self):
        """Each type should have required fields."""
        preset_path = Path(__file__).parent.parent / "presets" / "pearson-types.json"
        with open(preset_path) as f:
            data = json.load(f)
        
        required = ["type", "name", "F", "k", "wolfram_class", "description"]
        for ptype in data["pearson_types"]:
            for field in required:
                assert field in ptype, f"{ptype.get('type', 'unknown')} missing {field}"
            
            # Validate ranges
            assert 0 < ptype["F"] < 0.2, f"{ptype['type']} F out of range"
            assert 0 < ptype["k"] < 0.1, f"{ptype['type']} k out of range"
    
    def test_wolfram_classes_valid(self):
        """Wolfram classes should be valid values."""
        preset_path = Path(__file__).parent.parent / "presets" / "pearson-types.json"
        with open(preset_path) as f:
            data = json.load(f)
        
        valid_classes = [1, 2, "2-a", 3, 4]
        for ptype in data["pearson_types"]:
            assert ptype["wolfram_class"] in valid_classes
    
    def test_named_behaviors_loads(self):
        """Named behaviors JSON should load."""
        preset_path = Path(__file__).parent.parent / "presets" / "named-behaviors.json"
        with open(preset_path) as f:
            data = json.load(f)
        
        assert "named_behaviors" in data
        assert len(data["named_behaviors"]) >= 9  # At least the classics
    
    def test_no_duplicate_names(self):
        """No duplicate type or behavior names."""
        preset_path = Path(__file__).parent.parent / "presets" / "pearson-types.json"
        with open(preset_path) as f:
            data = json.load(f)
        
        types = [p["type"] for p in data["pearson_types"]]
        assert len(types) == len(set(types)), "Duplicate type symbols"
        
        names = [p["name"] for p in data["pearson_types"]]
        assert len(names) == len(set(names)), "Duplicate type names"
