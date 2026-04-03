from __future__ import annotations

import typer
from .synth import SigmaSynth

app = typer.Typer(help="Generate Sigma rules from suspicious Windows process events.")


@app.command()
def generate(
    path: str,
    product: str = "windows",
    category: str = "process_creation",
    profile: str = "balanced",
) -> None:
    rule = (
        SigmaSynth()
        .from_json(path)
        .for_logsource(product=product, category=category)
        .generate(profile=profile)
    )
    typer.echo(rule.yaml())


if __name__ == "__main__":
    app()