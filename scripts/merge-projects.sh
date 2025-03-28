#!/bin/bash
# Usage: ./scripts/merge-projects.sh <PROJECT_NAME>

PROJECT_NAME=$1
TEMP_BRANCH="temp-merge-$PROJECT_NAME"

# Define project-specific patterns to exclude
if [[ "$PROJECT_NAME" == "stan" ]]; then
  EXCLUDE_PATHS=(
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

# Make sure we have the latest changes
git checkout $PROJECT_NAME
git pull origin $PROJECT_NAME

# Create temporary branch from project branch
git checkout -b $TEMP_BRANCH

# Remove project-specific folders (only from git, not physically)
for path in "${EXCLUDE_PATHS[@]}"; do
  git rm -r --cached "$path" 2>/dev/null || true
done

# Commit the removals
git commit -m "Prepare for main merge: Remove project-specific code"

# Switch to main and merge the cleaned branch
git checkout main
git pull origin main
git merge --no-ff $TEMP_BRANCH -m "Merge non-project code from $PROJECT_NAME"

# Delete the temporary branch
git branch -D $TEMP_BRANCH

echo "Merge completed. Ready to push to origin/main."
echo "Run 'git push origin main' to publish changes."
