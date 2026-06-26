import pdfplumber, sys
for f in ["grade4_hani_20181214.pdf","grade3_hani_20181214.pdf","grade2_hani_20181214.pdf"]:
    print("\n\n########## ", f, " ##########")
    with pdfplumber.open("pdfs/"+f) as pdf:
        for i,page in enumerate(pdf.pages):
            t = page.extract_text() or ""
            print(f"\n----- page {i+1} -----")
            print(t)
