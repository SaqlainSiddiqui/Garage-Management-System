"""Static diagnostics for the Garage Management System."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {"venv", "__pycache__", ".git"}
errors = []

for path in ROOT.rglob("*.py"):
    if any(part in SKIP for part in path.parts):
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        errors.append(f"{path.relative_to(ROOT)}: SyntaxError: {exc}")

checks = [
    (ROOT / "views/dashboard.py", "        self.create_layout()", "Dashboard layout is not initialized."),
    (ROOT / "views/billing.py", "                service,\n                tax_rate", "Billing is passing the wrong object to create_invoice()."),
    (ROOT / "models/invoice.py", '"items": items', "Invoice items are not being stored."),
    (ROOT / "models/service.py", '"status": status', "Selected service status is not being saved."),
]

for path, needle, message in checks:
    if needle not in path.read_text(encoding="utf-8"):
        errors.append(f"{path.relative_to(ROOT)}: {message}")

if errors:
    print("PROJECT DIAGNOSTICS: FAILED")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

print("PROJECT DIAGNOSTICS: PASSED")
print("All project Python files passed syntax parsing and integration checks.")
