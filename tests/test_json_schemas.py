"""
Tests for JSON schema validation and data structure consistency
"""
import json
import glob
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestJSONSchemas:
    """Validate JSON files against expected schemas"""

    def test_ipfs_chain_record_structure(self):
        """IPFS_CHAIN_RECORD.json has required fields"""
        with open('IPFS_CHAIN_RECORD.json') as f:
            record = json.load(f)
        
        required_fields = ['timestamp', 'version', 'chain_length', 'merkle_root',
                          'chain_tip_hash', 'chain_genesis', 'proofs_sha256']
        
        for field in required_fields:
            assert field in record, f"Missing required field: {field}"

    def test_proof_structure(self):
        """Each proof has required cryptographic fields (chain integrity)"""
        # Essential fields for chain integrity - everything else is metadata
        essential_fields = ['chain_index', 'prev_hash', 'hash']
        
        with open('PROOFS.jsonl') as f:
            for i, line in enumerate(f):
                if line.strip():
                    proof = json.loads(line)
                    for field in essential_fields:
                        assert field in proof, f"Proof {i}: missing essential field {field}"

    def test_ecosystem_json_valid(self):
        """ECOSYSTEM.json is valid and parseable"""
        assert os.path.exists('ECOSYSTEM.json')
        with open('ECOSYSTEM.json') as f:
            ecosystem = json.load(f)
        assert isinstance(ecosystem, dict)

    def test_assessment_template_valid(self):
        """assessment_template.json is valid structure"""
        assert os.path.exists('assessment_template.json')
        with open('assessment_template.json') as f:
            template = json.load(f)
        assert isinstance(template, dict)

    def test_no_duplicate_chain_indices(self):
        """No duplicate chain_index values in PROOFS.jsonl"""
        indices = set()
        with open('PROOFS.jsonl') as f:
            for i, line in enumerate(f):
                if line.strip():
                    proof = json.loads(line)
                    chain_idx = proof.get('chain_index')
                    assert chain_idx not in indices, \
                        f"Duplicate chain_index {chain_idx} at line {i}"
                    indices.add(chain_idx)

    def test_chain_indices_sequential(self):
        """Chain indices are sequential from 0 to chain_length-1"""
        indices = []
        with open('PROOFS.jsonl') as f:
            for line in f:
                if line.strip():
                    proof = json.loads(line)
                    indices.append(proof.get('chain_index'))
        
        expected = list(range(len(indices)))
        assert indices == expected, f"Chain indices not sequential: {indices[:5]}..."
