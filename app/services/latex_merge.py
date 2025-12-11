# app/services/latex_merge.py
from typing import Dict

def merge_sections_into_latex(original: str, updates: Dict[str, str]) -> str:
    """
    Replace content between %SECTION:name ... %ENDSECTION
    with tailored_sections[name].
    """
    lines = original.splitlines()
    out = []
    skipping = False
    current = None

    for line in lines:
        stripped = line.strip()

        # Start section
        if stripped.startswith("%SECTION:"):
            current = stripped.split(":", 1)[1].strip()
            out.append(line)

            # Insert tailored content
            if current in updates:
                out.append(updates[current])

            skipping = True
            continue

        # End section
        if stripped.startswith("%ENDSECTION"):
            skipping = False
            out.append(line)
            current = None
            continue

        if not skipping:
            out.append(line)

    return "\n".join(out)
