"""
Generates the required 6-Scene Storyboard PDF (Storyboard_Derivative.pdf)
matching Section 3 of the M3 Internal Assessment instructions.
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config import (
    CONCEPT_AREA,
    COURSE_NAME,
    LEARNING_OBJECTIVE,
    STUDENT_ID,
    STUDENT_NAME,
    VIDEO_SUBTITLE,
    VIDEO_TITLE,
)


def build_storyboard_pdf(out_pdf: Path):
    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.3 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "MetaCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8,
    )
    obj_style = ParagraphStyle(
        "ObjCustom",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#E0F2FE"),
        borderPadding=8,
        spaceAfter=12,
    )
    cell_style = ParagraphStyle(
        "CellCustom",
        parent=styles["Normal"],
        fontSize=9.2,
        leading=12.5,
        textColor=colors.HexColor("#0F172A"),
    )
    header_style = ParagraphStyle(
        "HeaderCustom",
        parent=styles["Normal"],
        fontSize=9.8,
        leading=12,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )

    story = []
    story.append(Paragraph(f"{COURSE_NAME} — 6-Scene Storyboard", title_style))
    story.append(
        Paragraph(
            f"<b>Topic:</b> {VIDEO_TITLE}: {VIDEO_SUBTITLE} &nbsp;|&nbsp; "
            f"<b>Concept Area:</b> {CONCEPT_AREA}<br/>"
            f"<b>Student Name:</b> {STUDENT_NAME} &nbsp;|&nbsp; "
            f"<b>Student ID:</b> {STUDENT_ID}",
            meta_style,
        )
    )
    story.append(Paragraph(f"<b>One-Sentence Learning Objective:</b> {LEARNING_OBJECTIVE}", obj_style))

    rows = [
        [
            Paragraph("Scene", header_style),
            Paragraph("Purpose", header_style),
            Paragraph("Visual, Narration &amp; Math Plan", header_style),
        ],
        [
            Paragraph("<b>1. Hook / Context</b><br/>(~35 sec)", cell_style),
            Paragraph("Spark curiosity and motivate why instantaneous rate of change is needed.", cell_style),
            Paragraph(
                "<b>Visual:</b> Animated car moving along a road with s(t) = t<super>2</super> meters; "
                "side-by-side cards comparing average speed over [2, 4] vs. speedometer at t = 2s.<br/>"
                "<b>Math &amp; Narration:</b> Average speed = (16 - 4)/(4 - 2) = 6 m/s. "
                "Ask: what happens if Δt = 0? We get 0/0, motivating limits.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>2. Concept Introduction</b><br/>(~45 sec)", cell_style),
            Paragraph("Define notation, learning objective, secant slope, and the derivative.", cell_style),
            Paragraph(
                "<b>Visual:</b> Learning objective banner + two side-by-side definition cards.<br/>"
                "<b>Math &amp; Narration:</b> Define starting input x and step h ≠ 0. "
                "Secant slope m_sec = [f(x+h) - f(x)] / h. "
                "Derivative f'(x) = lim(h→0) [f(x+h) - f(x)] / h.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>3. Visual Intuition</b><br/>(~55 sec)", cell_style),
            Paragraph("Build geometric intuition before algebraic manipulation.", cell_style),
            Paragraph(
                "<b>Visual:</b> Plot of f(x) = x<super>2</super> with fixed P(2, 4) and moving Q(2+h, (2+h)<super>2</super>), "
                "rise/run triangle, and live slope readout panel.<br/>"
                "<b>Math &amp; Narration:</b> Animate h shrinking 2.0 → 1.0 → 0.5 → 0.1 → 0.002; "
                "amber secant line rotates smoothly onto the emerald tangent line.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>4. Worked Example</b><br/>(~55 sec)", cell_style),
            Paragraph("Demonstrate why and how the algebra produces the exact limit.", cell_style),
            Paragraph(
                "<b>Visual:</b> Split-screen: numerical table (h = 2, 1, 0.5, 0.1, 0.01 → slopes 6, 5, 4.5, 4.1, 4.01) "
                "and step-by-step algebraic derivation.<br/>"
                "<b>Math &amp; Narration:</b> Expand (2+h)<super>2</super> - 4 = 4h + h<super>2</super>, "
                "factor h(4+h)/h, cancel h (since h ≠ 0), take lim(h→0)(4+h) = 4.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>5. Interpretation</b><br/>(~35 sec)", cell_style),
            Paragraph("Connect the algebraic result f'(2) = 4 back to geometry and physics.", cell_style),
            Paragraph(
                "<b>Visual:</b> Progressive zoom-in (1x to 6.5x) around P(2, 4) showing local linearity "
                "with tangent line y = 4x - 4.<br/>"
                "<b>Math &amp; Narration:</b> Explain tangent equation y - 4 = 4(x - 2) and connect "
                "back to the car's speedometer reading 4 m/s at t = 2s.",
                cell_style,
            ),
        ],
        [
            Paragraph("<b>6. Summary &amp; Credits</b><br/>(~25 sec)", cell_style),
            Paragraph("Reinforce 3 core takeaways and disclose references &amp; AI tools.", cell_style),
            Paragraph(
                "<b>Visual:</b> Three takeaway cards + Credits &amp; AI Disclosure card.<br/>"
                "<b>Narration:</b> Recap secant slope, shrinking h→0, and simplifying before taking the limit; "
                "cite M3 notes, Stewart Calculus, and AI scripting/TTS disclosure.",
                cell_style,
            ),
        ],
    ]

    table = Table(rows, colWidths=[4.2 * cm, 6.3 * cm, 16.0 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    print(f"Storyboard PDF saved to: {out_pdf}")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "Storyboard_Derivative.pdf"
    build_storyboard_pdf(out)
