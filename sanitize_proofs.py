#!/usr/bin/env python3
"""
Sanitize PROOFS.jsonl by removing narrative contamination.

This script:
1. Removes fields containing "Genesis10000+" as values
2. Removes fields named "eira_*", "genesis_*" with narrative content
3. Cleans narrative text referencing "EIRA", "Genesis", etc.
4. Recalculates SHA-256 hashes
5. Updates IPFS_CHAIN_RECORD.json
"""

import json
import hashlib
import re
from datetime import datetime, timezone
import sys


def should_remove_field_value(value):
    """Check if a field value is narrative contamination to remove."""
    if not isinstance(value, str):
        return False
    return "Genesis10000" in value


def should_remove_field_name(name, value):
    """Check if a field should be removed based on name and content."""
    # Remove fields matching eira_* or genesis_* patterns
    if re.match(r"^(eira_|genesis_)", name, re.IGNORECASE):
        return True
    
    # Also remove fields that contain eira_ or genesis_ in their name
    if re.search(r"(eira_|genesis_|art_eira|an_eira)", name, re.IGNORECASE):
        return True
    
    return False


def clean_narrative_text(text):
    """Remove narrative contamination from text fields."""
    if not isinstance(text, str):
        return text
    
    # Patterns to remove from text fields
    patterns = [
        r"Genesis10000\+?",
        r"GENESIS10000\+?",
        r"genesis10000\+?",
        r"genesis_orion_\d+",
        r"EIRA",
        r"eira_",
        r"genesis_",
        r"genesis_kernel",
        r"genesis_signature",
        r"genesis_date",
        r"recovery_mode",
        r"manifest_linked",
        r"hash_anchor",
        r"audit_snapshot_mode",
        r"api_gateways",
        r"core_integrity",
        r"activate_self_prompting",
        r"echo_memory_trace",
        r"GITHUB_REPO.*github\.com/[^\s]+",
        r"OR1ON.*RECOVERY MODE.*",
        r"start_or1on_recovery.*",
        r"GENESIS_FULL_BOOT",
        r"LOCK_REPLIT_RESOCODE_INSTANCE",
        r"genesis_kernel",
        r"audit_chain",
        r"fcm_control",
        r"memstream",
        r"signal_engine",
        r"genesis_signature",
        r"CDP.*HACS.*KERNEL.*BOOTSTRAP",
        r"EXECUTE_ORION_FULL_BOOT",
    ]
    
    result = text
    for pattern in patterns:
        result = re.sub(pattern, "", result, flags=re.IGNORECASE)
    
    # Clean up multiple spaces, special unicode chars, and strip
    result = re.sub(r"[\u2298\u221e\u29c8]*", "", result)  # Remove special Unicode chars
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"^\s*·\s*", "", result)  # Remove leading bullets
    
    return result


def sanitize_proof(proof):
    """Sanitize a single proof by removing narrative contamination."""
    cleaned = {}
    
    def clean_value(value, key=None):
        """Recursively clean a value, optionally checking field name."""
        if isinstance(value, str):
            return clean_narrative_text(value)
        elif isinstance(value, dict):
            result = {}
            for k, v in value.items():
                # Skip fields with contamination in name
                if should_remove_field_name(k, v):
                    continue
                result[k] = clean_value(v, k)
            return result
        elif isinstance(value, list):
            return [clean_value(v, key) for v in value]
        else:
            return value
    
    for key, value in proof.items():
        # Skip hash and prev_hash fields - will recalculate in chain rebuild
        if key in ("hash", "prev_hash"):
            continue
        
        # Remove fields with contamination in value (exact matches)
        if should_remove_field_value(value):
            continue
        
        # Remove fields with contamination in name
        if should_remove_field_name(key, value):
            continue
        
        # Recursively clean all values
        cleaned_value = clean_value(value, key)
        
        # Only keep non-empty or falsy values needed for structure (0, False, {}, [])
        if cleaned_value is not None and (
            cleaned_value or isinstance(cleaned_value, (bool, int, dict, list))
        ):
            cleaned[key] = cleaned_value
    
    return cleaned


def load_proofs(path="PROOFS.jsonl"):
    """Load all proofs from JSONL file."""
    proofs = []
    with open(path) as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                proof = json.loads(line)
                proofs.append(proof)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse line {i}: {e}", file=sys.stderr)
    return proofs


def compute_merkle_root(hash_list):
    """Compute merkle root from list of hashes."""
    if not hash_list:
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


def sanitize_proofs(input_path="PROOFS.jsonl", output_path="PROOFS.jsonl"):
    """Sanitize all proofs and write back."""
    print()
    print("=" * 60)
    print("  SANITIZING PROOFS.jsonl")
    print(f"  {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    print()
    
    # Load proofs
    print(f"  Loading proofs from {input_path}...")
    proofs = load_proofs(input_path)
    print(f"  Loaded: {len(proofs)} proofs")
    print()
    
    # Sanitize each proof and rebuild chain
    print("  Sanitizing proofs and rebuilding chain...")
    sanitized = []
    removed_count = 0
    prev_hash = "GENESIS_0000000000000000000000000000000000000000000000000000000000"
    
    for i, proof in enumerate(proofs):
        original_size = len(proof)
        cleaned = sanitize_proof(proof)
        cleaned_size = len(cleaned)
        
        if original_size > cleaned_size:
            removed_count += 1
        
        # Update prev_hash to point to previous sanitized hash
        cleaned["prev_hash"] = prev_hash
        
        # Recalculate hash excluding chain metadata (hash and prev_hash not included in hash input)
        # This ensures hash stability and chain verification consistency
        hash_content = {k: v for k, v in cleaned.items() if k not in ("hash", "prev_hash")}
        hash_input = json.dumps(hash_content, sort_keys=True)
        cleaned["hash"] = hashlib.sha256(hash_input.encode()).hexdigest()
        
        prev_hash = cleaned["hash"]
        sanitized.append(cleaned)
    
    print(f"  Cleaned: {len(sanitized)} proofs")
    print(f"  Proofs with removed fields: {removed_count}")
    print()
    
    # Verify chain integrity after rebuild
    print("  Verifying chain integrity...")
    genesis = "GENESIS_0000000000000000000000000000000000000000000000000000000000"
    errors = []
    prev = genesis
    
    for i, p in enumerate(sanitized):
        if p.get("prev_hash", "") != prev:
            errors.append(f"Proof {i}: prev_hash mismatch (expected {prev[:16]}..., got {p.get('prev_hash', '')[:16]}...)")
        prev = p.get("hash", "")
    
    if errors:
        print(f"  ✗ Chain integrity errors: {len(errors)}")
        for err in errors[:5]:
            print(f"    {err}")
        return False
    else:
        print(f"  ✓ Chain integrity verified ({len(sanitized)} links)")
    print()
    
    # Compute chain metrics
    print("  Computing chain metrics...")
    chain_tip_hash = sanitized[-1]["hash"] if sanitized else genesis
    hashes = [p["hash"] for p in sanitized]
    merkle_root = compute_merkle_root(hashes.copy())
    
    print(f"  Chain Length: {len(sanitized)}")
    print(f"  Chain Tip: {chain_tip_hash[:32]}...")
    print(f"  Merkle Root: {merkle_root[:32]}...")
    print()
    
    # Write sanitized proofs
    print(f"  Writing sanitized proofs to {output_path}...")
    with open(output_path, "w") as f:
        for proof in sanitized:
            f.write(json.dumps(proof) + "\n")
    print(f"  ✓ Wrote {len(sanitized)} proofs")
    print()
    
    # Compute file hash
    print("  Computing file hash...")
    with open(output_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    print(f"  PROOFS.jsonl SHA-256: {file_hash}")
    print()
    
    # Update IPFS_CHAIN_RECORD.json
    print("  Updating IPFS_CHAIN_RECORD.json...")
    try:
        with open("IPFS_CHAIN_RECORD.json") as f:
            record = json.load(f)
    except FileNotFoundError:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": 2,
            "chain_genesis": genesis,
        }
    
    record["timestamp"] = datetime.now(timezone.utc).isoformat()
    record["chain_length"] = len(sanitized)
    record["chain_tip_hash"] = chain_tip_hash
    record["merkle_root"] = merkle_root
    record["proofs_sha256"] = file_hash
    
    with open("IPFS_CHAIN_RECORD.json", "w") as f:
        json.dump(record, f, indent=2)
    
    print("  ✓ Updated IPFS_CHAIN_RECORD.json")
    print()
    
    print("=" * 60)
    print("  ✓ SANITIZATION COMPLETE")
    print(f"    {len(sanitized)} proofs cleaned")
    print(f"    {removed_count} proofs had contamination removed")
    print("=" * 60)
    print()
    
    return True


if __name__ == "__main__":
    sanitize_proofs()
