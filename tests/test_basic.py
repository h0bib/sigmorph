from sigmorph import SigmaSynth


def test_generate_rule():
    events = [
        {
            "Image": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "CommandLine": "powershell.exe -enc aaa",
            "ParentImage": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "EventID": 1,
        },
        {
            "Image": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "CommandLine": "powershell.exe -EncodedCommand bbb",
            "ParentImage": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "EventID": 1,
        },
    ]

    rule = (
        SigmaSynth()
        .from_events(events)
        .for_logsource(product="windows", category="process_creation")
        .generate(profile="balanced")
    )

    text = rule.yaml().lower()
    assert "powershell.exe" in text
    assert "commandline|contains" in text
    assert "parentimage|endswith" in text
    assert "user" not in text