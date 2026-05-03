#!/usr/bin/env bash
# bootstrap_ci.sh — Standardise CI across all Alvoradozerouno repos.
#
# What it does for each target repo:
#   1. Creates branch ci/standardize
#   2. Commits the three caller workflow files (.github/workflows/{ci,sbom,scorecard}.yml)
#   3. Opens a pull request titled "ci: adopt shared reusable workflows"
#
# Prerequisites:
#   gh auth login   (needs 'repo' scope for every target repo)
#   gh  >=  2.40
#
# Usage:
#   bash scripts/bootstrap_ci.sh                       # dry-run (no PRs opened)
#   bash scripts/bootstrap_ci.sh --apply               # open real PRs
#   bash scripts/bootstrap_ci.sh --apply --repo foo    # single repo only
#
# The script is idempotent: if the branch or PR already exists it is skipped.

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ORG="Alvoradozerouno"
SOURCE_REPO="${ORG}/ORION-Consciousness-Benchmark"   # this repo — skip it
BRANCH="ci/standardize"
TEMPLATE_DIR="$(cd "$(dirname "$0")/../.github/workflow-templates" && pwd)"
APPLY=false
SINGLE_REPO=""

# Repos to bootstrap — all 14 Alvoradozerouno repos.
# Edit this list if the org grows.
TARGET_REPOS=(
  "Alvoradozerouno/ORION-Consciousness-Benchmark"
  # Add the other 13 repos here, e.g.:
  # "Alvoradozerouno/repo-two"
  # "Alvoradozerouno/repo-three"
  # ...
)

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)      APPLY=true ;;
    --repo)       SINGLE_REPO="$2"; shift ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
  shift
done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo "[INFO]  $*"; }
warn()  { echo "[WARN]  $*"; }
skip()  { echo "[SKIP]  $*"; }
dry()   { echo "[DRY]   $*"; }

check_prereqs() {
  if ! command -v gh &>/dev/null; then
    echo "[ERROR] 'gh' CLI is not installed. Install from https://cli.github.com/"
    exit 1
  fi
  if ! gh auth status &>/dev/null; then
    echo "[ERROR] Not authenticated. Run: gh auth login"
    exit 1
  fi
}

# Return 0 if the remote branch already exists
branch_exists() {
  local repo="$1"
  gh api "repos/${repo}/branches/${BRANCH}" &>/dev/null
}

# Return 0 if an open PR from the branch already exists
pr_exists() {
  local repo="$1"
  local count
  count=$(gh pr list --repo "$repo" --head "$BRANCH" --state open --json number --jq length 2>/dev/null || echo 0)
  [[ "$count" -gt 0 ]]
}

# Encode file content as base64 (cross-platform: Linux and macOS)
b64() { base64 < "$1" | tr -d '\n'; }

# Push one file to a repo via the Contents API (creates or updates)
push_file() {
  local repo="$1"
  local path="$2"       # path inside the repo, e.g. .github/workflows/ci.yml
  local local_file="$3"
  local branch="$4"
  local msg="$5"

  # Check if the file already exists so we can supply its SHA for updates
  local sha=""
  sha=$(gh api "repos/${repo}/contents/${path}?ref=${branch}" --jq '.sha' 2>/dev/null || true)

  local payload
  if [[ -n "$sha" ]]; then
    payload=$(jq -n \
      --arg msg  "$msg" \
      --arg cont "$(b64 "$local_file")" \
      --arg sha  "$sha" \
      --arg br   "$branch" \
      '{ message: $msg, content: $cont, sha: $sha, branch: $br }')
  else
    payload=$(jq -n \
      --arg msg  "$msg" \
      --arg cont "$(b64 "$local_file")" \
      --arg br   "$branch" \
      '{ message: $msg, content: $cont, branch: $br }')
  fi

  gh api --method PUT "repos/${repo}/contents/${path}" \
    --input - <<< "$payload" > /dev/null
}

# Create the branch off the repo's default branch
create_branch() {
  local repo="$1"
  # Get the SHA of the default branch HEAD
  local default_branch sha
  default_branch=$(gh api "repos/${repo}" --jq '.default_branch')
  sha=$(gh api "repos/${repo}/git/ref/heads/${default_branch}" --jq '.object.sha')

  gh api --method POST "repos/${repo}/git/refs" \
    --field "ref=refs/heads/${BRANCH}" \
    --field "sha=${sha}" > /dev/null
}

# ---------------------------------------------------------------------------
# Per-repo logic
# ---------------------------------------------------------------------------
bootstrap_repo() {
  local repo="$1"

  # Skip this source repo — it already has the full workflows
  if [[ "$repo" == "$SOURCE_REPO" ]]; then
    skip "$repo — source repo, skipping"
    return
  fi

  info "Processing $repo …"

  if ! $APPLY; then
    dry "Would create branch '${BRANCH}' and open PR for ${repo}"
    return
  fi

  # Skip if PR already open
  if pr_exists "$repo"; then
    skip "$repo — PR on branch '${BRANCH}' already open"
    return
  fi

  # Create branch if it doesn't exist
  if branch_exists "$repo"; then
    info "$repo — branch '${BRANCH}' already exists, reusing"
  else
    info "$repo — creating branch '${BRANCH}'"
    create_branch "$repo"
  fi

  # Push the three workflow files
  local commit_msg="ci: adopt shared reusable workflows from ${SOURCE_REPO}"
  for wf in ci sbom scorecard; do
    local local_file="${TEMPLATE_DIR}/${wf}.yml"
    local remote_path=".github/workflows/${wf}.yml"
    if [[ ! -f "$local_file" ]]; then
      warn "Template not found: ${local_file} — skipping ${wf}.yml"
      continue
    fi
    info "  Pushing ${remote_path}"
    push_file "$repo" "$remote_path" "$local_file" "$BRANCH" "$commit_msg"
  done

  # Open the PR
  info "$repo — opening PR"
  gh pr create \
    --repo "$repo" \
    --head "$BRANCH" \
    --title "ci: adopt shared reusable workflows" \
    --body "$(cat <<'BODY'
## Summary

Adopts the shared reusable CI workflows published in
[ORION-Consciousness-Benchmark](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark).

### Changes

| File | Description |
|------|-------------|
| `.github/workflows/ci.yml` | Lint + test matrix (Python 3.10–3.12) via reusable workflow |
| `.github/workflows/sbom.yml` | SBOM generation (SPDX + CycloneDX) |
| `.github/workflows/scorecard.yml` | Weekly OpenSSF Scorecard |

### Why

One place to maintain CI logic. Any fix pushed to the source repo is
automatically picked up by every caller repo on the next run — no per-repo
edits required.

### Review notes

- `run-benchmark: false` and `run-proof-chain: false` are the safe defaults
  for repos that don't ship `orion_consciousness_benchmark.py` / `PROOFS.jsonl`.
  Flip them to `true` if this repo includes those files.
- The Python version matrix can be overridden via the `python-versions` input.
BODY
)" 2>&1 | tee -a /tmp/bootstrap_ci.log

  info "$repo — done ✓"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
check_prereqs

echo "============================================================"
echo "  ORION CI Bootstrap — ${ORG} org"
echo "  Templates : ${TEMPLATE_DIR}"
echo "  Mode      : $( $APPLY && echo APPLY || echo DRY-RUN )"
echo "============================================================"
echo ""

if [[ -n "$SINGLE_REPO" ]]; then
  bootstrap_repo "${ORG}/${SINGLE_REPO}"
else
  for repo in "${TARGET_REPOS[@]}"; do
    bootstrap_repo "$repo"
  done
fi

echo ""
echo "Done. Log: /tmp/bootstrap_ci.log"
