# sigmorph

> Built by YAHIAOUI Hadj Habib (chaos.hh@gmail.com)

**sigmorph** is a Python library that generates **explainable Sigma detection rules** from suspicious Windows process events.

It is designed for detection engineers and analysts who want to quickly turn observed suspicious behavior into reusable detection rules.

---

## What it does

Given a set of suspicious events, sigmorph:

- extracts relevant fields
- measures field stability across samples
- removes noisy or environment-specific data
- generalizes patterns into Sigma-compatible conditions
- generates a Sigma rule
- provides:
  - rule scoring
  - explanation of decisions
  - anti-overfitting analysis

---

## Scope (v0.1)

This version is intentionally focused:

- Input: JSON events
- Target: Windows process creation logs
- Output: Sigma rule (YAML)
- No machine learning
- No external dependencies on SIEMs

---

## Example input

```json
[
  {
    "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "CommandLine": "powershell.exe -enc aGVsbG8=",
    "ParentImage": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "User": "LAB\\bob",
    "ComputerName": "WS-22",
    "EventID": 1
  },
  {
    "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "CommandLine": "powershell.exe -EncodedCommand ZGly",
    "ParentImage": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "User": "LAB\\alice",
    "ComputerName": "WS-30",
    "EventID": 1
  }
]

## Example output
</> YAML
title: Auto-generated suspicious process pattern
logsource:
  product: windows
  category: process_creation
detection:
  selection_1:
    Image|endswith: \powershell.exe
  selection_2:
    CommandLine|contains:
      - -enc
      - EncodedCommand
      - powershell
  selection_3:
    ParentImage|endswith: \winword.exe
  condition: selection_1 and selection_2 and selection_3
level: medium
metadata:
  status: experimental
  profile: balanced
  selected_fields:
    - Image
    - CommandLine
    - ParentImage
	
## Installation and Usage

</> Bash

pip install -e .
python -m sigmorph.cli examples/suspicious_powershell.json

</> Python

from sigmorph import SigmaSynth

rule = (
    SigmaSynth()
    .from_json("examples/suspicious_powershell.json")
    .for_logsource(product="windows", category="process_creation")
    .generate(profile="balanced")
)

print(rule.yaml())
print(rule.score())
print(rule.explain())
print(rule.overfit_report())

## Profiles

strict → high precision, low noise
balanced → default, best trade-off
broad → more coverage, more noise

## Core concepts

Field stability: evaluates how consistent a field is across events
Generalization: converts raw values into reusable Sigma conditions (contains, endswith, exact)
Noise reduction: removes environment-specific fields like usernames and hostnames
Overfit awareness: detects overly specific rules


## Author

YAHIAOUI Hadj Habib
GitHub: https://github.com/h0bib

Email: chaos.hh@gmail.com