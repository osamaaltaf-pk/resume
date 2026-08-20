# Osama Altaf, Personal Profile Site

A fast, dependency-free static site (HTML + CSS + vanilla JS) with **two tailored versions**
of my profile plus a private share hub. Deploys to Vercel with zero configuration.

## Pages

| Path           | Audience                     | Emphasis                                             |
| -------------- | ---------------------------- | --------------------------------------------------- |
| `/`            | **Private hub** (me)         | Pick a version, copy its link, share only that page |
| `/companies`   | Companies & recruiters       | Industry-first: impact, experience, skills, projects |
| `/professors`  | University professors        | Research-first: education & CGPA, thesis, projects  |

Every page has an email contact block (copy-to-clipboard + `mailto:`) and a link to the
downloadable **ATS-friendly PDF resume** (`/Osama_Altaf_Resume.pdf`).

## Structure

```
index.html            # private share hub (noindex)
companies/index.html  # company/recruiter version
professors/index.html # professor / grad-school version
styles.css            # shared styles (light + dark)
script.js             # theme toggle, mobile nav, scrollspy, copy buttons
assets/               # photo + favicons
Osama_Altaf_Resume.pdf# generated ATS resume (single column, real text)
scripts/generate_pdf.py  # regenerates the PDF (fpdf2 + Arial)
vercel.json           # cleanUrls + cache headers
```

## Develop locally

Any static server works, e.g.:

```bash
python -m http.server 5173
# then open http://localhost:5173
```

## Regenerate the PDF resume

```bash
pip install fpdf2
python scripts/generate_pdf.py
```

Produces a single-column, standard-font (Arial), real-text PDF that parses cleanly in
Applicant Tracking Systems.

## Deploy on Vercel

1. Push this repo to GitHub.
2. On Vercel: **Add New… → Project → Import** the repo.
3. Framework preset: **Other**. No build command, no output directory. Served statically from root.
4. Deploy. Optionally add a custom domain.

---

© Osama Altaf · AI Engineer · [LinkedIn](https://www.linkedin.com/in/osamaaltafpk/) · [GitHub](https://github.com/osamaaltaf-pk)
