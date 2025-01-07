#!/bin/bash

# Traverse all directories and subdirectories
find . -type f | while read -r file; do
  # Add the file to staging
  git add "$file"
  
  # Extract the filename (without path)
  filename=$(basename "$file")
  
  # Create a commit message
  commit_message="init add $filename after reset"
  
  # Commit the file
  git commit -m "$commit_message"
done

echo "All files have been processed!"
