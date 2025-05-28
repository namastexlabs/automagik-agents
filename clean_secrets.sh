#!/bin/bash

echo "🧹 Cleaning secrets from git history..."

# Files that contain secrets and need to be removed from history
FILES_TO_REMOVE=(
    ".env.prod"
    "docker-compose.yml"
)

# Create a temporary script for git filter-branch
cat > /tmp/filter_script.sh << 'EOF'
#!/bin/bash
FILES_TO_REMOVE=(".env.prod" "docker-compose.yml")
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
    fi
done
EOF

chmod +x /tmp/filter_script.sh

echo "Removing secret-containing files from git history..."

# Use git filter-branch to remove the files from entire history
git filter-branch --tree-filter '/tmp/filter_script.sh' --prune-empty -- --all

if [ $? -eq 0 ]; then
    echo "✅ Git history cleaned successfully"
    
    # Remove backup refs
    git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
    
    # Expire reflog
    git reflog expire --expire=now --all
    
    # Garbage collect
    git gc --prune=now --aggressive
    
    echo "✅ Cleanup completed"
else
    echo "❌ Git filter-branch failed"
    exit 1
fi

# Clean up
rm -f /tmp/filter_script.sh

echo "Git history is now clean of secrets. Ready to push!" 