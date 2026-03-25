#!/usr/bin/env bash
# refresh-dates.sh
# Updates dateModified in JSON-LD schema on the top 10 most important pages,
# then commits and pushes to trigger a Vercel redeploy (freshness signal for SEO).
#
# Usage:
#   ./scripts/refresh-dates.sh
#   ./scripts/refresh-dates.sh 2026-04-08   # optional: override today's date

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Accept optional date override; default to today (ISO 8601)
TODAY="${1:-$(date +%Y-%m-%d)}"

echo "Refreshing content dates to: $TODAY"

# Top 10 pages to refresh (relative to repo root)
PAGES=(
  "blog/ai-debt-collection.html"
  "blog/best-debt-collection-software.html"
  "blog/how-much-do-collection-agencies-charge.html"
  "blog/ai-vs-traditional-debt-collection.html"
  "blog/b2b-debt-collection.html"
  "blog/when-to-hire-collection-agency.html"
  "blog/collection-agency-alternative.html"
  "compare/highradius-alternatives.html"
  "index.html"
)

UPDATED=0

for PAGE in "${PAGES[@]}"; do
  FILE="$REPO_ROOT/$PAGE"

  if [[ ! -f "$FILE" ]]; then
    echo "  SKIP (not found): $PAGE"
    continue
  fi

  # Update dateModified in JSON-LD schema blocks
  # Handles both quoted formats:
  #   "dateModified": "2026-01-15"
  #   "dateModified":"2026-01-15"
  if grep -q '"dateModified"' "$FILE"; then
    sed -i '' 's|"dateModified"[[:space:]]*:[[:space:]]*"[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}"|"dateModified": "'"$TODAY"'"|g' "$FILE"
    echo "  Updated dateModified: $PAGE"
    UPDATED=$((UPDATED + 1))
  else
    echo "  No dateModified found: $PAGE"
  fi

  # Update any visible "Last updated:" text (common pattern in blog posts)
  # Handles: Last updated: January 15, 2026  OR  Last updated: 2026-01-15
  if grep -qi 'last updated' "$FILE"; then
    # ISO date format
    sed -i '' 's|Last updated: [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}|Last updated: '"$TODAY"'|g' "$FILE"
    echo "  Updated 'Last updated' text: $PAGE"
  fi
done

echo ""
echo "Pages updated: $UPDATED / ${#PAGES[@]}"

if [[ $UPDATED -eq 0 ]]; then
  echo "Nothing to commit."
  exit 0
fi

# Commit and push to trigger Vercel redeploy
cd "$REPO_ROOT"

git add "${PAGES[@]/#/$REPO_ROOT/}" 2>/dev/null || true
# Use relative paths for git add
for PAGE in "${PAGES[@]}"; do
  if [[ -f "$REPO_ROOT/$PAGE" ]]; then
    git -C "$REPO_ROOT" add "$PAGE"
  fi
done

git -C "$REPO_ROOT" commit -m "chore: refresh content dates for SEO freshness signal [${TODAY}]"
git -C "$REPO_ROOT" push origin main

echo ""
echo "Pushed. Vercel redeploy triggered."
echo "IndexNow re-submission recommended after deploy:"
echo "  curl -X POST https://api.indexnow.org/indexnow \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d @${REPO_ROOT}/indexnow.json"
