#!/usr/bin/env bash
# Run the browser integration suite headless and report.
#
#   scripts/browser-tests.sh [base-url]
#
# Serves the repository root on a system-chosen port, drives Chromium with software WebGL, and reads the
# result the page prints to the console. Software WebGL rather than the real GPU because the suite
# asserts geometry and DOM behaviour, not pixels: it must give the same answer on a headless CI
# runner with no display as it does on a workstation.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."          # -> repository root
CHROME="${CHROME:-chromium}"

# With no argument, the wrapper owns the listening socket until this script exits.
# A person may explicitly supply a complete loopback base address.
if [ "$#" -eq 0 ]; then
  exec python3 tools/with_server.py -- bash 3d/scripts/browser-tests.sh '{base}'
fi
if [ "$#" -ne 1 ]; then
  echo 'usage: browser-tests.sh [base-url]' >&2
  exit 2
fi
case "$1" in
  http://127.0.0.1:*) BASE="${1%/}/" ;;
  *) echo 'browser tests: expected a full loopback base address' >&2; exit 2 ;;
esac

# A dedicated profile, because Chromium refuses to share one with a running interactive instance.
# A sandboxed install can only write inside its own confinement, and a snap in particular cannot
# see hidden directories in $HOME at all — a profile under ~/.cache silently produces an empty
# DOM rather than an error. Honour explicit scratch first; otherwise prefer confinement.
if [ -z "${A3D_CHROME_PROFILE:-}" ]; then
  if [ -n "${TMPDIR:-}" ]; then
    A3D_CHROME_PROFILE="$TMPDIR/airship3d/chrome-profile"
  elif [ -d "$HOME/snap/chromium/common" ]; then
    A3D_CHROME_PROFILE="$HOME/snap/chromium/common/a3d-profile"
  else
    A3D_CHROME_PROFILE="${XDG_CACHE_HOME:-$HOME/.cache}/airship3d/chrome-profile"
  fi
fi
mkdir -p "$A3D_CHROME_PROFILE"
PROFILE=$(mktemp -d "$A3D_CHROME_PROFILE/run.XXXXXX")
cleanup() {
  if [ -n "${CHROME_PID:-}" ]; then
    kill "$CHROME_PID" 2>/dev/null || true
    wait "$CHROME_PID" 2>/dev/null || true
  fi
  rm -rf -- "$PROFILE"
}
trap cleanup EXIT

# THE RESULT COMES FROM THE PAGE'S OWN CONSOLE, NOT FROM --dump-dom.
#
# --dump-dom prints the DOM when the VIRTUAL-TIME BUDGET is exhausted, not when the page finishes,
# and virtual time PAUSES while any network fetch is outstanding. On a CI runner Chrome's own
# background services keep fetching — GCM registration retried every few minutes in the log — so
# the budget was never exhausted, the dump never came, and a suite that had printed
# "DONE pass=28 fail=0 skip=0" sat there until the timeout killed it. Four CI runs died that way.
#
# So the page prints its own answer and this script reads that, then kills the browser the moment
# it appears. The dump is no longer load-bearing, the run ends as soon as the work is done instead
# of waiting out a budget, and the background-networking flags below stop Chrome making the
# requests that caused it in the first place.
#
# --disk-cache-size=1 because the module graph comes off a plain static server: without it a second
# run can silently test the previous run's code. The timeout below is a HANG GUARD, not a budget —
# the suite is about 25 s on a workstation and several minutes on a runner through SwiftShader, and
# a limit tight enough to trip on a slow machine reports a hang that is not there.
: "${A3D_TEST_TIMEOUT:=1200}"
LOG="$PROFILE/last-run.log"
: > "$LOG"

"$CHROME" --headless=new --no-sandbox --disable-dev-shm-usage \
  --disable-gpu --disk-cache-size=1 --media-cache-size=1 \
  --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --enable-logging=stderr --log-level=0 \
  --disable-background-networking --disable-component-update --disable-sync \
  --disable-default-apps --no-first-run --no-default-browser-check \
  --disable-client-side-phishing-detection --disable-domain-reliability \
  --metrics-recording-only \
  --user-data-dir="$PROFILE" --virtual-time-budget=20000 --dump-dom \
  "${BASE}3d/tests/browser.html" >/dev/null 2>"$LOG" &
CHROME_PID=$!
DEADLINE=$(( $(date +%s) + A3D_TEST_TIMEOUT ))
while :; do
  grep -qa 'DONE pass=' "$LOG" && break
  if ! kill -0 "$CHROME_PID" 2>/dev/null; then break; fi     # exited without ever reporting
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then break; fi
  sleep 0.5
done
kill "$CHROME_PID" 2>/dev/null || true
wait "$CHROME_PID" 2>/dev/null || true
CHROME_PID=""

RESULT=$(grep -oaE 'DONE pass=[0-9]+ fail=[0-9]+ skip=[0-9]+' "$LOG" | tail -1 | sed 's/^DONE //')
FAILS=$(grep -oaE 'FAILURES .*' "$LOG" | tail -1 | sed 's/^FAILURES //;s/", source.*//')

if [ -z "$RESULT" ]; then
  echo "browser tests: NO RESULT after ${A3D_TEST_TIMEOUT}s — the page never finished" >&2
  echo "the last checks it entered, and chromium's own output ($LOG):" >&2
  grep -aE 'RUN |ERROR|Fail' "$LOG" | tail -25 >&2 || true
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
