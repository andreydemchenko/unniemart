#!/bin/bash
# Puts the website on the server (dev@159.195.15.10, folder ~/unniemart) and restarts it. Safe to run again.
# First time only, on the server: Caddy block (site/deploy/Caddyfile.snippet), logins (site/server/auth.py add ...),
# her sheet link (~/.config/unniemart/source.txt) and the robot key (~/.config/unniemart/google-key.json).
set -euo pipefail
cd "$(dirname "$0")/.."
SERVER=${UM_SERVER:-dev@159.195.15.10}
R=/home/dev/unniemart
SSH="ssh -o BatchMode=yes"

echo "building the page"
(cd site/web && npm run build --silent >/dev/null)
$SSH "$SERVER" "mkdir -p $R/app/site/server $R/app/site/web/dist $R/app/automations $R/mirror $R/state \
  ~/.config/unniemart ~/.config/systemd/user && chmod 700 ~/.config/unniemart $R/state"
echo "copying"
rsync -a --delete --exclude __pycache__ -e "$SSH" site/server/ "$SERVER:$R/app/site/server/"
rsync -a --delete -e "$SSH" site/web/dist/ "$SERVER:$R/app/site/web/dist/"
rsync -a -e "$SSH" automations/common.py automations/masterlist.py automations/order_desk.py \
  automations/google_sheet.py "$SERVER:$R/app/automations/"
rsync -a -e "$SSH" site/deploy/unniemart.service "$SERVER:.config/systemd/user/unniemart.service"
echo "python packages"
$SSH "$SERVER" "cd $R && { [ -x .venv/bin/python ] || python3 -m venv --without-pip .venv; } && \
  python3 -m pip --python .venv/bin/python install -q --disable-pip-version-check -r app/site/server/requirements.txt"
echo "restarting"
$SSH "$SERVER" "systemctl --user daemon-reload && systemctl --user enable -q unniemart && systemctl --user restart unniemart"
sleep 3
$SSH "$SERVER" "systemctl --user is-active unniemart && curl -s -o /dev/null -w 'local check: %{http_code}\n' http://127.0.0.1:8821/api/me"
echo "content"
python3 automations/site_sync.py
