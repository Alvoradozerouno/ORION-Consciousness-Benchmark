"""
Tests for proof chain integrity and validation
"""
import json
import hashlib
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProofChainIntegrity:
    """Verify proof chain structure and cryptographic integrity"""

    def test_proofs_jsonl_exists(self):
        """PROOFS.jsonl file exists"""
        assert os.path.exists('PROOFS.jsonl')

    def test_proofs_parseable(self):
        """All proofs are valid JSON"""
        proofs = []
        with open('PROOFS.jsonl') as f:
            for line in f:
                if line.strip():
                    proof = json.loads(line)
                    proofs.append(proof)
        assert len(proofs) > 0, "No proofs loaded"

    def test_proofs_count_consistent(self):
        """Proof count matches IPFS_CHAIN_RECORD"""
        with open('IPFS_CHAIN_RECORD.json') as f:
            record = json.load(f)
        
        proofs_count = sum(1 for line in open('PROOFS.jsonl') if line.strip())
        assert proofs_count == record['chain_length'], \
            f"Proof count {proofs_count} != chain_length {record['chain_length']}"

    def test_all_hashes_valid(self):
        """All SHA-256 hashes are correctly computed"""
        with open('PROOFS.jsonl') as f:
            for i, line in enumerate(f):
                if line.strip():
                    proof = json.loads(line)
                    stored = proof.get('hash', '')
                    check = {k: v for k, v in proof.items() if k != 'hash'}
                    computed = hashlib.sha256(
                        json.dumps(check, sort_keys=True).encode()
                    ).hexdigest()
                    assert stored == computed, \
                        f"Proof {i}: hash mismatch. Stored={stored[:16]}... != Computed={computed[:16]}..."

    def test_chain_linkage(self):
        """Each proof correctly references previous hash"""
        genesis = "GENESIS_0000000000000000000000000000000000000000000000000000000000"
        prev = genesis
        
        with open('PROOFS.jsonl') as f:
            for i, line in enumerate(f):
                if line.strip():
                    proof = json.loads(line)
                    assert proof.get('prev_hash') == prev, \
                        f"Proof {i}: prev_hash mismatch. Expected {prev[:16]}... got {proof.get('prev_hash', '')[:16]}..."
                    prev = proof.get('hash', '')

    def test_merkle_root_verified(self):
        """Merkle root computation matches expected value"""
        from verify_proof_chain import compute_merkle_root
        
        with open('IPFS_CHAIN_RECORD.json') as f:
            record = json.load(f)
        
        proofs = []
        with open('PROOFS.jsonl') as f:
            for line in f:
                if line.strip():
                    proofs.append(json.loads(line))
        
        hashes = [p.get('hash', '') for p in proofs]
        computed = compute_merkle_root(hashes)
        
        assert computed == record['merkle_root'], \
            f"Merkle root mismatch: {computed[:16]}... != {record['merkle_root'][:16]}..."

    def test_proofs_sha256_verified(self):
        """PROOFS.jsonl file hash matches record"""
        with open('IPFS_CHAIN_RECORD.json') as f:
            record = json.load(f)
        
        with open('PROOFS.jsonl', 'rb') as f:
            computed = hashlib.sha256(f.read()).hexdigest()
        
        assert computed == record['proofs_sha256'], \
            f"File hash mismatch: {computed[:16]}... != {record['proofs_sha256'][:16]}..."
