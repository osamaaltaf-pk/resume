#!/usr/bin/env python
"""One-off: remove all em/en dashes, humanize phrasing, fix London role dates."""
import re

def apply(path, reps, regexes=None):
    s = open(path, encoding="utf-8").read()
    missing = []
    for old, new in reps:
        if old in s:
            s = s.replace(old, new)
        else:
            missing.append(old[:60])
    for pat, rep in (regexes or []):
        s = re.sub(pat, rep, s)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(f"{path}: em={s.count(chr(0x2014))} en={s.count(chr(0x2013))}"
          + (f"  MISSING={missing}" if missing else "  (all matched)"))

shared = [
 ('aria-label="Osama Altaf — home"', 'aria-label="Osama Altaf home"'),
 ('<h3>AI Engineer — LLM Systems Research &amp; Analyst</h3>',
  '<h3>AI Engineer, LLM Systems Research &amp; Analyst</h3>'),
 ('<div class="job-when">Jul 2025 — Present</div>', '<div class="job-when">Jul 2025 to Jan 2026</div>'),
 ('<div class="job-when">Feb 2025 — Jun 2025</div>', '<div class="job-when">Feb 2025 to Jun 2025</div>'),
 ('<div class="job-when">Nov 2024 — Feb 2025</div>', '<div class="job-when">Nov 2024 to Feb 2025</div>'),
 ('<div class="job-when">Oct 2023 — Feb 2024</div>', '<div class="job-when">Oct 2023 to Feb 2024</div>'),
 ('<div class="job-when">Apr 2023 — Oct 2023</div>', '<div class="job-when">Apr 2023 to Oct 2023</div>'),
 ('<div class="job-when">Apr 2023 — Feb 2024</div>', '<div class="job-when">Apr 2023 to Feb 2024</div>'),
 ('Contract · Remote — London, United Kingdom', 'Contract · Remote · London, United Kingdom'),
 ('Confidential GovTech · Remote — Morocco', 'Confidential GovTech · Remote · Morocco'),
 ('<h3>AI Engineer — Voice AI Agent Platform</h3>', '<h3>AI Engineer, Voice AI Agent Platform</h3>'),
 ('US Project · Remote — Miami, United States', 'US Project · Remote · Miami, United States'),
 ('<li><span>LLMOps — Deployment &amp; Inference</span>', '<li><span>LLMOps: Deployment &amp; Inference</span>'),
 ('IELTS 7.5 — C2 Listening &amp; Reading; C1 Speaking &amp; Writing',
  'IELTS 7.5, with C2 Listening and Reading and C1 Speaking and Writing'),
 ('<h3>BS Physics — Computational Physics &amp; Computer Programming</h3>',
  '<h3>BS Physics, Computational Physics &amp; Computer Programming</h3>'),
 ('Deploy and scale large language models for smart assistants and task automation at company level.',
  'Deployed and scaled large language models for smart assistants and task automation at company level.'),
 ('Leverage vLLM for high-throughput, low-latency inference with efficient KV cache utilization.',
  'Used vLLM for high-throughput, low-latency inference with efficient KV cache use.'),
 ('Integrate AIBrix multi-agent orchestration to coordinate tools and APIs into goal-driven agent workflows.',
  'Integrated AIBrix multi-agent orchestration to coordinate tools and APIs into goal-driven agent workflows.'),
 ('Fine-tune LLMs on proprietary datasets to align outputs with company-specific terminology.',
  'Fine-tuned LLMs on proprietary datasets to align outputs with company-specific terminology.'),
 ('Build scalable FastAPI services with in-memory caching via LMCache and Redis.',
  'Built scalable FastAPI services with in-memory caching via LMCache and Redis.'),
 ('Deploy and scale large language models for smart assistants and task automation.',
  'Deployed and scaled large language models for smart assistants and task automation.'),
 ('Use vLLM for high-throughput, low-latency inference with efficient KV cache utilization.',
  'Used vLLM for high-throughput, low-latency inference with efficient KV cache use.'),
 ('Integrate multi-agent orchestration (AIBrix) to coordinate tools and APIs into goal-driven workflows.',
  'Integrated multi-agent orchestration (AIBrix) to coordinate tools and APIs into goal-driven workflows.'),
 ('Fine-tune LLMs on proprietary datasets; build FastAPI services with LMCache/Redis caching.',
  'Fine-tuned LLMs on proprietary datasets and built FastAPI services with LMCache and Redis caching.'),
]
shared_re = [(r'(class="kicker">\d\d) — ', r'\1 · ')]

companies = shared + [
 ('<title>Osama Altaf — AI Engineer | LLM Systems, Voice AI & Agentic Automation</title>',
  '<title>Osama Altaf | AI Engineer, LLM Systems, Voice AI & Agentic Automation</title>'),
 ('<meta property="og:title" content="Osama Altaf — AI Engineer" />',
  '<meta property="og:title" content="Osama Altaf, AI Engineer" />'),
 ('agentic automation</strong> — from a multi-tenant SaaS content platform to a\n        government-grade translation system spanning 30+ languages, with a focus on latency,\n        cost, and reliability.',
  'agentic automation</strong>. My work ranges from a multi-tenant SaaS content platform to a\n        government-grade translation system spanning 30+ languages, and I keep a close eye on latency,\n        cost, and reliability.'),
 ('<span class="stat-l">CGPA — BS Physics (KFUEIT)</span>', '<span class="stat-l">CGPA, BS Physics (KFUEIT)</span>'),
 ('<!-- FLAGSHIP — Founder product -->', '<!-- FLAGSHIP: Founder product -->'),
 ('<p>My venture — a full <strong>multi-tenant SaaS</strong> platform: an AI whiteboard-animation studio where an <strong>agentic content-creation</strong> pipeline turns a prompt into finished animated videos, end to end.</p>',
  '<p>My company. Wisko is a full <strong>multi-tenant SaaS</strong> platform: an AI whiteboard-animation studio where an <strong>agentic content-creation</strong> pipeline turns a prompt into a finished animated video.</p>'),
 ("I'm an AI Engineer who enjoys building smart systems that hold up in production —",
  "I'm an AI Engineer who enjoys building smart systems that hold up in production,"),
 ('<strong>BS Physics, KFUEIT — CGPA 3.63/4.00</strong>', '<strong>BS Physics, KFUEIT, CGPA 3.63/4.00</strong>'),
 ('draft investment memos — featuring self-correction loops and tool use.',
  'draft investment memos, with self-correction loops and tool use.'),
 ('bulk AI image and video generation — queue and produce media at scale from a single interface.',
  'bulk AI image and video generation, so you can queue and produce media at scale from one interface.'),
 ('to manage routes, sources, and configuration — live for a real pay-per-call business.',
  'to manage routes, sources, and configuration. It is live for a real pay-per-call business.'),
 ('<h3>Wstorage — Secure Internal File Storage</h3>', '<h3>Wstorage: Secure Internal File Storage</h3>'),
 ('for company teams — authenticated uploads, organization, and retrieval of internal files behind access control.',
  'for company teams, with authenticated uploads, organization, and retrieval of internal files behind access control.'),
 ('<h3>AutoStitch — Video Editing Desktop App</h3>', '<h3>AutoStitch: Video Editing Desktop App</h3>'),
 ('the fastest way to reach me is email — copy it below or click to open your mail app.',
  'the fastest way to reach me is email. Copy it below, or click to open your mail app.'),
 ('subject=AI%20Engineer%20role%20%E2%80%94%20Osama%20Altaf', 'subject=AI%20Engineer%20role%20from%20Osama%20Altaf'),
]

professors = shared + [
 ('<title>Osama Altaf — AI Researcher &amp; Engineer | LLM & Computer Vision</title>',
  '<title>Osama Altaf | AI Researcher &amp; Engineer, LLM & Computer Vision</title>'),
 ('<meta name="description" content="Osama Altaf — AI engineer and aspiring researcher in large language models, computer vision, and voice AI. BS Physics, CGPA 3.63/4.00. Research, projects, and academic CV." />',
  '<meta name="description" content="Osama Altaf, AI engineer and aspiring researcher in large language models, computer vision, and voice AI. BS Physics, CGPA 3.63/4.00. Research, projects, and academic CV." />'),
 ('<meta property="og:title" content="Osama Altaf — AI Researcher & Engineer" />',
  '<meta property="og:title" content="Osama Altaf, AI Researcher & Engineer" />'),
 ('<span class="stat-l">CGPA — BS Physics (US 4.0 scale GPA 3.63)</span>',
  '<span class="stat-l">CGPA, BS Physics (US 4.0 scale GPA 3.63)</span>'),
 ('<!-- FLAGSHIP — Founder product -->', '<!-- FLAGSHIP: Founder product -->'),
 ('<p>My venture — a <strong>multi-tenant SaaS</strong> platform where autonomous <strong>agents</strong> generate complete whiteboard-animation videos end to end: applied agentic AI and multimodal generation running in production.</p>',
  '<p>My company. Wisko is a <strong>multi-tenant SaaS</strong> platform where autonomous <strong>agents</strong> generate complete whiteboard-animation videos: applied agentic AI and multimodal generation running in production.</p>'),
 ('and an AI digital microscope to detect cotton-crop diseases from visual symptoms —',
  'and an AI digital microscope to detect cotton-crop diseases from visual symptoms,'),
 ('<strong>BS Physics (Computational) — CGPA 3.63 / 4.00</strong>',
  '<strong>BS Physics (Computational), CGPA 3.63 / 4.00</strong>'),
 ('Pakistan · 2019–2023', 'Pakistan · 2019 to 2023'),
 ('Pakistan · 2017–2019 ·', 'Pakistan · 2017 to 2019 ·'),
 ('Pakistan · 2015–2017 ·', 'Pakistan · 2015 to 2017 ·'),
 ('radiography imagery — adapting a vision-language model to medical image understanding.',
  'radiography imagery, adapting a vision-language model to medical image understanding.'),
 ('diffusion transformer to ONNX — enabling CPU/GPU inference without a PyTorch runtime dependency.',
  'diffusion transformer to ONNX, so it runs CPU/GPU inference without a PyTorch runtime dependency.'),
 ('on Supabase &amp; GCS — an end-to-end multimodal generation system.',
  'on Supabase &amp; GCS, running as a full multimodal generation system.'),
 ('The best way to reach me is email — copy it below or click to open your mail app.',
  'The best way to reach me is email. Copy it below, or click to open your mail app.'),
 ('subject=Graduate%20research%20inquiry%20%E2%80%94%20Osama%20Altaf', 'subject=Graduate%20research%20inquiry%20from%20Osama%20Altaf'),
]

apply("companies/index.html", companies, shared_re)
apply("professors/index.html", professors, shared_re)
apply("index.html", [
 ('<title>Osama Altaf — Share Hub</title>', '<title>Osama Altaf | Share Hub</title>'),
 ('aria-label="Osama Altaf — home"', 'aria-label="Osama Altaf home"'),
 ('versions of your profile — one for', 'versions of your profile: one for'),
])
apply("README.md", [
 ('# Osama Altaf — Personal Profile Site', '# Osama Altaf, Personal Profile Site'),
 ('No build command, no output directory — served statically from root.',
  'No build command, no output directory. Served statically from root.'),
 ('© Osama Altaf — AI Engineer ·', '© Osama Altaf · AI Engineer ·'),
])
