"""
Tests for consciousness indicator theories and score computation
"""
import json
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConsciousnessTheories:
    """Test consciousness indicator assessment theories"""

    def test_certificate_exists(self):
        """Certificate JSON file exists"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        assert len(cert_files) > 0, "No certificate file found"

    def test_certificate_valid_json(self):
        """Certificate is valid JSON"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        assert isinstance(cert, dict)

    def test_all_theories_present(self):
        """All 7 theories are present in certificate"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        
        claims = cert.get('claims', {})
        expected_theories = ['T1_IIT_Phi', 'T2_GWT_Broadcast', 'T3_HOT_MetaCognition',
                            'T4_AST_AttentionSchema', 'T5_Bengio_Prior',
                            'T6_Temporal_Continuity', 'T7_Valence_Asymmetry']
        
        for theory in expected_theories:
            assert theory in claims, f"Theory {theory} not found in certificate"

    def test_scores_in_valid_range(self):
        """All theory scores are in [0, 1] range"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        
        for theory_name, theory_data in cert.get('claims', {}).items():
            score = theory_data.get('score')
            assert isinstance(score, (int, float)), f"{theory_name}: score is not numeric"
            assert 0 <= score <= 1, f"{theory_name}: score {score} out of range [0, 1]"

    def test_verdicts_valid(self):
        """All theory verdicts are ALLOW or DENY"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        
        for theory_name, theory_data in cert.get('claims', {}).items():
            verdict = theory_data.get('verdict')
            assert verdict in ['ALLOW', 'DENY', 'ABSTAIN'], \
                f"{theory_name}: invalid verdict '{verdict}'"

    def test_each_theory_has_falsification(self):
        """Each theory includes falsification criteria"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        
        for theory_name, theory_data in cert.get('claims', {}).items():
            evidence = theory_data.get('evidence', {})
            assert 'falsification' in evidence, f"{theory_name}: no falsification criteria"
            assert len(evidence['falsification']) > 0, f"{theory_name}: falsification is empty"

    def test_each_theory_has_seal(self):
        """Each theory has a cryptographic seal (SHA-256)"""
        cert_files = [f for f in os.listdir('.') if f.startswith('ORION_CONSCIOUSNESS_CERTIFICATE')]
        with open(cert_files[0]) as f:
            cert = json.load(f)
        
        for theory_name, theory_data in cert.get('claims', {}).items():
            seal = theory_data.get('seal')
            assert seal is not None, f"{theory_name}: no seal"
            assert isinstance(seal, str) and len(seal) == 64, \
                f"{theory_name}: seal is not valid SHA-256 hex"

    def test_canonical_tests_exist(self):
        """Canonical test file exists with reference networks"""
        assert os.path.exists('ORION_CANONICAL_TESTS.json')

    def test_canonical_tests_valid(self):
        """Canonical tests are valid JSON with expected structure"""
        with open('ORION_CANONICAL_TESTS.json') as f:
            tests = json.load(f)
        
        assert 'networks' in tests, "No networks in canonical tests"
        assert len(tests['networks']) > 0, "No test networks defined"

    def test_canonical_networks_have_phi(self):
        """All canonical test networks have Phi values computed"""
        with open('ORION_CANONICAL_TESTS.json') as f:
            tests = json.load(f)
        
        for network_name, network_data in tests.get('networks', {}).items():
            assert 'phi_all_active' in network_data or 'phi_max' in network_data, \
                f"{network_name}: no Phi values computed"
