#!/usr/bin/env bash
# Run the browser integration suite headless and report.
#
#   scripts/browser-tests.sh [port]
#
# Serves the repository root on a local port, drives Chromium with software WebGL, and greps the
# machine-readable result attribute out of the dumped DOM. Software WebGL rather than the real
# GPU because the suite asserts geometry and DOM behaviour, not pixels: it must give the same
# answer on a headless CI runner with no display as it does on a workstation.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."          # -> repository root
PORT="${1:-8791}"
CHROME="${CHROME:-chromium}"

if ! curl -sf -o /dev/null "http://127.0.0.1:$PORT/3d/index.js"; then
  python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
  SERVER=$!
  trap 'kill $SERVER 2>/dev/null || true' EXIT
  sleep 1
fi

# A dedicated profile, because Chromium refuses to share one with a running interactive instance.
# A sandboxed install can only write inside its own confinement, and a snap in particular cannot
# see hidden directories in $HOME at all — a profile under ~/.cache silently produces an empty
# DOM rather than an error. Prefer the confinement directory when one is present.
if [ -z "${A3D_CHROME_PROFILE:-}" ]; then
  if [ -d "$HOME/snap/chromium/common" ]; then
    A3D_CHROME_PROFILE="$HOME/snap/chromium/common/a3d-profile"
  else
    A3D_CHROME_PROFILE="${XDG_CACHE_HOME:-$HOME/.cache}/airship3d/chrome-profile"
  fi
fi
PROFILE="$A3D_CHROME_PROFILE"
mkdir -p "$PROFILE"

# --disk-cache-size=1 because the module graph is served from a plain static server: without it a
# second run can silently test the previous run's code.
# The timeout is a guard against a hang, not a performance budget, so it has to be generous
# enough for the slowest machine that legitimately runs this. A CI runner renders through
# SwiftShader on shared vCPUs and takes minutes over what a desktop does in seconds: 300 s
# was tight enough that the suite was killed mid-run and reported as a failure (exit 124).
: "${A3D_TEST_TIMEOUT:=1200}"
DOM=$(timeout "$A3D_TEST_TIMEOUT" "$CHROME" --headless=new --no-sandbox --disable-dev-shm-usage \
  --disk-cache-size=1 --media-cache-size=1 \
  --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --user-data-dir="$PROFILE" --virtual-time-budget=120000 --dump-dom \
  "http://127.0.0.1:$PORT/3d/tests/browser.html" 2>/dev/null)

RESULT=$(printf '%s' "$DOM" | grep -oE 'data-a3d-result="[^"]*"' | head -1 | sed 's/.*="//;s/"$//')
FAILS=$(printf '%s' "$DOM" | grep -oE 'data-a3d-failures="[^"]*"' | head -1 | sed 's/.*="//;s/"$//')

if [ -z "$RESULT" ]; then
  echo "browser tests: NO RESULT (the page did not finish)" >&2
  exit 1
fi
echo "browser tests: $RESULT"
[ -n "$FAILS" ] && echo "failures: $FAILS"
case "$RESULT" in *"fail=0"*) exit 0 ;; *) exit 1 ;; esac
