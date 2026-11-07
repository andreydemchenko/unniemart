#!/bin/bash
# Runner for the scheduled jobs (launchd, see automations/launchd/). Logs go to data/logs/.
#   automations/run.sh daily    news_watch → media → site_sync (the website gets the news and new video covers)
#   automations/run.sh desk     site_sync only, every hour: files to the website;
#                               quiet unless the website hasn't been updated for 6+ hours
#   automations/run.sh weekly   weekly_stats → peer_watch → her sheet → weekly_brief → media → site_sync (about 15 minutes,
#                               ~$0.55 of Apify)
# The website itself runs on the server all the time (site/, https://unniemart.159-195-15-10.sslip.io).
# A Mac notification says when something is urgent, when the brief is ready, or when a step failed.
set -u
cd "$(dirname "$0")/.." || exit 1
export PATH="$HOME/.pyenv/versions/3.10.12/bin:$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"
mkdir -p data/logs
LOG="data/logs/$(date +%Y-%m-%d)-$1.log"

notify() { osascript -e "display notification \"$2\" with title \"Unnie Mart: $1\"" >/dev/null 2>&1; }

step() {   # step NAME COMMAND...: run, log, and remember the last output line
    local name=$1; shift
    echo "== $(date '+%F %T') $name" >>"$LOG"
    if "$@" >>"$LOG.out" 2>>"$LOG"; then
        LAST=$(tail -1 "$LOG.out"); cat "$LOG.out" >>"$LOG"; rm -f "$LOG.out"; return 0
    fi
    cat "$LOG.out" >>"$LOG" 2>/dev/null; rm -f "$LOG.out"
    notify "$name failed" "See $LOG"; FAILED=1; return 1
}

sync() {   # one website update at a time (the hourly and the daily run can meet)
    local lock=data/state/site_sync.lock
    mkdir -p data/state
    if ! mkdir "$lock" 2>/dev/null; then
        [ -n "$(find "$lock" -maxdepth 0 -mmin +30)" ] || return 0   # a run is going; an older lock is left over
    fi
    step site_sync python3 -W ignore automations/site_sync.py
    rmdir "$lock" 2>/dev/null
}

FAILED=0; LAST=""
case "${1:-}" in
  daily)
    step news_watch python3 automations/news_watch.py
    case "$LAST" in *"(0 urgent)"*) ;; *urgent*) notify "news" "$LAST · data/news/latest.md" ;; esac
    step media python3 -W ignore automations/media.py
    sync
    ;;
  desk)
    sync
    ;;
  weekly)
    step weekly_stats python3 automations/weekly_stats.py
    step peer_watch python3 automations/peer_watch.py
    step masterlist python3 -W ignore automations/masterlist.py   # fresh stock tab for the brief
    # The brief still runs if a scrape failed: its source-health line says what's missing.
    step weekly_brief python3 -W ignore automations/weekly_brief.py && notify "weekly brief ready" "$LAST"
    step media python3 -W ignore automations/media.py           # covers for the new videos and the brief's examples
    sync
    ;;
  *) echo "usage: $0 daily|desk|weekly"; exit 2 ;;
esac
exit $FAILED
