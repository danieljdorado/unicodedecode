# Unicode Decode
![Image of Logo for application site](https://www.nlpnotebook.com/static/projects/unicode.logolarge.png)
## Django Website for Unicode Character Search

## Description

Unicode Decode lets you inspect any text character by character: see each character’s name, general category, digit value, bidirectional class, and code point. You can check which Unicode normalization forms (NFC, NFKC, NFD, NFKD) your string is already in, and open detailed codepoint pages for every character. Useful for debugging text, learning Unicode, and verifying normalization.

## Features

- **Decode** — Paste text and click "Examine" to get a table of every character with: Character, Name, Category, Digit, Direction, Integer, Code Point. Character names link to codepoint detail pages.
- **Normalization** — Reports which of NFC, NFKC, NFD, and NFKD the input is already in.
- **Codepoint pages** — Detail view per character: name, category, digit, direction, decomposition, aliases, East Asian width, and upper/lower forms.
- **Tofu** — Informational page about missing glyphs.
- **Other pages** — About, Privacy, Terms.

## Tech stack

- **Backend:** Django (3.0–5.0), Python 3.
- **Frontend:** Materialize CSS (`unicodedecode/static/css/`, `unicodedecode/static/js/`).
- **Data:** Python standard library `unicodedata`, plus app utilities and `unicodedecode/files/NameAliases.txt` for character names and aliases.

## Getting started

**Prerequisites:** Python 3, pip.

**Setup:** From the project root (the directory that contains `manage.py` and `requirements.txt`):

> [!Note]
> These will be added to the repo at a different date.

1. Create and activate a virtual environment.
2. Run `pip install -r requirements.txt`.
3. Run migrations if the project uses a database: `python manage.py migrate`.

**Run:** From the project root, run `python manage.py runserver` and open the URL shown (e.g. http://127.0.0.1:8000/).

## Routes

| Path | Description |
|------|-------------|
| `/` | Decode: form and results table |
| `/about` | About |
| `/codepoint/<slug>` | Codepoint detail (e.g. `0041` for 'A') |
| `/tofu` | Tofu (missing glyphs) |
| `/terms` | Terms and Conditions |
| `/privacy` | Privacy Policy |

## Project structure

- **Project root:** `manage.py`, `requirements.txt`, `USearch/` (Django settings and root URLs), `unicodedecode/` (app).
- **App (`unicodedecode/`):** `views.py`, `forms.py`, `urls.py`, `unicode_util.py`, `mappings.py`, `templates/decode/`, `static/`, `files/NameAliases.txt`.

## Testing

Tests are in `unicodedecode/tests.py`. From the project root run:

- `pytest`, or
- `python manage.py test`

The project uses pytest and pytest-django (see `requirements.txt`).

## Screenshot
![Preview of unicode search site](https://www.nlpnotebook.com/static/projects/unicode_search.png)


## Acknowledgement

- [Cynthia McDonald](https://github.com/mcdonald-cyber) for providing Frontend support and logo design.
