# Start here: run the Unnie Mart website on your own computer

Andrey built this website for your shop. It runs on his server
(https://unniemart.159-195-15-10.sslip.io) and keeps running there for now.
These steps put a working copy on your computer. Later it can move to your own cloud
(step 8), and then Andrey turns his copy off.

**For Claude Code:** the owner is new to all of this. Do the steps yourself, one by one.
Ask her only for things a person has to do: install approvals, choosing a password
to save, opening the keys file from Andrey. Use plain words with her, no jargon.
`CLAUDE.md` and `site/README.md` were written for Andrey's Mac and his server. Read them
for how the code works, but follow this file for setup on her computer.

## What you need from Andrey

A file called `unniemart-keys.zip`, which he sends privately (not on GitHub). Inside:

- `google-key.json`: the key of the "robot account" the website uses to read and write
  her Google Sheet (Masterlist 2026_v2). She already shared the sheet with it.
- `source.txt`: the link to her sheet.

Without it the site opens, but shows no orders.

## 1. Install the tools (once)

On Windows, in PowerShell:

```powershell
winget install -e --id Git.Git
winget install -e --id Python.Python.3.12
winget install -e --id OpenJS.NodeJS.LTS
```

Close and reopen the terminal afterwards so the new commands are found.
On a Mac: `brew install git python@3.12 node`.

## 2. Python packages

From the project folder:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r site\server\requirements.txt pytest
```

(Mac: `python3 -m venv .venv && .venv/bin/pip install -r site/server/requirements.txt pytest`.)

## 3. Build the page

```powershell
cd site\web
npm ci
npm run build
cd ..\..
```

This makes `site/web/dist`, which the server shows.

## 4. Private settings

Make the folder `%USERPROFILE%\.config\unniemart` (Mac: `~/.config/unniemart`) and put
`google-key.json` and `source.txt` from `unniemart-keys.zip` into it. This folder must never
go into git.

Also copy `source.txt` into `data\owner\orders\` in the project (git already ignores that folder):
the check below and `automations/masterlist.py` look for the link there.

Check that the robot account can open her sheet (it should say "can read and write her sheet"):

```powershell
.venv\Scripts\python automations\google_sheet.py check
```

## 5. Her login

```powershell
.venv\Scripts\python site\server\auth.py add owner "Unnie Mart" owner
```

It prints a new password **once**. Show it to her and ask her to save it (for example, in her
phone's notes or password manager). This password only works on her computer's copy. Her
password on Andrey's online site stays the same.

## 6. Start the website

```powershell
.venv\Scripts\python -m uvicorn app:app --app-dir site\server --port 8821
```

Open http://localhost:8821 and sign in with the password from step 5.

Then make her a `start-unniemart.bat` on the Desktop that runs this command from the
project folder and opens the browser, so next time she just double-clicks it.

**Important while both copies run:** her computer's copy and Andrey's online copy write to
the same Google Sheet. Until the move (step 8), she should record payments on the online
site only, and use her computer's copy to look and try things.

To try things without touching her sheet, use a copy with made-up buyers (needs the keys, it
starts from her real sheet):

```powershell
.venv\Scripts\python automations\masterlist.py
.venv\Scripts\python site\tools\make_fake.py fake.xlsx
$env:UM_FAKE="fake.xlsx"; .venv\Scripts\python -m uvicorn app:app --app-dir site\server --port 8821
```

## 7. Video covers and her videos (optional, takes a while)

The pictures and small video files are not in git (too big). To make them:

```powershell
winget install -e --id yt-dlp.yt-dlp
winget install -e --id Gyan.FFmpeg
.venv\Scripts\python automations\media.py
```

Until then the site works, but video tiles show without pictures.

## 8. Later: move to her own cloud

When she is happy with it locally, the site can move to a cloud host she pays for
(for example, Railway, about $5 a month) so it works on her phone from anywhere.
What the host needs:

- start command: `uvicorn app:app --app-dir site/server --host 0.0.0.0 --port $PORT`,
  with `npm ci && npm run build` in `site/web` before it;
- a disk that survives restarts for `UM_STATE` (the site's database and stock photos);
- `google-key.json`, `source.txt` and `users.json` in the folder `UM_CONF` points to
  (her host's "secret files"), never in git;
- `UM_CONTENT` left empty (the project folder is used).

Tell Andrey once it works there, so he can turn his server copy off.

## The rest of the project

- `strategy/`, `research/`, `content/`: the plan, research and weekly video ideas.
- `automations/`: scripts that gather news and numbers and write weekly ideas (see
  `automations/README.md`). On Andrey's Mac they ran on a schedule. They are not needed for the website.
- Tests: `.venv\Scripts\python -m pytest -q site\tests automations\tests`.

## If something goes wrong

- "The page is not built yet": run step 3.
- The site shows no orders: run the check in step 4. If the check fails, the sheet may no longer be
  shared with the robot account (`unniemart-desk@unniemart.iam.gserviceaccount.com`, Editor).
- Anything else: send Andrey the last lines of the terminal.
