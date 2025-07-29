from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.screen import Screen
from textual import work
import asyncio

boot_lines = [
    "[bold green]GridBIOS v2.3 - Initializing...[/]",
    "[dim]Memory check:[/] [green]32K OK[/]",
    "[dim]CPU:[/] [green]Z80 Compatible - OK[/]",
    "[dim]I/O Ports:[/] [green]All Detected[/]",
    "[dim]Loading user interface...[/]",
    "[dim]Starting economic data daemon...[/]",
    "[green]System Ready.[/green]",
]

class BootScreen(Screen):
    def compose(self) -> ComposeResult:
        self.output = Static("", id="boot")
        yield self.output

    @work  # Background task, runs when screen mounts
    async def on_mount(self):
        for line in boot_lines:
            self.output.update(self.output.renderable + line + "\n")
            await asyncio.sleep(0.6)
        await asyncio.sleep(0.8)
        await self.app.push_screen("main")


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("[b green]Welcome to ECON CLI[/b green]\nPress Q to quit.", id="main")

    def on_key(self, event):
        if event.key.lower() == "q":
            self.app.exit()

class TerminalBootApp(App):
    CSS = """
    #boot {
        padding: 2;
        color: green;
        background: black;
    }
    #main {
        padding: 2;
        background: black;
        color: green;
    }
    """

    def on_mount(self):
        self.install_screen(BootScreen(), name="boot")
        self.install_screen(MainScreen(), name="main")
        self.push_screen("boot")

if __name__ == "__main__":
    TerminalBootApp().run()