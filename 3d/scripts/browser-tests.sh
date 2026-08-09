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
# The timeout is a guard against a hang, not a performance budget, so it is generous: the suite
# takes about 25 s on a workstation, and a CI runner rendering through SwiftShader on shared vCPUs
# is entitled to take several minutes over that. It is deliberately NOT tuned any tighter, because
# a limit that a slow machine trips reports a hang that is not there.
#
# Raising it does not fix a hang, though. A runner failing at 300 s went on to fail at 1200 s, and
# a limit that scales with itself is measuring a page that never finishes rather than one that is
# slow. Hence the log below: the useful thing on a timeout is WHERE it stopped, not more seconds.
: "${A3D_TEST_TIMEOUT:=1200}"

# Chromium's stderr, kept rather than discarded, and left in the profile directory so it can be
# read after the fact. --dump-dom prints the page only if the browser lives long enough to finish,
# so a killed run used to produce a bare exit 124 and nothing else at all. The page logs
# "RUN <name>" on entering each check and --enable-logging=stderr forwards the console here, so
# the last RUN line in this file is the check that hung.
LOG="$PROFILE/last-run.log"
STATUS=0
DOM=$(timeout "$A3D_TEST_TIMEOUT" "$CHROME" --headless=new --no-sandbox --disable-dev-shm-usage \
  --disable-gpu --disk-cache-size=1 --media-cache-size=1 \
  --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --enable-logging=stderr --log-level=0 \
  --user-data-dir="$PROFILE" --virtual-time-budget=120000 --dump-dom \
  "http://127.0.0.1:$PORT/3d/tests/browser.html" 2>"$LOG") || STATUS=$?

if [ "$STATUS" -ne 0 ]; then
  if [ "$STATUS" -eq 124 ]; then
    echo "browser tests: KILLED after ${A3D_TEST_TIMEOUT}s — the page never finished" >&2
  else
    echo "browser tests: chromium exited $STATUS" >&2
  fi
  echo "the last checks it entered, and chromium's own output ($LOG):" >&2
  grep -aE 'RUN |ERROR|Fail' "$LOG" | tail -25 >&2 || true
  exit 1
fi

RESULT=$(printf '%s' "$DOM" | grep -oE 'data-a3d-result="[^"]*"' | head -1 | sed 's/.*="//;s/"$//')
FAILS=$(printf '%s' "$DOM" | grep -oE 'data-a3d-failures="[^"]*"' | head -1 | sed 's/.*="//;s/"$//')

if [ -z "$RESULT" ]; then
  echo "browser tests: NO RESULT (the page did not finish)" >&2
  exit 1
fi
echo "browser tests: $RESULT"
[ -n "$FAILS" ] && echo "failures: $FAILS"

# A SKIP IS NOT A PASS. Every GL check in the suite begins `if (!gl) return null`, so a browser
# that cannot give the page a WebGL2 context skips all of them and still reports fail=0 — a green
# run that tested nothing but the stylesheet. That is the worst result this script can produce,
# because it is indistinguishable from success in a checks list. Skips therefore fail, and a
# machine that genuinely has no GL has to say so out loud.
case "$RESULT" in
  *"skip=0"*) ;;
  *) if [ -n "${A3D_ALLOW_SKIP:-}" ]; then
       echo "warning: checks were skipped and A3D_ALLOW_SKIP is set — GL was NOT exercised" >&2
     else
       echo "browser tests: checks were SKIPPED ($RESULT) — this browser gave the page no" >&2
       echo "WebGL2 context, so the GL suite did not run. Set A3D_ALLOW_SKIP=1 to accept that." >&2
       exit 1
     fi ;;
esac

case "$RESULT" in *"fail=0"*) exit 0 ;; *) exit 1 ;; esac
