#!/bin/bash
# inference.sh – Launcher script for LatentSync inference with superresolution

# Default superres method is "none" (i.e. do not use superresolution)
SUPERRES_METHOD="none"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --superres)
            SUPERRES_METHOD="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
done

# Export the chosen superres method so Python can read it
export SUPERRES_METHOD

# Now launch the Python inference code (pass along any remaining arguments)
python predict.py "$@"
