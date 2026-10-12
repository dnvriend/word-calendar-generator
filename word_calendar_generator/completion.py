"""Completion command for word-calendar-generator.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import typer
import typer.completion as typer_completion

from word_calendar_generator.app import make_app

completion_app = make_app("Generate shell completion scripts.")


@completion_app.command(name="generate")
def generate_completion(
    shell: typer_completion.Shells = typer.Argument(
        ...,
        help="Shell type (bash, zsh, fish, powershell, pwsh)",
    ),
) -> None:
    """Generate shell completion script.

    Install instructions:

    \b
    # Bash (add to ~/.bashrc):
    eval "$(word-calendar-generator completion generate bash)"

    \b
    # Zsh (add to ~/.zshrc):
    eval "$(word-calendar-generator completion generate zsh)"

    \b
    # Fish (add to ~/.config/fish/completions/word-calendar-generator.fish):
    word-calendar-generator completion generate fish > ~/.config/fish/completions/word-calendar-generator.fish

    \b
    File-based Installation (Recommended for better performance):

    \b
    # Bash
    word-calendar-generator completion generate bash > ~/.word-calendar-generator-complete.bash
    echo 'source ~/.word-calendar-generator-complete.bash' >> ~/.bashrc

    \b
    # Zsh
    word-calendar-generator completion generate zsh > ~/.word-calendar-generator-complete.zsh
    echo 'source ~/.word-calendar-generator-complete.zsh' >> ~/.zshrc

    \b
    Supported Shells: bash, zsh, fish, powershell, pwsh.
    """
    script = typer_completion.get_completion_script(
        prog_name="word-calendar-generator",
        complete_var="_WORD_CALENDAR_GENERATOR_COMPLETE",
        shell=shell.value,  # nosec B604 — shell is a shell-type string, not subprocess shell=True
    )
    typer.echo(script)
