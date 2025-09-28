from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os, datetime

def compute_final_score(tabular_score, dna_score=None, notes_score=None):
    scores, weights = [], []
    if tabular_score is not None:
        scores.append(tabular_score); weights.append(0.4)
    if dna_score is not None:
        scores.append(dna_score); weights.append(0.4)
    if notes_score is not None:
        if isinstance(notes_score, dict) and "predicted_class" in notes_score:
            score_val = 0.7 if notes_score["predicted_class"] == 1 else 0.3
        else:
            score_val = float(notes_score)
        scores.append(score_val); weights.append(0.2)
    return sum(s * w for s, w in zip(scores, weights)) / sum(weights) if scores else 0.0

def generate_report_interactive(info, tabular_score, dna_score, notes_score,
                                final_score,
                                out_path="reports/Patient_Report_interactive.pdf"):
    styles = getSampleStyleSheet()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(out_path)
    story = []
    story.append(Paragraph("Early Disease Prediction — Interactive Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().isoformat()}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Patient Details:", styles["Heading2"]))
    for k, v in info.items():
        story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Model Outputs:", styles["Heading2"]))
    story.append(Paragraph(f"Lifestyle/Family risk: {tabular_score:.2f}", styles["Normal"]))
    story.append(Paragraph(f"DNA risk: {dna_score if dna_score is not None else 'Not provided'}", styles["Normal"]))
    story.append(Paragraph(f"Clinical Notes risk: {notes_score if notes_score is not None else 'Not provided'}", styles["Normal"]))
    story.append(Paragraph(f"Final combined risk: {final_score:.2f}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Recommendations:", styles["Heading2"]))
    if final_score >= 0.6:
        story.append(Paragraph("High risk detected — follow up with a healthcare professional.", styles["Normal"]))
    elif final_score >= 0.35:
        story.append(Paragraph("Moderate risk — consider targeted tests and lifestyle improvements.", styles["Normal"]))
    else:
        story.append(Paragraph("Low risk — maintain healthy lifestyle and regular checkups.", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Why this recommendation?", styles["Heading2"]))
    reasons = []
    if tabular_score is not None and tabular_score >= 0.6:
        reasons.append("Lifestyle/Family history shows elevated risk factors.")
    if dna_score is not None and dna_score >= 0.6:
        reasons.append("Genetic markers indicate possible predisposition.")
    if notes_score is not None:
        if isinstance(notes_score, dict) and notes_score.get("predicted_class") == 1:
            reasons.append("Clinical notes analysis detected disease-related signals.")
    if not reasons:
        reasons.append("No major individual risk factor detected — overall risk comes from combined signals.")
    
    for r in reasons:
        story.append(Paragraph(f"- {r}", styles["Normal"]))

    doc.build(story)
    print(f"Report saved to {out_path}")
