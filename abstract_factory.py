"""
Abstract Factory Pattern
-------------------------
Provides an interface for creating FAMILIES of related objects without
specifying their concrete classes. Where Factory Method creates ONE
product, Abstract Factory creates a whole consistent set of products
that are meant to work together.

Real-world use cases:
- Cross-platform UI toolkits (Windows vs macOS widgets)
- Database driver families (Postgres connection + Postgres cursor + ...)
- Cloud provider SDK abstraction (AWS vs GCP storage + compute + queue)
"""

from abc import ABC, abstractmethod


# ---- Abstract product interfaces ----
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


# ---- Concrete product family: Windows ----
class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[Windows Checkbox]"


# ---- Concrete product family: macOS ----
class MacButton(Button):
    def render(self) -> str:
        return "(Mac Button)"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "(Mac Checkbox)"


# ---- Abstract Factory ----
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        ...


class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


def render_ui(factory: UIFactory) -> None:
    """Client code works only with the abstract factory/products —
    it never knows or cares which OS family it's rendering."""
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(button.render(), checkbox.render())


if __name__ == "__main__":
    import platform

    factory = WindowsUIFactory() if platform.system() == "Windows" else MacUIFactory()
    render_ui(factory)

    # Explicitly swapping the whole family at once — the key benefit:
    render_ui(WindowsUIFactory())
    render_ui(MacUIFactory())
