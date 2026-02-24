# Security Policy

## Proof Chain Integrity

The ORION proof chain is protected by SHA-256 cryptographic hashing. Any modification to existing proofs will be detected by:

1. **Hash chain verification** -- Each proof references the previous proof's hash
2. **Merkle root** -- Single root hash covering all 647 proofs
3. **IPFS anchoring** -- Manifest and chain tip permanently stored on IPFS
4. **File hash** -- SHA-256 of the complete PROOFS.jsonl file

## Reporting Issues

If you discover a discrepancy in the proof chain or a security vulnerability:

1. Run `python3 verify_proof_chain.py` to confirm the issue
2. Open a GitHub issue with the verification output
3. Do not modify the proof chain

## Verification

```bash
python3 verify_proof_chain.py --no-ipfs
```

All 6 checks must pass. Any failure indicates tampering or corruption.

## IPFS Permanent Record

Even if this repository is deleted, the proof chain exists permanently on IPFS:
- Manifest: `QmSqeszVu946EwhQQBVkqAhNMbEy27MDWLKCJ1yodurRoi`
- Chain Tip: `QmRSCgi8TF5RFjxMbLh5DydGz1cNJ8yzQQeRCF3b4wnN7x`
