import os, sys
from models import risk_model, genomics_model, nlp_model
from utils.data_loader import load_patient_info_from_interactive, load_text_file
from utils.report_generator import generate_report_interactive
import numpy as np

def ask(prompt, allowed=None, default=None):
    try:
        ans = input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting."); sys.exit(0)
    if ans == "" and default is not None: return default
    if allowed:
        while ans.lower() not in [a.lower() for a in allowed]:
            ans = input(f"Please enter one of {allowed}: ").strip()
    return ans

def run():
    print("=== Early Disease Prediction — Interactive CLI ===\n")
    info = load_patient_info_from_interactive()
    print("\nCollected basic info.")

    # Branching follow-ups
    if info['age'] >= 50 or info['family_history']:
        colon = ask("Because of age/family history:\nHave you done colon screening (yes/no)? ", ["yes","no"], "no")
        info['colon_screening'] = 1 if colon.lower()=="yes" else 0
    else:
        info['colon_screening'] = 0

    # Lifestyle add-ons
    diet = ask("Do you follow a balanced diet (yes/no)? ", ["yes","no"], "yes")
    exercise = ask("Weekly exercise hours [3]: ", None, "3")
    info['diet'] = 1 if diet.lower()=="yes" else 0
    info['exercise_hours'] = float(exercise)

    # DNA input
    dna_score = None
    if ask("\nProvide DNA/VCF/text file or paste sequence? (yes/no) [no]: ", ["yes","no"], "no")=="yes":
        path = ask("Enter file path or paste raw sequence: ")
        seq = None
        if os.path.isfile(path):
            seq = load_text_file(path)
        elif all(ch.upper() in "ATGCUYN-" for ch in path) and len(path)>10:
            seq = path
        if seq:
            print("Running genomic embedding (first run downloads model)...")
            emb = genomics_model.get_dna_embedding(seq)
            dna_score = float(1/(1+np.exp(-(np.linalg.norm(emb)-25)/10)))
            print(f"→ DNA risk: {dna_score:.2f}")

    # Clinical notes input
    notes_score = None
    if ask("\nUpload/paste clinical notes? (yes/no) [no]: ", ["yes","no"], "no")=="yes":
        npath = ask("Enter notes file path or paste notes directly: ")
        text = load_text_file(npath) if os.path.isfile(npath) else npath
        if text:
            print("Analyzing clinical notes...")
            out = nlp_model.analyze_notes(text)
            logits = np.array(out["logits"])[0]
            probs = np.exp(logits)/np.sum(np.exp(logits))
            notes_score = float(probs[1])
            print(f"→ Notes risk: {notes_score:.2f}")

    # Tabular risk
    base_risk = risk_model.predict_risk([info['age'], info['bmi'],
                                         info['smoking'], info['family_history']])
    print(f"\nLifestyle risk: {base_risk:.2f}")

    # Weighted final
    w = {'tabular':0.5, 'dna':0.3, 'notes':0.2}
    total = w['tabular']; final = base_risk*w['tabular']
    if dna_score is not None: final += dna_score*w['dna']; total += w['dna']
    if notes_score is not None: final += notes_score*w['notes']; total += w['notes']
    final /= total
    print(f"\n=== Final combined risk score: {final:.2f} ===\n")

    generate_report_interactive(info, base_risk, dna_score, notes_score, final)
    print("Report saved to reports/Patient_Report_interactive.pdf")

if __name__ == "__main__":
    run()
