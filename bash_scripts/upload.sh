#!/bin/bash

# Directory containing the image files
ASSETS_DIR="assets/unverified"

# Supported image mime types
IMAGE_TYPES=("image/jpeg" "image/png" "image/gif")

# Function to check if a file is an image
is_image() {
  local file="$1"
  local mime_type=$(file --mime-type -b "$file")
  for type in "${IMAGE_TYPES[@]}"; do
    if [[ "$mime_type" == "$type" ]]; then
      echo "$mime_type"
      return 0
    fi
  done
  return 1
}

# Loop over all files in the assets directory
for file in "$ASSETS_DIR"/*; do
  if [[ -f "$file" ]]; then
    mime_type=$(is_image "$file")
    if [[ $? -eq 0 ]]; then
      # Run the curl command for each image file
      curl -X 'POST' \
        'http://localhost:8000/api/receipts' \
        -H 'accept: application/json' \
        -H 'Content-Type: multipart/form-data' \
        -F "files=@$file;type=$mime_type"

      echo "Uploaded $file"
    fi
  fi
done