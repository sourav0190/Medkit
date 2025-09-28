import json

def load_patient_info(path="inputs/patient_info.json"):
    with open(path, "r") as f:
        return json.load(f)

def load_dna_sequence(path="inputs/dna_sequence.txt"):
    with open(path, "r") as f:
        return f.read().strip()

def load_clinical_notes(path="inputs/clinical_notes.txt"):
    with open(path, "r") as f:
        return f.read().strip()
def load_patient_info_from_interactive():
    print("Enter patient details (press Enter for default).")
    age = input("Age [40]: ").strip(); age = int(age) if age else 40
    bmi = input("BMI [26.5]: ").strip(); bmi = float(bmi) if bmi else 26.5
    smoking = input("Smoking? (yes/no) [no]: ").strip().lower()
    smoking = 1 if smoking in ("yes","y","1") else 0
    family = input("Family history of major disease? (yes/no) [yes]: ").strip().lower()
    family = 1 if family in ("yes","y","1") else 0
    return {"age": age, "bmi": bmi, "smoking": smoking, "family_history": family}
def load_text_file(path):
    """Read a UTF-8 text file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()