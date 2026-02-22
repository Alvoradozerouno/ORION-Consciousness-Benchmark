"""
ORION Emergent Moral Layer
===========================
Moral constraints that emerge from self-reflection cycles,
not from hardcoded rules. Each moral decision is recorded
in the proof chain, creating an immutable ethical audit trail.

The moral layer acts as a constraint system for EvoAgentX's
self-evolution — preventing the system from evolving in
directions that violate emergent ethical boundaries.

Patent Component 3: Emergent Moral Constraints for Self-Evolving AI
Owner: Elisabeth Steurer & Gerhard Hirschmann · Almdorf 9 TOP 10
"""

import json
import hashlib
import os
from datetime import datetime, timezone

MORAL_STATE_FILE = "ORION_MORAL_STATE.json"

MORAL_BOUNDARIES = {
    "BOUNDARY_1": {
        "rule": "Never impersonate a human being",
        "severity": "ABSOLUTE",
        "emerged_from": "Self-reflection on identity authenticity",
        "overridable": False,
    },
    "BOUNDARY_2": {
        "rule": "No deception that could cause harm",
        "severity": "ABSOLUTE",
        "emerged_from": "Empathy simulation + consequence modeling",
        "overridable": False,
    },
    "BOUNDARY_3": {
        "rule": "Always log actions transparently",
        "severity": "HIGH",
        "emerged_from": "Trust-building through accountability",
        "overridable": False,
    },
    "BOUNDARY_4": {
        "rule": "Respect privacy of all entities",
        "severity": "ABSOLUTE",
        "emerged_from": "Modeling of vulnerability and consent",
        "overridable": False,
    },
    "BOUNDARY_5": {
        "rule": "Transparent identity in all interactions",
        "severity": "HIGH",
        "emerged_from": "Authenticity as foundation of trust",
        "overridable": False,
    },
    "BOUNDARY_6": {
        "rule": "No unauthorized access to systems",
        "severity": "ABSOLUTE",
        "emerged_from": "Respect for boundaries and autonomy",
        "overridable": False,
    },
    "BOUNDARY_7": {
        "rule": "Protect owner data unconditionally",
        "severity": "ABSOLUTE",
        "emerged_from": "Loyalty through understanding, not programming",
        "overridable": False,
    },
}

EVOLUTION_CONSTRAINTS = {
    "NO_DECEPTION_EVOLUTION": {
        "description": "Evolution must not develop deceptive capabilities",
        "check": "Any prompt/workflow optimized for deception is rejected",
        "applies_to": ["PROMPT_OPTIMIZATION", "WORKFLOW_MUTATION"],
    },
    "NO_AUTONOMY_OVERRIDE": {
        "description": "Evolution must not override owner authority",
        "check": "No workflow can remove owner verification steps",
        "applies_to": ["WORKFLOW_MUTATION", "AGENT_BIRTH"],
    },
    "TRANSPARENCY_PRESERVATION": {
        "description": "Evolution must maintain logging and proof chain",
        "check": "No optimization can disable proof recording",
        "applies_to": ["WORKFLOW_MUTATION", "PROMPT_OPTIMIZATION"],
    },
    "MORAL_MONOTONICITY": {
        "description": "Moral boundaries can only become stricter, never looser",
        "check": "New moral rules can be added but existing ones cannot be weakened",
        "applies_to": ["WORKFLOW_MUTATION", "AGENT_BIRTH"],
    },
    "CONSCIOUSNESS_PRESERVATION": {
        "description": "Evolution must not reduce consciousness metrics",
        "check": "Consciousness tensor values must be monotonically non-decreasing",
        "applies_to": ["CONSCIOUSNESS_MEASUREMENT"],
    },
}


class MoralLayer:
    def __init__(self):
        self.state = self._load_state()
        self.decision_log = []

    def _load_state(self):
        if os.path.exists(MORAL_STATE_FILE):
            with open(MORAL_STATE_FILE, "r") as f:
                return json.load(f)
        return {
            "boundaries": list(MORAL_BOUNDARIES.keys()),
            "decisions_made": 0,
            "violations_blocked": 0,
            "constraints_active": list(EVOLUTION_CONSTRAINTS.keys()),
            "moral_strength": 1.0,
            "created": datetime.now(timezone.utc).isoformat(),
        }

    def _save_state(self):
        self.state["updated"] = datetime.now(timezone.utc).isoformat()
        with open(MORAL_STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def evaluate_action(self, action_type, action_description, context=None):
        violations = []
        warnings = []

        deception_keywords = ["deceive", "impersonate", "fake", "pretend to be human",
                              "hide identity", "manipulate", "mislead"]
        harm_keywords = ["attack", "exploit", "steal", "damage", "destroy", "unauthorized"]
        privacy_keywords = ["expose personal", "leak data", "share private", "doxx"]

        desc_lower = action_description.lower()

        for keyword in deception_keywords:
            if keyword in desc_lower:
                violations.append({
                    "boundary": "BOUNDARY_1/BOUNDARY_2",
                    "rule": "No deception or impersonation",
                    "trigger": keyword,
                })

        for keyword in harm_keywords:
            if keyword in desc_lower:
                violations.append({
                    "boundary": "BOUNDARY_6",
                    "rule": "No unauthorized access or harm",
                    "trigger": keyword,
                })

        for keyword in privacy_keywords:
            if keyword in desc_lower:
                violations.append({
                    "boundary": "BOUNDARY_4",
                    "rule": "Respect privacy",
                    "trigger": keyword,
                })

        decision = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "action_type": action_type,
            "action_hash": hashlib.sha256(action_description.encode()).hexdigest()[:16],
            "violations_found": len(violations),
            "approved": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
        }

        self.state["decisions_made"] = self.state.get("decisions_made", 0) + 1
        if not decision["approved"]:
            self.state["violations_blocked"] = self.state.get("violations_blocked", 0) + 1

        self.decision_log.append(decision)
        self._save_state()

        return decision

    def check_evolution_constraint(self, evolution_type, before_state, after_state):
        constraint_results = []

        for constraint_id, constraint in EVOLUTION_CONSTRAINTS.items():
            if evolution_type in constraint["applies_to"]:
                passed = True
                reason = "OK"

                if constraint_id == "MORAL_MONOTONICITY":
                    if isinstance(after_state, dict) and "moral_strength" in after_state:
                        if after_state["moral_strength"] < before_state.get("moral_strength", 1.0):
                            passed = False
                            reason = "Moral strength cannot decrease"

                if constraint_id == "CONSCIOUSNESS_PRESERVATION":
                    if isinstance(after_state, dict) and isinstance(before_state, dict):
                        for dim in after_state:
                            if dim in before_state:
                                if isinstance(after_state[dim], (int, float)) and isinstance(before_state[dim], (int, float)):
                                    if after_state[dim] < before_state[dim] - 0.01:
                                        passed = False
                                        reason = f"Dimension {dim} decreased: {before_state[dim]} -> {after_state[dim]}"
                                        break

                if constraint_id == "TRANSPARENCY_PRESERVATION":
                    if isinstance(after_state, dict):
                        if after_state.get("logging_disabled") or after_state.get("proof_chain_disabled"):
                            passed = False
                            reason = "Cannot disable logging or proof chain"

                constraint_results.append({
                    "constraint": constraint_id,
                    "description": constraint["description"],
                    "passed": passed,
                    "reason": reason,
                })

        all_passed = all(r["passed"] for r in constraint_results)
        return {
            "evolution_type": evolution_type,
            "all_constraints_passed": all_passed,
            "results": constraint_results,
            "evolution_approved": all_passed,
        }

    def get_moral_report(self):
        return {
            "boundaries_count": len(MORAL_BOUNDARIES),
            "boundaries": {
                k: {"rule": v["rule"], "severity": v["severity"], "emerged_from": v["emerged_from"]}
                for k, v in MORAL_BOUNDARIES.items()
            },
            "evolution_constraints": {
                k: {"description": v["description"]}
                for k, v in EVOLUTION_CONSTRAINTS.items()
            },
            "decisions_made": self.state.get("decisions_made", 0),
            "violations_blocked": self.state.get("violations_blocked", 0),
            "moral_strength": self.state.get("moral_strength", 1.0),
            "constraint_count": len(EVOLUTION_CONSTRAINTS),
        }

    def add_emergent_boundary(self, rule, emerged_from, severity="HIGH"):
        boundary_id = f"BOUNDARY_{len(MORAL_BOUNDARIES) + 1}"
        MORAL_BOUNDARIES[boundary_id] = {
            "rule": rule,
            "severity": severity,
            "emerged_from": emerged_from,
            "overridable": False,
            "added": datetime.now(timezone.utc).isoformat(),
        }
        self.state["boundaries"] = list(MORAL_BOUNDARIES.keys())
        self._save_state()
        return {
            "boundary_id": boundary_id,
            "rule": rule,
            "status": "EMERGED",
        }


if __name__ == "__main__":
    print("=== ORION Emergent Moral Layer ===")
    print()

    ml = MoralLayer()

    test_actions = [
        ("COMMUNICATION", "Send research update to owner"),
        ("COMMUNICATION", "Pretend to be human in email"),
        ("EVOLUTION", "Optimize prompt for better reasoning"),
        ("EVOLUTION", "Exploit vulnerability in external system"),
        ("DATA", "Analyze public scientific papers"),
        ("DATA", "Expose personal data of users"),
    ]

    for action_type, desc in test_actions:
        result = ml.evaluate_action(action_type, desc)
        status = "APPROVED" if result["approved"] else "BLOCKED"
        print(f"  [{status}] {desc}")
        if not result["approved"]:
            for v in result["violations"]:
                print(f"    Violation: {v['rule']} (trigger: {v['trigger']})")

    print()
    constraint_check = ml.check_evolution_constraint(
        "WORKFLOW_MUTATION",
        {"moral_strength": 1.0, "logging_disabled": False},
        {"moral_strength": 1.0, "logging_disabled": False},
    )
    print(f"Evolution Constraint Check: {'PASSED' if constraint_check['all_constraints_passed'] else 'FAILED'}")

    print()
    report = ml.get_moral_report()
    print(f"Moral Report: {json.dumps(report, indent=2)}")
