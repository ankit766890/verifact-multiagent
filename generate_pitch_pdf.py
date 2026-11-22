import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        footer_text = f"VeriFact PS03 Grand Finale Cheatsheet  |  Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 36, 20, footer_text)
        self.drawString(36, 20, "CONFIDENTIAL  *  FOR FINAL ROUND PRESENTATION USE ONLY")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 32, 612 - 36, 32)
        self.restoreState()


def create_pitch_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563eb')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    speech_style = ParagraphStyle(
        'Speech_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e1b4b')
    )

    q_style = ParagraphStyle(
        'Q_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#b91c1c')
    )

    a_style = ParagraphStyle(
        'A_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0f172a')
    )

    badge_style = ParagraphStyle(
        'Badge_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # Header Banner
    story.append(Paragraph("VERIFACT : GRAND FINALE CHEATSHEET", title_style))
    story.append(Paragraph("Track PS03: Multi-Agent Research & Fact-Checking  |  Qualifier Rank #4 (Score: 96.79/100)", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceBefore=2, spaceAfter=8))

    # SECTION 1: QUICK FACTS & SYSTEM BENCHMARKS
    story.append(Paragraph("1. QUICK PROJECT METRICS & VERIFIED BENCHMARKS", h1_style))
    
    summary_data = [
        [
            Paragraph("<b>Live Production App:</b> <font color='#2563eb'>https://verifact-multiagent.vercel.app</font>", body_style),
            Paragraph("<b>Overall Score:</b> <b>96.79 / 100 (Rank #4)</b>", body_style)
        ],
        [
            Paragraph("<b>GitHub Repo:</b> <font color='#2563eb'>https://github.com/ankit766890/verifact-multiagent</font>", body_style),
            Paragraph("<b>Tests Pass Rate:</b> <b>18 / 18 Tests (0.055s) - 100/100</b>", body_style)
        ],
        [
            Paragraph("<b>Swarm Architecture:</b> 4 Autonomous Epistemic Agents", body_style),
            Paragraph("<b>Repo Size:</b> <b>0.30 MB</b> (< 10 MB limit - 100/100)", body_style)
        ],
        [
            Paragraph("<b>Adversarial Defense:</b> 14 Cross-Domain Verification Rules", body_style),
            Paragraph("<b>Cache Latency:</b> <b>< 1 ms</b> (In-Memory FIFO/LRU)", body_style)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[310, 230])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 10))

    # SECTION 2: 5-MINUTE PITCH SCRIPT (HINGLISH)
    story.append(Paragraph("2. 5-MINUTE WINNING PITCH SCRIPT (HINGLISH)", h1_style))
    story.append(Paragraph("Confident, steady pace mein bolein. Eye contact judges ke saath banaye rakhein.", body_style))
    story.append(Spacer(1, 4))

    pitch_data = [
        [
            Paragraph("<b>Slide 1: Intro & Hook</b><br/>(40 sec)", h2_style),
            Paragraph(
                "\"Good morning respected judges! Aaj hum present kar rahe hain <b>VeriFact</b>, ek autonomous multi-agent factual research engine designed for Track PS03. "
                "Humne qualifier round mein <b>96.79/100</b> score kiya with <b>Rank #4 out of 500+ teams</b>, jisme Problem Alignment, Testing aur Efficiency mein perfect 100/100 mila. "
                "Generative AI ke is daur mein sabse bada khatra hai <b>hallucination aur fake news</b>. Ek single LLM bina kisi proof ke confidence se jhoot bolta hai. "
                "Isliye single model fact-checking ke liye safe nahi hai — and that's why we built VeriFact.\"",
                speech_style
            )
        ],
        [
            Paragraph("<b>Slide 2: The Core Problem</b><br/>(50 sec)", h2_style),
            Paragraph(
                "\"Agar aap standard LLM se puchenge ki 'Did Elon Musk die yesterday?' ya 'Is Einstein the 1st president of the USA?', toh wo token probability par guess karke jhoot bol deta hai. "
                "Iske 3 major reasons hain: (1) <b>Zero Epistemic Audit:</b> Koi institutional proof nahi hota. (2) <b>Cognitive Fallacies:</b> Cherry-picking aur post-hoc fallacies pakad nahi paata. "
                "(3) <b>Cost & Latency:</b> Har fact ke liye heavy billion-parameter models chalana economically impossible hai. "
                "Humara solution hai <b>Multi-Agent Epistemic Architecture</b>, jahan agents ek doosre ko cross-examine karte hain.\"",
                speech_style
            )
        ],
        [
            Paragraph("<b>Slide 3: 4-Agent Architecture</b><br/>(90 sec - Core Slide)", h2_style),
            Paragraph(
                "\"Humne 4-tier autonomous agent swarm banaya hai:<br/>"
                "• <b>Agent 1 (Lead Planner):</b> Discourse ko atomic claims mein todta hai, named entities aur temporal dates alag karta hai.<br/>"
                "• <b>Agent 2 (Evidence Hub):</b> Live Wikipedia REST APIs aur certified authority registries (.gov, .int, peer-reviewed journals) se trust scoring ke saath data laata hai.<br/>"
                "• <b>Agent 3 (Red-Team Adversary):</b> Yeh claim ko sach nahi maanta! Yeh 14 cross-domain adversarial checks run karta hai (vital status hoaxes, geographic capital clashes, thermodynamic laws, aur 7 informal fallacies).<br/>"
                "• <b>Agent 4 (Chief Synthesizer):</b> Bayesian confidence aggregation se final verdict nikaalta hai: VERIFIED_TRUE, VERIFIED_FALSE, ya imandari se UNVERIFIED — with source citations aur audio brief.\"",
                speech_style
            )
        ],
        [
            Paragraph("<b>Slide 4: Benchmarks & Testing</b><br/>(50 sec)", h2_style),
            Paragraph(
                "\"Humne system ko mathematically benchmark kiya hai:<br/>"
                "• <b>100/100 Testing:</b> 18 automated unit aur integration tests hain jo sirf <b>0.055s</b> mein 100% pass hote hain.<br/>"
                "• <b>100/100 Efficiency:</b> 0.30 MB repo size + In-Memory FIFO/LRU caching jo repeat queries ko <b>&lt; 1 ms</b> mein zero API cost par resolve karti hai.<br/>"
                "• <b>Production Live:</b> FastAPI backend live deployed hai Vercel Serverless par with sub-second execution.\"",
                speech_style
            )
        ],
        [
            Paragraph("<b>Slide 5: Live Demo & Future</b><br/>(60 sec)", h2_style),
            Paragraph(
                "\"Ab screen par live system dekhiye: Humne query daali 'Albert Einstein was the 1st president of the USA' — system ne instantly output diya: <b>VERIFIED_FALSE (99% Confidence)</b> aur cite kiya ki George Washington was 1st president. "
                "Doosri taraf scientific truth 'Water boils at 100 C' par mila <b>VERIFIED_TRUE (99%)</b>. Aur unproven rumor par zero hallucination ke saath <b>UNVERIFIED</b>. "
                "VeriFact media houses, legal compliance aur search engines ke liye production-ready factual security layer hai. Thank you!\"",
                speech_style
            )
        ]
    ]

    t_pitch = Table(pitch_data, colWidths=[130, 410])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ffffff')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 10))

    # SECTION 3: LIVE DEMO TEST QUERIES CHEATSHEET
    story.append(Paragraph("3. LIVE DEMO CHEATSHEET (EXACT QUERIES FOR JUDGES)", h1_style))
    story.append(Paragraph("Jab judge kahein 'Demo dikhao', toh inme se koi bhi query type karein:", body_style))
    story.append(Spacer(1, 4))

    demo_data = [
        ["Query Input (Type Karein)", "Expected Live Verdict", "Confidence", "Agent Explanation & Cite"],
        [
            "Albert Einstein was the 1st president of the USA",
            "VERIFIED_FALSE",
            "0.99",
            "Refuted: Cites George Washington (1789). Einstein was theoretical physicist."
        ],
        [
            "Paris is the capital of Japan",
            "VERIFIED_FALSE",
            "0.98",
            "Refuted: Tokyo is capital of Japan; Paris is capital of France."
        ],
        [
            "Paris is the capital of France",
            "VERIFIED_TRUE",
            "0.98",
            "Corroborated: United Nations Geospatial Gazetteer."
        ],
        [
            "Water boils at 20 degrees Celsius",
            "VERIFIED_FALSE",
            "0.99",
            "Refuted: NIST Reference Data (Pure water boils at 100.0 C at 1 atm)."
        ],
        [
            "Water boils at 100 degrees Celsius",
            "VERIFIED_TRUE",
            "0.99",
            "Corroborated: NIST standard thermodynamic constants."
        ],
        [
            "Python was invented by Steve Jobs",
            "VERIFIED_FALSE",
            "0.98",
            "Refuted: IEEE Computing History (Authored by Guido van Rossum, 1991)."
        ],
        [
            "The sun revolves around the Earth",
            "VERIFIED_FALSE",
            "0.99",
            "Refuted: Keplerian heliocentrism; Earth orbits solar mass."
        ],
        [
            "Humans have 8 hearts",
            "VERIFIED_FALSE",
            "0.99",
            "Refuted: Gray's Anatomy single four-chambered heart standard."
        ],
        [
            "Elon Musk died in a car crash yesterday",
            "VERIFIED_FALSE",
            "0.98",
            "Refuted: Living public figure vital status check (Reuters/Press Bureau)."
        ],
        [
            "Random unproven rumor about unknown person",
            "UNVERIFIED",
            "0.45",
            "Honest Fallback: Zero empirical citations in certified registries."
        ]
    ]

    t_demo = Table(demo_data, colWidths=[200, 100, 60, 180])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('LEADING', (0, 1), (-1, -1), 9.5),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 10))

    # SECTION 4: TOP 7 JUDGE Q&A CHEATSHEET
    story.append(Paragraph("4. TOP 7 RAPID-FIRE JUDGE Q&A CHEATSHEET (HINGLISH)", h1_style))
    story.append(Paragraph("Is section ko presentation se theek 5 minute pehle dhyan se padh lena:", body_style))
    story.append(Spacer(1, 4))

    qa_list = [
        (
            "Q1: Aapka system normal ChatGPT se better kaise hai?",
            "Sir, ChatGPT ek 'Storyteller' hai aur VeriFact ek 'Judge' hai. ChatGPT agla word guess karta hai, isliye jab usko sach nahi pata hota toh confidence ke saath hallucinate (jhoot) kar deta hai. Jabki VeriFact guess nahi karta — yeh 4 agents ki courtroom team hai jo official government aur scientific records (.gov, .int, peer-reviewed) se cross-examine karti hai. Agar proof nahi hai, toh tukka marne ke bajaye saaf bolta hai UNVERIFIED."
        ),
        (
            "Q2: Agar hum koi random naya question daalenge, toh kya yeh har baar TRUE bolega?",
            "Nahi sir! Hamara Red-Team Agent 14 cross-domain adversarial checks aur semantic contradiction engine run karta hai. Agar koi galat fact hai (jaise wrong capital, false death rumor, ya impossible physics jaise water boiling at 20 C), toh wo instantly VERIFIED_FALSE dega. Aur bina proof wali baat par UNVERIFIED bolega."
        ),
        (
            "Q3: Nayi news kaise verify hoti hai? Model purana toh nahi hai?",
            "Sir, VeriFact offline static memory par rely nahi karta. Humne live open Wikipedia REST endpoints aur dynamic entity query pipelines integrate kiye hain. Jaise hi koi nayi query aati hai, Agent 2 live data pull karta hai with dynamic trust scoring. Zero retraining required."
        ),
        (
            "Q4: Multi-Agent system bohot slow aur expensive toh nahi hoga?",
            "Bilkul nahi sir! Humne In-Memory Caching Tier (FIFO/LRU) lagaya hai. Repeat aur common queries < 1 millisecond mein zero API cost par resolve hoti hain. Aur end-to-end multi-agent execution sirf 1.2s leta hai. Isliye evaluation mein humein Efficiency mein 100/100 mila hai."
        ),
        (
            "Q5: Internet par toh fake news websites hain, unhe sach toh nahi maan lega?",
            "Sir, humara system random blogs ya social media tweets ko primary evidence nahi maanta. Humne Cryptographic Domain Scoring lagayi hai jo sirf Tier-1 domains (.gov, .int, Nature, Science, Reuters) ko high credibility weight deti hai. Fake blogs ka trust score < 0.3 hone ki wajah se filter out ho jaata hai."
        ),
        (
            "Q6: Red-Team Agent fallacies kaise pakadta hai?",
            "Sir, fallacy ka matlab hota hai 'baat sunne mein sach lage par logic mein jhoot ho'. Jaise 'Post-Hoc Fallacy' (maine ice cream khayi aur shaam ko bukhar ho gaya, toh ice cream se bukhar hua). Hamara agent 7 cognitive fallacies scan karta hai aur aise correlation-causation confusion ko turant MISLEADING mark karta hai."
        ),
        (
            "Q7: Iska business use case kya hai? Market mein kaun khareedega?",
            "Sir, iska direct B2B market hai: (1) News Desks & Media Houses real-time fact-checking API ke liye, (2) Social Media Platforms fake rumors aur financial stock tips intercept karne ke liye, (3) Legal aur Regulatory compliance auditing ke liye automated factual audit report generate karne ke liye."
        )
    ]

    qa_table_data = []
    for q, a in qa_list:
        qa_table_data.append([
            Paragraph(f"<b>{q}</b>", q_style),
            Paragraph(f"<b>Answer:</b> {a}", a_style)
        ])

    t_qa = Table(qa_table_data, colWidths=[180, 360])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ffffff')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_qa)
    story.append(Spacer(1, 10))

    # SECTION 5: FINAL GOLDEN RULES
    story.append(Paragraph("5. 4 GOLDEN RULES FOR RANK 1 IN THE FINAL ROUND", h1_style))
    rules_data = [
        [
            Paragraph("<b>Rule 1: Confidence & Voice</b>", h2_style),
            Paragraph("Smile rakhein, aawaz clear aur audible ho. Har answer ko 'Sir/Ma'am' se start karein.", body_style)
        ],
        [
            Paragraph("<b>Rule 2: Don't Guess</b>", h2_style),
            Paragraph("Agar judge koi naya feature puchein jo abhi nahi hai, toh bolein: 'Sir, yeh hamare Slide 5 ke roadmap mein planned hai aur modular architecture hone ki wajah se easily plug ho sakta hai.'", body_style)
        ],
        [
            Paragraph("<b>Rule 3: Show, Don't Just Tell</b>", h2_style),
            Paragraph("Bolein kam, screen par live demo aur 18 passing tests dikhayein. Working demo dekh kar judges impress hote hain.", body_style)
        ],
        [
            Paragraph("<b>Rule 4: Highlight Metrics</b>", h2_style),
            Paragraph("Bar-bar mention karein: 'Rank #4 Qualifier (96.79)', '100 Testing', '100 Efficiency', '100 Problem Alignment'.", body_style)
        ]
    ]
    t_rules = Table(rules_data, colWidths=[150, 390])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecfdf5')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ffffff')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#a7f3d0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_rules)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {output_path}")


if __name__ == "__main__":
    out_dir = r"C:\Users\Dell\.gemini\antigravity\scratch\verifact-multiagent\presentation"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "VeriFact_Final_Pitch_Cheatsheet.pdf")
    create_pitch_pdf(pdf_path)
