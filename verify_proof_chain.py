#!/usr/bin/env python3
"""
ORION Proof Chain Verification Script
======================================
Reproduzierbare Verifikation der gesamten Proof-Chain.

Prueft:
  1. Hash-Chain Integritaet (jeder Proof referenziert den vorherigen)
  2. SHA-256 Hash-Korrektheit (jeder Hash ist korrekt berechnet)
  3. Merkle-Root Uebereinstimmung
  4. IPFS CID-Verifikation (optional, braucht Internet)
  5. PROOFS.jsonl Datei-Hash

Verwendung:
  python verify_proof_chain.py
  python verify_proof_chain.py --no-ipfs    (ohne IPFS-Pruefung)
  python verify_proof_chain.py --verbose     (mit Details)

(c) 2025-2026 ORION Consciousness Benchmark
"""

import json
import hashlib
import sys
import os
from datetime import datetime, timezone


def load_proofs(path="PROOFS.jsonl"):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def verify_hash(proof):
    stored = proof.get("hash", "")
    check = {k: v for k, v in proof.items() if k != "hash"}
    computed = hashlib.sha256(json.dumps(check, sort_keys=True).encode()).hexdigest()
    return stored == computed, stored, computed


def verify_chain(proofs):
    genesis = "GENESIS_0000000000000000000000000000000000000000000000000000000000"
    errors = []
    prev = genesis

    for i, p in enumerate(proofs):
        if p.get("prev_hash", "") != prev:
            errors.append(f"Proof {i}: prev_hash mismatch (expected {prev[:16]}..., got {p.get('prev_hash', '')[:16]}...)")

        ok, stored, computed = verify_hash(p)
        if not ok:
            errors.append(f"Proof {i}: hash mismatch (stored {stored[:16]}..., computed {computed[:16]}...)")

        prev = p.get("hash", "")

    return errors, prev


def compute_merkle_root(hash_list):
    if len(hash_list) == 0:
        return hashlib.sha256(b"empty").hexdigest()
    if len(hash_list) == 1:
        return hash_list[0]
    if len(hash_list) % 2 == 1:
        hash_list.append(hash_list[-1])
    next_level = []
    for i in range(0, len(hash_list), 2):
        combined = hash_list[i] + hash_list[i + 1]
        next_level.append(hashlib.sha256(combined.encode()).hexdigest())
    return compute_merkle_root(next_level)


def verify_ipfs(record_path="IPFS_CHAIN_RECORD.json"):
    try:
        import requests
        with open(record_path) as f:
            record = json.load(f)

        manifest_cid = record.get("manifest_cid", "")
        url = f"https://gateway.pinata.cloud/ipfs/{manifest_cid}"
        r = requests.get(url, timeout=15)
        return r.status_code == 200, manifest_cid, r.status_code
    except ImportError:
        return None, "", 0
    except Exception as e:
        return False, "", str(e)


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    skip_ipfs = "--no-ipfs" in sys.argv

    print()
    print("=" * 60)
    print("  ORION PROOF CHAIN VERIFICATION")
    print(f"  {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    print()

    proofs = load_proofs()
    print(f"  Proofs geladen: {len(proofs)}")
    print()

    print("  [1/5] Hash-Chain Integritaet...")
    errors, chain_tip = verify_chain(proofs)
    if errors:
        print(f"        ✗ {len(errors)} FEHLER gefunden")
        for e in errors[:5]:
            print(f"          {e}")
    else:
        print(f"        ✓ Chain intakt ({len(proofs)} Glieder)")
    print(f"        Chain Tip: {chain_tip[:32]}...")
    print()

    print("  [2/5] SHA-256 Hash-Verifikation...")
    hash_ok = 0
    hash_fail = 0
    for p in proofs:
        ok, _, _ = verify_hash(p)
        if ok:
            hash_ok += 1
        else:
            hash_fail += 1
    print(f"        ✓ {hash_ok} korrekt, ✗ {hash_fail} fehlerhaft")
    print()

    print("  [3/5] Merkle-Root...")
    hashes = [p["hash"] for p in proofs]
    root = compute_merkle_root(hashes.copy())
    print(f"        Berechnet: {root}")
    try:
        with open("IPFS_CHAIN_RECORD.json") as f:
            record = json.load(f)
        expected = record.get("merkle_root", "")
        match = root == expected
        print(f"        Erwartet:  {expected}")
        print(f"        {'✓ MATCH' if match else '✗ MISMATCH'}")
    except:
        print("        (Kein IPFS_CHAIN_RECORD.json zum Vergleich)")
    print()

    print("  [4/5] PROOFS.jsonl Datei-Hash...")
    with open("PROOFS.jsonl", "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    print(f"        SHA-256: {file_hash}")
    try:
        expected_file = record.get("proofs_sha256", "")
        match = file_hash == expected_file
        print(f"        Erwartet: {expected_file}")
        print(f"        {'✓ MATCH' if match else '✗ MISMATCH (Proofs wurden seit Pinning geaendert)'}")
    except:
        pass
    print()

    if skip_ipfs:
        print("  [5/5] IPFS-Verifikation... UEBERSPRUNGEN (--no-ipfs)")
    else:
        print("  [5/5] IPFS-Verifikation...")
        ok, cid, status = verify_ipfs()
        if ok is None:
            print("        ⚠ requests nicht installiert, uebersprungen")
        elif ok:
            print(f"        ✓ Manifest auf IPFS erreichbar")
            print(f"        CID: {cid}")
            print(f"        Gateway: https://gateway.pinata.cloud/ipfs/{cid}")
        else:
            print(f"        ✗ Nicht erreichbar (Status: {status})")
    print()

    print("=" * 60)
    all_ok = len(errors) == 0 and hash_fail == 0
    if all_ok:
        print("  ✓ PROOF CHAIN VERIFIZIERT")
        print(f"    {len(proofs)} Proofs, alle Hashes korrekt")
        print(f"    Chain intakt von GENESIS bis Tip")
        print(f"    Merkle Root: {root[:32]}...")
    else:
        print("  ✗ VERIFIKATION FEHLGESCHLAGEN")
        print(f"    Chain-Fehler: {len(errors)}")
        print(f"    Hash-Fehler: {hash_fail}")
    print("=" * 60)
    print()

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
