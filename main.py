from utils.report_generator import generate_report_interactive, compute_final_score

# Example (replace with real outputs from models)
info = {"age": 40, "bmi": 26.5, "smoking": 0, "family": 1}
tabular_score = 0.67
dna_score = 0.55
notes_score = {"predicted_class": 1}

# ✅ Compute final score dynamically
final_score = compute_final_score(tabular_score, dna_score, notes_score)

# ✅ Generate PDF
generate_report_interactive(info, tabular_score, dna_score, notes_score, final_score)

