# Osama Altaf, Personal Profile Site

A fast, dependency-free static site (HTML + CSS + vanilla JS) with **three versions**
of my profile plus a private share hub. Deploys to Vercel with zero configuration.

## Pages

| Path           | Audience                     | Emphasis                                             |
| -------------- | ---------------------------- | --------------------------------------------------- |
| `/`            | **Private hub** (me)         | Pick a version, copy its link, share only that page |
| `/companies`   | Companies & recruiters       | Industry-first: impact, experience, skills, projects |
| `/professors`  | University professors        | Research-first: education & CGPA, thesis, projects  |
| `/personal`    | Anyone (bio / signature link) | First-person homepage: Now, what I want to study next, my story, News |

Each audience gets **its own PDF** - the two are not the same document:

| PDF | Linked from | Emphasis |
| --- | --- | --- |
| `Osama_Altaf_Resume.pdf` | `/companies` | ATS-friendly industry resume: summary, skills, employment, selected projects |
| `Osama_Altaf_Academic_CV.pdf` | `/professors` | Academic CV: research interests, education with coursework and thesis, research projects first, employment condensed, academic service |

Every page has an email contact block (copy-to-clipboard + `mailto:`) and a link to the PDF
for its own audience.

## Structure

```
index.html            # private share hub (noindex)
companies/index.html  # company/recruiter version
professors/index.html # professor / grad-school version
personal/index.html   # personal academic-style homepage (Now + News)
styles.css            # shared styles (light + dark)
script.js             # theme toggle, mobile nav, scrollspy, copy buttons
assets/               # photo + favicons
Osama_Altaf_Resume.pdf     # generated ATS industry resume (single column, real text)
Osama_Altaf_Academic_CV.pdf# generated academic CV (research-first ordering)
scripts/generate_pdf.py        # regenerates the industry resume (fpdf2 + Arial)
scripts/generate_cv_academic.py# regenerates the academic CV
vercel.json           # cleanUrls + cache headers
```

## Develop locally

Any static server works, e.g.:

```bash
python -m http.server 5173
# then open http://localhost:5173
```

## Regenerate the PDFs

```bash
pip install fpdf2
python scripts/generate_pdf.py          # -> Osama_Altaf_Resume.pdf     (industry)
python scripts/generate_cv_academic.py # -> Osama_Altaf_Academic_CV.pdf (academic)
```

Both read Arial from `C:\Windows\Fonts`; adjust `FONT_DIR` on other platforms.

**CGPA is 3.63/4.00**, per the official KFUEIT final transcript (134/134 credit hours, 90%).

Produces a single-column, standard-font (Arial), real-text PDF that parses cleanly in
Applicant Tracking Systems.

## Deploy on Vercel

1. Push this repo to GitHub.
2. On Vercel: **Add New… → Project → Import** the repo.
3. Framework preset: **Other**. No build command, no output directory. Served statically from root.
4. Deploy. Optionally add a custom domain.

---

© Osama Altaf · AI Engineer · [LinkedIn](https://www.linkedin.com/in/osamaaltafpk/) · [GitHub](https://github.com/osamaaltaf-pk)
