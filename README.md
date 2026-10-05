# Smart Appointment Scheduler

Small personal demo I built to practice Selenium + page objects.

There's a fake clinic website in `demo_website/`, and a Python script that logs in, finds a patient, picks a doctor/time, and books an appointment. Nothing here is connected to a real clinic or real patient data.

## Stack

- HTML / CSS / JS (local demo site)
- Python + Selenium
- pytest
- credentials via `.env`

## Project layout

```
demo_website/     # fake UI you can click through in a browser
automation/       # selenium script + page objects
tests/            # a couple of basic tests
```

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# mac/linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env
```

## Run the demo site

```bash
cd demo_website
python -m http.server 5500
```

Open http://localhost:5500

Login:

- user: `demo_admin`
- pass: `demo_pass_123`

## Run the automation

Keep the site running, then from the project root:

```bash
python -m automation.scheduler
```

It should open Chrome, walk through the booking flow, and print the appointment id at the end.

Optional knobs in `.env`:

```
BASE_URL=http://localhost:5500
DEMO_USERNAME=demo_admin
DEMO_PASSWORD=demo_pass_123
PATIENT_QUERY=Ava Chen
DOCTOR_NAME=Dr. Sofia Rivera
HEADLESS=false
BROWSER=chrome
```

## Tests

Needs the demo site up on port 5500.

```bash
pytest -v
```

## Notes

- Page objects live under `automation/pages/`
- Uses explicit waits (no random `sleep()` calls)
- Driver is pulled in by `webdriver-manager`, so you usually don't need to install chromedriver yourself
