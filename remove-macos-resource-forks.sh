#!/usr/bin/env bash
set -euo pipefail

# Run from project root: /Users/johnny/Downloads/dupic
if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree is not clean. Commit or stash changes before running this script."
  git status --porcelain
  exit 1
fi

BRANCH="remove-macos-resource-forks"
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH"
fi

echo "Finding all files named starting with '._'..."
find . -name '._*' -type f -print | sed 's|^\./||' > all_dotunderscore_files.txt || true
echo "Total ._* files found: $(wc -l < all_dotunderscore_files.txt || true)"
echo

echo "Finding tracked ._* files in git..."
git ls-files -z | tr '\0' '\n' | grep -E '(^|/)\._' > tracked_dotunderscore_files.txt || true
echo "Total tracked ._* files: $(wc -l < tracked_dotunderscore_files.txt || true)"
echo

if [ -s tracked_dotunderscore_files.txt ]; then
  echo "Removing tracked ._* files via git rm..."
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    echo "git rm -- \"$f\""
    git rm -- "$f"
  done < tracked_dotunderscore_files.txt
  git commit -m "Remove macOS resource-fork files (._*)"
else
  echo "No tracked ._* files to remove."
fi
echo

if [ -s all_dotunderscore_files.txt ]; then
  echo "Deleting remaining untracked ._* files from disk..."
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [ -f "$f" ]; then
      if ! git ls-files --error-unmatch -- "$f" >/dev/null 2>&1; then
        echo "rm -- \"$f\""
        rm -v -- "$f"
      fi
    fi
  done < all_dotunderscore_files.txt
else
  echo "No ._* files on disk to delete."
fi
echo

echo "Updating .gitignore..."
if [ ! -f .gitignore ]; then
  touch .gitignore
fi
grep -qxF "._*" .gitignore || printf "\n# macOS resource fork files\n._*\n.DS_Store\n" >> .gitignore
git add .gitignore
git commit -m "Add macOS ignores (.DS_Store, ._*)" || true

echo "Pushing branch $BRANCH to origin..."
git push -u origin "$BRANCH"

echo "Done. Review the branch on GitHub and merge into your main branch when ready."