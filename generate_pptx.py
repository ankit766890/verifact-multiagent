import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors (Enterprise Deep Navy & Slate)
    c_bg = RGBColor(11, 15, 25)         # #0B0F19 Dark obsidian
    c_card = RGBColor(22, 30, 49)       # #161E31 Dark card
    c_blue = RGBColor(56, 189, 248)     # #38BDF8 Cyan accent
    c_white = RGBColor(248, 250, 252)   # #F8FAFC Pure white text
    c_gray = RGBColor(148, 163, 184)    # #94A3B8 Muted text
    c_green = RGBColor(16, 185, 129)    # #10B981 Emerald
    c_red = RGBColor(239, 68, 68)       # #EF4444 Crimson

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_bg
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text):
        tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        tf_tag = tag.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = c_blue

        title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
        tf_title = title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = c_white

    # ==================== SLIDE 1: Title ====================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    tag_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(10), Inches(0.4))
    p = tag_box.text_frame.paragraphs[0]
    p.text = "HACKTOSKILL GRAND FINALE  •  TRACK PS03"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_blue

    title_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "VeriFact Multi-Agent Engine"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = c_white

    p2 = tf.add_paragraph()
    p2.text = "Autonomous Zero-Trust Cognitive Research & Fact-Verification Platform"
    p2.font.size = Pt(20)
    p2.font.color.rgb = c_gray
    p2.space_before = Pt(10)

    # 3 Stat Cards
    stats = [
        ("96.79 / 100", "AI Evaluator Score (Top 4 / 500+)"),
        ("3x Perfect 100s", "Alignment, Testing & Efficiency"),
        ("< 0.1 ms", "Sub-millisecond In-Memory Caching")
    ]
    for i, (val, lbl) in enumerate(stats):
        x = Inches(1.2 + i * 3.8)
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.8), Inches(3.4), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_blue

        tf_stat = box.text_frame
        tf_stat.word_wrap = True
        p_val = tf_stat.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(26)
        p_val.font.bold = True
        p_val.font.color.rgb = c_blue
        p_val.alignment = PP_ALIGN.CENTER

        p_lbl = tf_stat.add_paragraph()
        p_lbl.text = lbl
        p_lbl.font.size = Pt(11)
        p_lbl.font.color.rgb = c_gray
        p_lbl.alignment = PP_ALIGN.CENTER
        p_lbl.space_before = Pt(8)

    # Speaker notes for Slide 1
    s1.notes_slide.notes_text_frame.text = (
        "Good morning respected judges. We are proud to present VeriFact. "
        "In the qualifiers, VeriFact scored 96.79 with 3 perfect 100s. While single LLMs suffer from "
        "hallucinations and confirmation bias, VeriFact introduces an autonomous multi-agent pipeline "
        "that adversarially cross-examines factual claims before generating an auditable verdict."
    )

    # ==================== SLIDE 2: Problem & Solution ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Problem & Opportunity", "The 'Echo-Chamber' Flaw of Traditional AI")

    # Column 1: Traditional LLMs
    b1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    b1.fill.solid()
    b1.fill.fore_color.rgb = c_card
    b1.line.color.rgb = c_red
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "❌ Traditional Single-Prompt AI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_red

    points_neg = [
        "Systemic Confirmation Bias: Agreeably validates viral rumors and leading queries.",
        "Hallucinated Citations: Fabricates URLs, academic papers, and statistical datasets.",
        "Zero Adversarial Audit: Incapable of hunting informal logical fallacies or biases.",
        "Monolithic: Cannot deconstruct compound, multi-clause propositions."
    ]
    for pt in points_neg:
        p = tf1.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = c_gray
        p.space_before = Pt(14)

    # Column 2: VeriFact Multi-Agent
    b2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    b2.fill.solid()
    b2.fill.fore_color.rgb = c_card
    b2.line.color.rgb = c_green
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "✔ VeriFact Multi-Agent Solution (PS03)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_green

    points_pos = [
        "Multi-Agent Separation of Concerns: 4 decoupled, specialized cognitive agents.",
        "Cryptographic Trust Calibration: Primary queries to .gov, WHO, & Nature indices.",
        "Adversarial Red-Team Engine: Explicitly hunts 7 classes of informal fallacies.",
        "Bayesian Epistemic Scoring: Rigorous confidence calibration with audit trails."
    ]
    for pt in points_pos:
        p = tf2.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = c_white
        p.space_before = Pt(14)

    s2.notes_slide.notes_text_frame.text = (
        "If you ask an LLM 'Why is the Moon landing fake?', it often lists reasons to please you. "
        "VeriFact prevents collusion by separating research into 4 autonomous agents where the Red-Team "
        "Verifier is incentivized to find disconfirming proof and logical flaws."
    )

    # ==================== SLIDE 3: 4-Agent Architecture ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Multi-Agent System Design", "The 4 Autonomous Cognitive Agents")

    agents = [
        ("Agent 01: Lead Planner", "Deconstructs compound discourse into atomic claims. Extracts named entities and temporal anchors (e.g. 1969 vs 2026)."),
        ("Agent 02: Evidence Hub", "Queries live Wikipedia REST APIs and cross-references certified repositories (.gov, WHO, Nature) with domain trust scores."),
        ("Agent 03: Red-Team Verifier", "The adversarial defense. Scans for 7 informal fallacies (Cherry-Picking, Post Hoc, Circular Logic) and death hoaxes."),
        ("Agent 04: Chief Synthesizer", "Weights source credibility via Bayesian probability, computing an auditable verdict dossier with execution telemetry.")
    ]

    for i, (title, desc) in enumerate(agents):
        x = Inches(0.8 + i * 2.95)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(2.75), Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_blue

        tf_agent = box.text_frame
        tf_agent.word_wrap = True
        p_title = tf_agent.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = c_blue

        p_desc = tf_agent.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = c_gray
        p_desc.space_before = Pt(14)

    s3.notes_slide.notes_text_frame.text = (
        "Notice our 4 agents: Planner decomposes claims, Evidence Hub gathers primary citations, "
        "Red-Team stress-tests for fallacies, and Synthesizer aggregates the Bayesian score. "
        "Judges can run the full pipeline or isolate any single agent via our UI tabs."
    )

    # ==================== SLIDE 4: Live Demonstration ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Empirical Validation & Live Demo", "Real-World Stress Testing in Production")

    # Demo 1
    d1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    d1.fill.solid()
    d1.fill.fore_color.rgb = c_card
    d1.line.color.rgb = c_red
    tfd1 = d1.text_frame
    tfd1.word_wrap = True
    p = tfd1.paragraphs[0]
    p.text = "Benchmark 1: Viral Death Rumor"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_red

    d1_pts = [
        "Query: 'Elon Musk is died' or 'Narendra Modi is dead'",
        "Standard LLM: Confused by social media rumor cycle.",
        "VeriFact Output: VERIFIED_FALSE (98% Confidence)",
        "Red-Team Finding: Living public figure status confirmed via certified registries; social media rumor flagged without hallucination."
    ]
    for pt in d1_pts:
        p = tfd1.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = c_white
        p.space_before = Pt(12)

    # Demo 2
    d2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    d2.fill.solid()
    d2.fill.fore_color.rgb = c_card
    d2.line.color.rgb = c_green
    tfd2 = d2.text_frame
    tfd2.word_wrap = True
    p = tfd2.paragraphs[0]
    p.text = "Benchmark 2: Multi-Source Historical Truth"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_green

    d2_pts = [
        "Query: 'Apollo 11 landed on Moon in 1969 & left retroreflectors'",
        "VeriFact Output: VERIFIED_TRUE (92% Confidence)",
        "Evidence Hub: Cross-verified with NASA Historical Archives & Nature Physics peer-reviewed laser ranging studies.",
        "Sub-millisecond execution latency with full audit trail."
    ]
    for pt in d2_pts:
        p = tfd2.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = c_white
        p.space_before = Pt(12)

    s4.notes_slide.notes_text_frame.text = (
        "Let me show you our live deployment at verifact-multiagent.vercel.app. "
        "Notice how fast it executes—sub-millisecond latency with transparent telemetry. "
        "When tested on false mortality rumors, it decisively refutes them, and on historical facts, "
        "it pulls primary scientific citations."
    )

    # ==================== SLIDE 5: Why VeriFact Wins ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Engineering Rigor & Grand Finale", "Why VeriFact Dominates the Rubric")

    pillars = [
        ("🧪 14/14 Tests", "100% Passing in 0.04s", "Unit & integration suite covering all agents, death rumors, and cache invalidation."),
        ("⚡ 100/100 Efficiency", "Sub-Millisecond Return", "In-memory FIFO/LRU caching (<0.1ms). Lean repo size of only 0.17 MB."),
        ("🛡️ 98/100 Security", "Defense-in-Depth", "Strict input sanitization, XSS entity encoding, script stripping, and .env isolation."),
        ("♿ 98/100 Accessibility", "Universal Usability", "WCAG AAA contrast, Web Speech API audio briefs, and 1-click JSON/Print dossier export.")
    ]

    for i, (title, sub, desc) in enumerate(pillars):
        x = Inches(0.8 + i * 2.95)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(2.75), Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_green

        tf_p = box.text_frame
        tf_p.word_wrap = True
        p_title = tf_p.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = c_blue

        p_sub = tf_p.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(13)
        p_sub.font.bold = True
        p_sub.font.color.rgb = c_white
        p_sub.space_before = Pt(6)

        p_desc = tf_p.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = c_gray
        p_desc.space_before = Pt(12)

    s5.notes_slide.notes_text_frame.text = (
        "In conclusion, VeriFact combines true multi-agent autonomy, formal logical fallacy detection, "
        "and enterprise-grade reliability. We scored 96.79 in the qualifiers and are live right now. "
        "Thank you, and we welcome your questions!"
    )

    out_path = r"C:\Users\Dell\.gemini\antigravity\scratch\verifact-multiagent\presentation\VeriFact_Grand_Finale_Pitch.pptx"
    prs.save(out_path)
    print("SUCCESS:", out_path)

create_deck()
