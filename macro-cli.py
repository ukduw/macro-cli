from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Footer
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
import plotext as plt
import io
import sys

# Fake inflation data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
inflation = [2.1, 2.4, 3.0, 3.6, 3.3, 2.9]

class ChartView(Static):
    selected_index = reactive(0)

    def on_mount(self):
        self.plot_chart()

    def plot_chart(self):
        # Redirect plotext output to string
        sys.stdout = io.StringIO()
        plt.clear_figure()
        plt.title("Inflation Rate %")
        plt.plot(months, inflation, marker="dot", color="cyan")
        plt.scatter([months[self.selected_index]], [inflation[self.selected_index]], marker='circle', color='red')
        plt.plotsize(60, 15)
        plt.ylim(0, max(inflation) + 1)
        plt.show()
        chart_output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        label = f"{months[self.selected_index]}: {inflation[self.selected_index]}%"
        self.update(f"[bold green]Selected:[/bold green] {label}\n\n[white on black]{chart_output}[/]")

    def on_key(self, event):
        if event.key in ["left"]:
            self.selected_index = (self.selected_index - 1) % len(months)
            self.plot_chart()
        elif event.key in ["right"]:
            self.selected_index = (self.selected_index + 1) % len(months)
            self.plot_chart()

class Menu(Static):
    def compose(self) -> ComposeResult:
        yield Button("Inflation Chart", id="chart", variant="primary")
        yield Button("Exit", id="exit", variant="error")

class TerminalApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    Menu {
        width: 30%;
        border: heavy green;
        padding: 1;
        height: 100%;
    }
    ChartView {
        border: panel green;
        padding: 1;
        height: 100%;
    }
    Button {
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Menu()
        yield ChartView()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.exit()

if __name__ == "__main__":
    TerminalApp().run()



# world bank dl, tradingeconomics scrape...
# periodic scrape to check for changes...
    # or maybe just once per run?