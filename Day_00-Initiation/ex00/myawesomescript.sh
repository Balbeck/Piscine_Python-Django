#!/bin/bash
# This script takes a URL as an argument and prints the value of the "Location" header
# from the HTTP response headers.

# curl -I only HTTP headers
#grep -i "^location:" extrait Location (redirection)
#cut -d' ' -f2 récupère l’URL cible
#"$1" → 1er argument du script (bit.ly/...)

curl -I "$1" 2>/dev/null | grep -i "^location:" | cut -d' ' -f2
