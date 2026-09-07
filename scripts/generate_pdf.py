#!/usr/bin/env python
"""
Generates an ATS-friendly, US-standard PDF resume for Osama Altaf.

Design goals:
- Single column, standard font (Arial), real selectable text -> parses cleanly in ATS.
- No photo, no tables-for-layout, no text boxes. Just headings, bullets, links.
- Two pages, tight but readable.
Run:  python scripts/generate_pdf.py
Output: public/Osama_Altaf_Resume.pdf
"""
import os
from fpdf import FPDF

FONT_DIR = r"C:\Windows\Fonts"
OUT = os.path.join(os.path.dirname(__file__), "..", "Osama_Altaf_Resume.pdf")

# --- palette ---
INK = (17, 24, 39)       # near-black
MUTE = (75, 85, 99)      # gray
ACCENT = (37, 99, 235)   # blue
RULE = (209, 213, 219)   # light gray rule

NAME = "Osama Altaf"
TITLE = "Founder & CEO, Wisko (wiskoai.com)  |  AI Engineer - LLM & Voice AI"


class Resume(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-11)
        self.set_font("Arial", "", 7.5)
        self.set_text_color(*MUTE)
        self.cell(0, 5, f"Osama Altaf  -  AI Engineer", align="L")
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R")


pdf = Resume(orientation="P", unit="mm", format="Letter")
pdf.set_auto_page_break(auto=True, margin=14)
pdf.set_margins(left=15, top=13, right=15)
pdf.alias_nb_pages()

# Register Arial (full Unicode: dashes, bullets, etc.)
pdf.add_font("Arial", "", os.path.join(FONT_DIR, "arial.ttf"))
pdf.add_font("Arial", "B", os.path.join(FONT_DIR, "arialbd.ttf"))
pdf.add_font("Arial", "I", os.path.join(FONT_DIR, "ariali.ttf"))
pdf.add_font("Arial", "BI", os.path.join(FONT_DIR, "arialbi.ttf"))

pdf.add_page()
EPW = pdf.epw  # effective page width


def section(title):
    pdf.ln(2.2)
    pdf.set_font("Arial", "B", 10.5)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 5.4, title.upper(), new_x="LMARGIN", new_y="NEXT")
    y = pdf.get_y()
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, y, pdf.l_margin + EPW, y)
    pdf.ln(1.6)


def role(title, meta, when):
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "I", 8.8)
    pdf.set_text_color(*MUTE)
    # meta line left, dates right
    y = pdf.get_y()
    pdf.cell(EPW * 0.72, 4.6, meta)
    pdf.set_font("Arial", "", 8.8)
    pdf.cell(EPW * 0.28, 4.6, when, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.6)


def bullets(items):
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(*INK)
    for it in items:
        x = pdf.get_x()
        pdf.set_text_color(*ACCENT)
        pdf.cell(4, 4.6, "-")
        pdf.set_text_color(*INK)
        pdf.set_x(x + 4)
        pdf.multi_cell(EPW - 4, 4.6, it, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.8)


def labeled(label, text):
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(*INK)
    lw = pdf.get_string_width(label + " ") + 1
    x = pdf.get_x()
    pdf.cell(lw, 4.8, label)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(*INK)
    pdf.set_x(x + lw)
    pdf.multi_cell(EPW - lw, 4.8, text, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.4)


# ---------------- HEADER ----------------
pdf.set_font("Arial", "B", 22)
pdf.set_text_color(*INK)
pdf.cell(0, 9, NAME, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", "", 10.5)
pdf.set_text_color(*ACCENT)
pdf.cell(0, 5.6, TITLE, new_x="LMARGIN", new_y="NEXT")
pdf.ln(1.2)

# contact line 1
pdf.set_font("Arial", "", 9)
pdf.set_text_color(*MUTE)
contact = "Pakistan  |  (+92) 318 7661096  |  osamaaltaf.pk@gmail.com"
pdf.cell(0, 4.8, contact, new_x="LMARGIN", new_y="NEXT")
# links line with real hyperlinks
pdf.set_text_color(*ACCENT)
seg = "linkedin.com/in/osamaaltafpk"
pdf.cell(pdf.get_string_width(seg) + 1, 4.8, seg,
         link="https://www.linkedin.com/in/osamaaltafpk/")
pdf.set_text_color(*MUTE)
pdf.cell(pdf.get_string_width("   |   ") , 4.8, "   |   ")
pdf.set_text_color(*ACCENT)
seg2 = "github.com/osamaaltaf-pk"
pdf.cell(pdf.get_string_width(seg2) + 1, 4.8, seg2,
         link="https://github.com/osamaaltaf-pk", new_x="LMARGIN", new_y="NEXT")

# ---------------- SUMMARY ----------------
section("Summary")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(*INK)
summary = ("Founder and CEO of Wisko (wiskoai.com), a multi-tenant AI SaaS whiteboard-animation platform, and an "
           "AI Engineer specializing in production-grade large language model systems, real-time voice AI, "
           "and agentic automation. Experience ranges from multilingual voice platforms handling live telephony "
           "to a government-grade real-time translation system spanning 30+ languages. Focused on making models "
           "deployment-ready: fine-tuning LLMs and vision-language models, hyperparameter tuning, and accelerating "
           "inference with KV caching and quantization using PipeCat, LiveKit, LangChain, LangGraph, and CrewAI.")
pdf.multi_cell(EPW, 4.7, summary, align="L", new_x="LMARGIN", new_y="NEXT")

# ---------------- SKILLS ----------------
section("Technical Skills")
labeled("LLM & GenAI:", "Fine-tuning, RAG, quantization, KV cache, prompt engineering, transformers, vision-language models")
labeled("Frameworks:", "LangChain, LangGraph, CrewAI, AutoGen, PipeCat, LiveKit, Hugging Face")
labeled("Voice AI:", "Whisper ASR, STT/TTS pipelines, SIP trunking, WebRTC, real-time telephony")
labeled("Inference & MLOps:", "vLLM, LMCache, AIBrix, Docker, model deployment, MLOps")
labeled("Backend & Data:", "Python, FastAPI, Redis, REST APIs, Pinecone, Weaviate, Qdrant, vector databases")
labeled("Automation:", "n8n, Make, Zapier")

# ---------------- EXPERIENCE ----------------
section("Professional Experience")
role("Founder & CEO - Wisko (wiskoai.com)", "Multi-tenant AI SaaS - Whiteboard Animation Studio", "Current")
bullets([
    "Founded and lead Wisko, a multi-tenant SaaS platform where an agentic pipeline turns a prompt into a finished whiteboard-animation video.",
    "Own product direction, system architecture, and the agentic content-generation stack.",
])
role("AI Engineer - LLM Systems Research & Analyst (Contract, Remote)", "London, United Kingdom", "Jul 2025 - Jan 2026")
bullets([
    "Deployed and scaled large language models for smart assistants and task automation at company level.",
    "Used vLLM for high-throughput, low-latency inference with efficient KV cache use.",
    "Integrated AIBrix multi-agent orchestration to coordinate tools and APIs into goal-driven agent workflows.",
    "Fine-tuned LLMs on proprietary datasets to align outputs with company-specific terminology.",
    "Built scalable FastAPI services with in-memory caching via LMCache and Redis.",
])
role("AI Voice Agent Developer & Research Analyst - Government Real-Time Translation System",
     "Confidential GovTech Project, Remote  -  Morocco", "Feb 2025 - Jun 2025")
bullets([
    "Co-developed a real-time multilingual communication system with bi-directional translation across 30+ languages.",
    "Integrated Whisper ASR with custom speech pipelines, achieving sub-1500 ms latency using LiveKit and PipeCat.",
    "Engineered context-aware memory modules to retain conversational history and ensure cross-language consistency.",
    "Met government-grade security, privacy, and performance standards.",
])
role("AI Engineer - Voice AI Agent Platform (US Project, Remote)", "Miami, United States", "Nov 2024 - Feb 2025")
bullets([
    "Designed a scalable Voice AI platform supporting inbound/outbound telephony via SIP trunk routing.",
    "Built modular, no-code agent workflow builders enabling users to define dynamic call flows.",
    "Integrated LangGraph-powered agents for context-aware, multi-turn conversations.",
    "Hardened Speech-to-Text and Text-to-Speech pipelines for production reliability.",
])
role("Associate Business Development (Internship, Remote)", "iAxon Software House", "Oct 2023 - Feb 2024")
bullets([
    "Conducted market analysis that drove a 10% increase in client acquisition.",
    "Coordinated product launches, consistently meeting or exceeding deadlines.",
    "Improved client communication strategies, increasing retention and satisfaction.",
])
role("Junior AI Engineer (Intern)", "iAxon Software House", "Apr 2023 - Oct 2023")
bullets([
    "Optimized model-training workflows, cutting compute time 30% via improved feature engineering.",
    "Built Python predictive-modeling solutions, improving forecasting accuracy 15%.",
    "Fine-tuned ML models across diverse domains and automated data processing (+20% team productivity).",
])

# ---------------- EDUCATION ----------------
section("Education")
role("BS Physics - Computational Physics & Computer Programming",
     "Khwaja Fareed University of Engineering & IT (KFUEIT), Pakistan", "CGPA 3.63 / 4.00")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(*INK)
pdf.multi_cell(EPW, 4.6, "Thesis: Object Detection Transformer model for disease detection on cotton leaves.",
               new_x="LMARGIN", new_y="NEXT")
pdf.ln(1.2)
labeled("Additional:", "Machine Learning, MLOps & LLM Zoomcamps - DataTalks.Club (2023).  "
                        "F.Sc. Pre-Medical, BISE Bahawalpur - 89%.  Matriculation, BISE Bahawalpur - 95%.")

# ---------------- PROJECTS ----------------
section("Selected Projects")
bullets([
    "Airport Vehicle Detection, Vision vs. LiDAR (freelance research, UK): Benchmarked a range of computer-vision "
    "models for detecting vehicles at airports, assessing whether camera-based systems can replace LiDAR by "
    "estimating depth, distance, and detection quality across varied lighting, seasons, and weather.",
    "Cotton Disease Detection Transformer (Final Year Project): Vision Transformer with an AI digital microscope "
    "for accurate cotton-crop disease detection from visual symptoms; outperformed CNN baselines.",
    "Autonomous Financial Analyst Swarm: Multi-agent CrewAI system that scrapes market news, runs sentiment "
    "analysis, and drafts investment memos with self-correction loops and tool use.",
    "Secure Enterprise RAG Knowledge Base: Privacy-preserving document assistant on local Llama 3 and Qdrant "
    "for semantic search with no external data leakage.",
    "Edge-AI Industrial Safety Monitor: YOLOv8 PPE detection on NVIDIA Jetson Orin Nano at <40 ms offline "
    "inference for low-bandwidth factory environments.",
    "Portable Radar System: Raspberry Pi remote-sensing radar with real-time Python signal processing for "
    "distance and velocity estimation.",
])

# ---------------- CERTIFICATIONS ----------------
section("Certifications")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(*INK)
certs = ("DeepLearning.AI: Fine-Tuning LLMs; LLMOps - Deployment & Inference; Building AI Voice Agents for "
         "Production; Practical Multi-AI Agents with CrewAI; AI Agentic Design Patterns with AutoGen; Evaluating "
         "AI Agents; Vector Databases: From Embeddings to Applications; LangChain for LLM App Development; "
         "Building Coding Agents.   edX (IBM): Mastering Generative AI - Agents with RAG & LangChain.   "
         "DataTalks.Club: MLOps & LLM Zoomcamp.")
pdf.multi_cell(EPW, 4.6, certs, align="L", new_x="LMARGIN", new_y="NEXT")

# ---------------- LANGUAGES ----------------
section("Languages")
labeled("English:", "IELTS 7.5 (C2 Listening & Reading; C1 Speaking & Writing)")
labeled("Urdu:", "Native")

# ---------------- LEADERSHIP ----------------
section("Leadership & Activities")
bullets([
    "President, Natural Resources Defense Council & Society, KFUEIT.",
    "Organizer of ICPSE-2021 and ICPSE-2022 (International Conferences on Physical Sciences & Engineering) and "
    "ICSMAND (9th International Conference on Semiconductor Materials & Nano-Devices).",
    "Organized the 1st South Punjab Science Mela 2021 and a Blood Donation Camp at Sehja Public Health Care Centre.",
    "Student Proctor at the 1st KFUEIT Convocation; Organizer and Cricketer at the Annual Sports Gala.",
])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
pdf.output(OUT)
print("Wrote", os.path.abspath(OUT), "pages:", pdf.page_no())
