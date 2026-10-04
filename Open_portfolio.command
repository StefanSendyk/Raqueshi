#!/bin/bash
# Double-click this file to open the Media Studies portfolio with music working.
# YouTube only plays on pages with a web address, so this starts a small web server
# for this folder (http://localhost:8000) and opens the page through it.
# Close this Terminal window when you're done to stop the server.
cd "$(dirname "$0")"
PAGE="Media_Studies_portfolio7.html"
if ! lsof -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
  python3 -m http.server 8000 >/dev/null 2>&1 &
  sleep 1
fi
open "http://localhost:8000/$PAGE"
echo "Portfolio is open at http://localhost:8000/$PAGE"
echo "Close this window to stop the server."
wait
