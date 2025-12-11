# app/services/latex_parser.py
from typing import Dict

def parse_latex_sections(latex: str) -> Dict[str, str]:
    """
    MVP parser using simple markers:
    %SECTION:summary
       ...
    %ENDSECTION
    """

    sections = {}
    current = None
    buffer = []

    for line in latex.splitlines():
        print(line)
        stripped = line.strip()

        if stripped.startswith("%SECTION:"):
            if current and buffer:
                sections[current] = "\n".join(buffer).strip()
                buffer = []

            current = stripped.split(":", 1)[1].strip()

        elif stripped.startswith("%ENDSECTION"):
            if current and buffer:
                sections[current] = "\n".join(buffer).strip()
                buffer = []
            current = None

        else:
            if current:
                buffer.append(line)

    # Catch last section if missing END
    if current and buffer:
        sections[current] = "\n".join(buffer).strip()

    return sections
