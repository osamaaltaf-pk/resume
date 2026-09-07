#!/usr/bin/env python
"""
Generates the ACADEMIC CV for Osama Altaf - the version linked from /professors.

Differs from the industry resume (scripts/generate_pdf.py) in ordering and emphasis:
  Research interests -> Education (coursework + thesis) -> Research experience
  -> Professional experience (condensed) -> Skills -> Service -> Certifications.

Design goals: single column, real selectable text, no photo, no layout tables.
Run:  python scripts/generate_cv_academic.py
Out:  Osama_Altaf_Academic_CV.pdf
"""
import os
from fpdf import FPDF

FONT_DIR = r"C:\Windows\Fonts"
OUT = os.path.join(os.path.dirname(__file__), "..", "Osama_Altaf_Academic_CV.pdf")

INK, MUTE, ACCENT, RULE = (17, 24, 39), (75, 85, 99), (37, 99, 235), (209, 213, 219)

NAME = "Osama Altaf"
TITLE = "AI Researcher & Engineer  |  Vision-Language Models, Medical Imaging, Computer Vision"


class CV(FPDF):
    def footer(self):
        self.set_y(-11)
        self.set_font("Arial", "", 7.5)
        self.set_text_color(*MUTE)
        self.cell(0, 5, "Osama Altaf  -  Academic CV", align="L")
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R")


pdf = CV(orientation="P", unit="mm", format="Letter")
pdf.set_auto_page_break(auto=True, margin=14)
pdf.set_margins(left=15, top=13, right=15)
pdf.alias_nb_pages()
for style, fname in (("", "arial.ttf"), ("B", "arialbd.ttf"),
                     ("I", "ariali.ttf"), ("BI", "arialbi.ttf")):
    pdf.add_font("Arial", style, os.path.join(FONT_DIR, fname))
pdf.add_page()
EPW = pdf.epw


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
    pdf.cell(EPW * 0.70, 4.6, meta)
    pdf.set_font("Arial", "", 8.8)
    pdf.cell(EPW * 0.30, 4.6, when, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.6)


def bullets(items):
    pdf.set_font("Arial", "", 9)
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
    pdf.set_x(x + lw)
    pdf.multi_cell(EPW - lw, 4.8, text, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.4)


def para(text):
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(*INK)
    pdf.multi_cell(EPW, 4.7, text, align="L", new_x="LMARGIN", new_y="NEXT")


# ---------------- HEADER ----------------
pdf.set_font("Arial", "B", 22)
pdf.set_text_color(*INK)
pdf.cell(0, 9, NAME, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", "", 10)
pdf.set_text_color(*ACCENT)
pdf.cell(0, 5.6, TITLE, new_x="LMARGIN", new_y="NEXT")
pdf.ln(1.2)
pdf.set_font("Arial", "", 9)
pdf.set_text_color(*MUTE)
pdf.cell(0, 4.8, "Pakistan (open to relocation)  |  (+92) 318 7661096  |  osamaaltaf.pk@gmail.com",
         new_x="LMARGIN", new_y="NEXT")

LINKS = [("github.com/osamaaltaf-pk", "https://github.com/osamaaltaf-pk"),
         ("linkedin.com/in/osamaaltafpk", "https://www.linkedin.com/in/osamaaltafpk/"),
         ("osama-altaf.vercel.app", "https://osama-altaf.vercel.app/professors")]
for i, (label, url) in enumerate(LINKS):
    if i:
        pdf.set_text_color(*MUTE)
        pdf.cell(pdf.get_string_width("  |  "), 4.8, "  |  ")
    pdf.set_text_color(*ACCENT)
    last = (i == len(LINKS) - 1)
    pdf.cell(pdf.get_string_width(label) + 1, 4.8, label, link=url,
             new_x="LMARGIN" if last else "RIGHT",
             new_y="NEXT" if last else "TOP")

# ---------------- RESEARCH INTERESTS ----------------
section("Research Interests")
para("Vision-language models for medical imaging, with a focus on visual grounding: producing answers that can be "
     "traced back to the region of the scan they came from, rather than captions for a whole volume. Related "
     "interests in segmentation, 3D medical imaging, multimodal representation learning, and the construction and "
     "validation of benchmarks that hold up under distribution shift across sites and acquisition conditions.")

# ---------------- EDUCATION ----------------
section("Education")
role("BS Physics - Computational Physics & Computer Programming",
     "Khwaja Fareed University of Engineering & IT (KFUEIT), Rahim Yar Khan, Pakistan", "2019 - 2023")
labeled("CGPA:", "3.63 / 4.00  -  134 / 134 credit hours  -  overall 90 percent  -  EQF Level 6. "
                 "Final-year semester GPAs of 3.82 and 3.94.")
labeled("Thesis:", "Object Detection Transformer for disease detection on cotton leaves. Designed a "
                   "transformer-based detector coupled with an AI-modelled digital microscope to identify "
                   "cotton-crop disease from visual symptoms; outperformed CNN baselines on classification accuracy.")
labeled("Relevant coursework:", "Introduction to Computational Physics (A), Linear Algebra (A), Probability and "
                                "Statistics (A), Mathematical Methods of Physics I-II, Introduction to Computer "
                                "Programming and Applications (A+), Digital Electronics (A+), Statistical Mechanics "
                                "(A), Solid State Physics I-II (A), Nuclear Physics (A+), Introduction to "
                                "Nanoscience and Nanotechnologies (A), Technical Writing and Presentation Skills (A).")
pdf.ln(0.6)
labeled("Additional training:", "Machine Learning, MLOps and LLM Zoomcamps - DataTalks.Club (2023).")
labeled("Pre-university:", "F.Sc. Pre-Medical, BISE Bahawalpur (89 percent). Matriculation, BISE Bahawalpur "
                           "(95 percent).")

# ---------------- RESEARCH EXPERIENCE ----------------
section("Research Experience & Projects")
role("Vision-Language Fine-Tuning on Radiography", "Independent research project - multimodal ML", "2025 - 2026")
bullets([
    "Fine-tuned Llama 3.2 Vision with Unsloth and LoRA on radiography imagery, adapting a general vision-language "
    "model to medical image understanding.",
    "Observed that report-like fluency emerges long before verifiable grounding: the model describes findings "
    "confidently while the supporting evidence stays untraceable to a region. This motivates my current interest "
    "in grounded medical VLMs.",
])
role("Visual Grounding Pipeline for Chest Radiographs", "Independent project - multimodal ML", "2025")
bullets([
    "Built a five-stage pipeline that forces a model to commit to a location: multimodal analysis, grounded "
    "retrieval, normalised bounding-box emission, box rendering onto the source image, and a clinician-facing "
    "discussion stage.",
    "Demonstrates region-level accountability in 2D, and makes explicit how much scarcer grounded supervision is "
    "than descriptive supervision.",
])
role("Airport Vehicle Detection: Vision versus LiDAR", "Freelance research study for a UK-based researcher", "2025")
bullets([
    "Benchmarked a range of computer-vision detection and depth-estimation models against LiDAR for vehicle "
    "detection at airports, across varying lighting, seasonal and weather conditions.",
    "The central finding was the instability of model ranking under distribution shift: aggregate accuracy was a "
    "poor predictor of behaviour once acquisition conditions changed.",
])
role("Edge-AI Vision on NVIDIA Jetson", "Embedded computer vision", "2024 - 2025")
bullets([
    "Deployed quantised YOLOv8 detection to a Jetson Orin Nano at sub-40 ms fully offline inference for "
    "low-bandwidth environments.",
])
role("Physics Instrumentation & Remote Sensing", "Undergraduate hardware projects", "2021 - 2023")
bullets([
    "Portable Raspberry Pi radar for remote sensing with real-time signal processing for distance and velocity "
    "estimation; IoT safety systems including a blind-spot accident-prevention module and a gas-leakage detector.",
])

# ---------------- PROFESSIONAL ----------------
section("Professional Experience")
role("Founder & CEO - Wisko (wiskoai.com)", "Multi-tenant agentic AI SaaS - whiteboard animation", "Current")
bullets([
    "Lead a platform where an agentic pipeline turns a prompt into a finished animation; own the architecture and "
    "the multimodal generation stack.",
])
role("AI Engineer - LLM Systems Research & Analyst", "Contract, remote - London, United Kingdom",
     "Jul 2025 - Jan 2026")
bullets([
    "Deployed and scaled LLMs with vLLM for high-throughput, low-latency inference and efficient KV-cache use.",
    "Fine-tuned models on proprietary corpora; built FastAPI services with LMCache and Redis caching.",
])
role("AI Voice Agent Developer & Research Analyst", "Confidential GovTech project, remote - Morocco",
     "Feb 2025 - Jun 2025")
bullets([
    "Co-developed real-time bi-directional translation across 30+ languages at sub-1500 ms latency, integrating "
    "Whisper ASR with custom speech pipelines and context-aware memory.",
])
role("AI Engineer - Voice AI Agent Platform", "US project, remote - Miami, United States", "Nov 2024 - Feb 2025")
bullets([
    "Designed a telephony-scale voice platform with SIP routing and LangGraph agents for multi-turn conversation.",
])
role("Junior AI Engineer (Intern)", "iAxon Software House, Pakistan", "Apr 2023 - Feb 2024")
bullets([
    "Cut model-training compute time 30 percent through feature engineering; improved forecasting accuracy "
    "15 percent.",
])

# ---------------- SKILLS ----------------
section("Technical Skills")
labeled("Vision & multimodal:", "Vision transformers, object detection, visual grounding, vision-language models, "
                                "depth estimation, PyTorch, OpenCV")
labeled("LLM & training:", "LoRA / QLoRA, Unsloth, GRPO, quantisation, KV cache, RAG, Hugging Face, TRL")
labeled("Inference & MLOps:", "vLLM, ONNX Runtime, Docker, FastAPI, edge deployment (Jetson Orin Nano), managed "
                              "cloud training and evaluation")
labeled("Data & retrieval:", "Qdrant, Pinecone, Weaviate, Redis, PostgreSQL")
labeled("Scientific foundations:", "Computational physics, mathematics, statistics, signal processing")

# ---------------- SERVICE ----------------
section("Academic Service & Leadership")
bullets([
    "Conference organiser: ICPSE-2021 and ICPSE-2022 (International Conferences on Physical Sciences and "
    "Engineering); ICSMAND (9th International Conference on Semiconductor Materials and Nano-Devices).",
    "President, Natural Resources Defence Council and Society, KFUEIT.",
    "Organised the 1st South Punjab Science Mela (2021); student proctor at the 1st KFUEIT Convocation.",
])

# ---------------- LANGUAGES & CERTS ----------------
section("Languages & Certifications")
labeled("English:", "IELTS 7.5 overall - C2 Listening and Reading, C1 Speaking and Writing.")
labeled("Urdu:", "Native.")
labeled("Certifications:", "DeepLearning.AI - Fine-Tuning LLMs; LLMOps: Deployment and Inference; Building AI Voice "
                           "Agents for Production; Practical Multi-AI Agents with CrewAI; AI Agentic Design Patterns "
                           "with AutoGen; Evaluating AI Agents; Vector Databases; LangChain for LLM App Development. "
                           "edX / IBM - Generative AI: Agents with RAG and LangChain. DataTalks.Club - MLOps and "
                           "LLM Zoomcamp.")

pdf.output(OUT)
print("Wrote", os.path.abspath(OUT), "pages:", pdf.page_no())
