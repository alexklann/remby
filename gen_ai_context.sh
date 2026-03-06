#!/bin/bash
rm -rf codebase.txt
(
    echo "--- PROJECT STRUCTURE ---";
    tree --gitignore;
    echo -e "\n--- FILE CONTENTS ---";
    git ls-files "*.py" "*.json" "*.md" | while read -r file; do
        echo "--- FILE: $file ---"
        cat "$file"
        echo -e "\n"
    done
) > codebase.txt

echo "file://$(realpath codebase.txt)" | wl-copy -t text/uri-list
