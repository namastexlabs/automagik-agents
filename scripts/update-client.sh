#!/bin/bash
# Usage: ./scripts/update-project.sh <PROJECT_NAME>

PROJECT_NAME=$1

# Define project-specific patterns that should be preserved
if [[ "$PROJECT_NAME" == "stan" ]]; then
  PRESERVE_PATHS=(
    "src/agents/simple/stan_agent"
    "src/agents/simple/stan_email_agent"
    "src/tools/blackpearl"
    "src/tools/omie"
    "tests/tools/blackpearl"
    "tests/tools/omie"
  )
else
  echo "Error: Unknown project name. Add paths for this project in the script."
  exit 1
fi

# Make sure we have the latest of both branches
git checkout main
git pull origin main
git checkout $PROJECT_NAME
git pull origin $PROJECT_NAME

# First, backup the project-specific files
TEMP_DIR=$(mktemp -d)
for path in "${PRESERVE_PATHS[@]}"; do
  if [ -d "$path" ]; then
    mkdir -p "$TEMP_DIR/$(dirname "$path")"
    cp -r "$path" "$TEMP_DIR/$(dirname "$path")/"
  fi
done

# Merge main into project branch
git merge main -m "Merge updates from main"

# Restore project-specific files that might have been deleted or modified
for path in "${PRESERVE_PATHS[@]}"; do
  if [ -d "$TEMP_DIR/$path" ]; then
    rm -rf "$path" 2>/dev/null || true
    cp -r "$TEMP_DIR/$path" "$(dirname "$path")/"
    git add "$path"
  fi
done

if git diff --cached --quiet; then
  echo "No project files needed to be restored."
else
  git commit -m "Restore project-specific files after main merge"
fi

# Clean up
rm -rf "$TEMP_DIR"

echo "project branch updated successfully with main changes, preserving project-specific code."
echo "Run 'git push origin $PROJECT_NAME' to publish changes."
