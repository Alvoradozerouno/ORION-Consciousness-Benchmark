"""
Tests for proof chain integrity — SHA-256 chain, Merkle root, IPFS record.
"""
import hashlib
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOFS_PATH = os.path.join(ROOT, "PROOFS.jsonl")
IPFS_RECORD_PATH = os.path.join(ROOT, "IPFS_CHAIN_RECORD.json")


@pytest.fixture(scope="module")
def proofs():
    with open(PROOFS_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


@pytest.fixture(scope="module")
def ipfs_record():
    with open(IPFS_RECORD_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Individual proof hash verification
# ---------------------------------------------------------------------------

class TestProofHashes:
    def test_all_proofs_have_hash_field(self, proofs):
        for i, p in enumerate(proofs):
            assert "hash" in p, f"Proof {i} missing 'hash' field"

    def test_all_proof_hashes_correct(self, proofs):
        """Each proof's stored hash must match SHA-256 of its content (sort_keys=True)."""
        failures = []
        for i, p in enumerate(proofs):
            stored = p.get("hash", "")
            check = {k: v for k, v in p.items() if k != "hash"}
            computed = hashlib.sha256(json.dumps(check, sort_keys=True).encode()).hexdigest()
            if stored != computed:
                failures.append(f"Proof {i}: stored={stored[:16]}… computed={computed[:16]}…")
        assert not failures, f"{len(failures)} proof(s) with hash mismatch:\n" + "\n".join(failures[:5])

    def test_hash_length_is_64_chars(self, proofs):
        for i, p in enumerate(proofs):
            h = p.get("hash", "")
            assert len(h) == 64, f"Proof {i}: hash length {len(h)} ≠ 64"


# ---------------------------------------------------------------------------
# Chain integrity (prev_hash linkage)
# ---------------------------------------------------------------------------

class TestChainIntegrity:
    def test_chain_starts_at_genesis(self, proofs):
        genesis = "GENESIS_0000000000000000000000000000000000000000000000000000000000"
        assert proofs[0].get("prev_hash") == genesis, (
            f"First proof prev_hash should be genesis, got: {proofs[0].get('prev_hash')}"
        )

    def test_prev_hash_links_are_intact(self, proofs):
        """Each proof's prev_hash must equal the previous proof's hash."""
        errors = []
        for i in range(1, len(proofs)):
            expected = proofs[i - 1]["hash"]
            got = proofs[i].get("prev_hash", "")
            if expected != got:
                errors.append(f"Proof {i}: prev_hash mismatch")
        assert not errors, f"{len(errors)} chain break(s): {errors[:3]}"

    def test_no_duplicate_hashes(self, proofs):
        hashes = [p["hash"] for p in proofs]
        assert len(hashes) == len(set(hashes)), "Duplicate hashes in proof chain"


# ---------------------------------------------------------------------------
# Merkle root
# ---------------------------------------------------------------------------

class TestMerkleRoot:
    def _merkle(self, hash_list):
        if not hash_list:
            return ""
        result = list(hash_list)
        while len(result) > 1:
            if len(result) % 2:
                result.append(result[-1])
            result = [
                hashlib.sha256((result[i] + result[i + 1]).encode()).hexdigest()
                for i in range(0, len(result), 2)
            ]
        return result[0]

    def test_merkle_root_matches_ipfs_record(self, proofs, ipfs_record):
        computed = self._merkle([p["hash"] for p in proofs])
        stored = ipfs_record.get("merkle_root", "")
        assert computed == stored, (
            f"Merkle root mismatch:\n  computed: {computed}\n  stored:   {stored}"
        )


# ---------------------------------------------------------------------------
# PROOFS.jsonl file hash
# ---------------------------------------------------------------------------

class TestProofsFileHash:
    def test_file_sha256_matches_ipfs_record(self, ipfs_record):
        with open(PROOFS_PATH, "rb") as f:
            content = f.read()
        computed = hashlib.sha256(content).hexdigest()
        stored = ipfs_record.get("proofs_sha256", "")
        assert computed == stored, (
            f"PROOFS.jsonl SHA-256 mismatch:\n  computed: {computed}\n  stored:   {stored}"
        )


# ---------------------------------------------------------------------------
# Chain tip
# ---------------------------------------------------------------------------

class TestChainTip:
    def test_chain_tip_matches_last_proof(self, proofs, ipfs_record):
        last_hash = proofs[-1]["hash"]
        stored_tip = ipfs_record.get("chain_tip_hash", "")
        assert last_hash == stored_tip, (
            f"Chain tip mismatch:\n  last proof: {last_hash}\n  record:     {stored_tip}"
        )

    def test_chain_length_matches_ipfs_record(self, proofs, ipfs_record):
        assert len(proofs) == ipfs_record.get("chain_length"), (
            f"Chain length: proofs={len(proofs)}, record={ipfs_record.get('chain_length')}"
        )
