#! /usr/bin/env python

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log
from textual.containers import Container
from textual.reactive import reactive
from subprocess import Popen, PIPE
import threading


MENU_OPTIONS = {
    "1": ("Start the Bedrock full stack & Magma microservices",
          "docker compose up"),
    "2": ("Stop the entire stack",
          "docker compose down"),
    "3": ("Delete the entire logical DB and all data",
          "rm -rf -v dbvolume/data/"),
    "4": ("Rebuild the Bedrock FastAPI container with current Magma code",
          "docker rmi bedrock-bedrock && docker compose build bedrock"),
    "5": ("Run unit tests",
          "cd bedrock && pytest --cov=app --cov-report=term --cov-report=html --verbose tests/ && cd .."),
    "6": ("Reinstall the FastAPI microservices module 'magma' locally",
          "pip uninstall -y magma && cd bedrock && pip install . && cd .."),
    "7": ("Git status",
          "git status"),
    "8": ("Exit menu only (stack up/down state will not change)", None),
}  # NOTE: Update the # of the exit key in on_key() below. Exit # is hardcoded there.


class DevMenu(App):
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Quit")]
    selected = reactive("1")


    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Log(id="log_area", highlight=True, max_lines=1000, auto_scroll=True)
            yield Static(self.render_menu(), id="menu")
        yield Footer()


    def render_menu(self) -> str:
        return "\n".join(
            # TODO: NOTE! The styling codes are working in the lower/menu window, just not in the upper/log window.
            f"[bold magenta]{key}.[/bold magenta] {desc}" +
            (" [green](selected)[/green]" if key == self.selected else "")
            for key, (desc, _) in MENU_OPTIONS.items()
        )


    def on_mount(self):
        # TODO: Styling codes are not working in the upper/log window (only in the lower/menu window)
        # self.query_one(Log).write_line("[bold yellow]Welcome to the Bedrock Developer Menu![/bold yellow]")
        self.query_one(Log).write_line("================  Bedrock Developer Menu ================")


    def action_quit(self):
        self.exit()


    def on_key(self, event):
        key = event.key
        if key in MENU_OPTIONS:
            self.selected = key
            self.refresh_menu()
            desc, cmd = MENU_OPTIONS[key]
            if key == "8":
                self.exit()
            else:
                self.run_command(desc, cmd)


    def refresh_menu(self):
        self.query_one(Static).update(self.render_menu())


    def stream_output(self, pipe, log, prefix=""):
        for line in iter(pipe.readline, b""):
            log.write_line(f"{prefix}{line.decode(errors='ignore').rstrip()}")
        pipe.close()


    def run_command(self, description, command):
        log = self.query_one(Log)
        log.write_line(f"\n")
        # log.write_line(f"[yellow]>> {description}[/yellow]")  # TODO: Styling codes not currently working in upp/log window.
        # log.write_line(f">> {description}")
        log.write_line(f"$ {command}")
        log.write_line(f"\n")

        try:
            process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, bufsize=1)

            # Use threads to stream stdout and stderr
            threading.Thread(target=self.stream_output, args=(process.stdout, log), daemon=True).start()
            threading.Thread(target=self.stream_output, args=(process.stderr, log, "ERR: "), daemon=True).start()

            # Wait for process to complete in the background
            threading.Thread(target=lambda: (
                process.wait(),
                log.write_line(f"[Process exit code: {process.returncode}]")
            ), daemon=True).start()

        except Exception as e:
            log.write_line(f"[red]Error running command: {e}[/red]")


if __name__ == "__main__":
    DevMenu().run()

