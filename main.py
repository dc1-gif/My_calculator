import ast
import operator

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}


def safe_eval(expr):
    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = ev(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        raise ValueError("Invalid expression")

    return ev(ast.parse(expr, mode="eval"))


class CalculatorApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.display = TextInput(
            font_size=48,
            multiline=False,
            readonly=True,
            halign="right",
            size_hint_y=0.2,
        )
        root.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=8)
        keys = [
            "C", "<", "%", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "0", ".", "=", "",
        ]
        for key in keys:
            if key == "":
                grid.add_widget(BoxLayout())
                continue
            btn = Button(text=key, font_size=32)
            btn.bind(on_press=self.on_key)
            grid.add_widget(btn)
        root.add_widget(grid)

        return root

    def on_key(self, button):
        key = button.text
        if key == "C":
            self.display.text = ""
        elif key == "<":
            self.display.text = self.display.text[:-1]
        elif key == "=":
            self.calculate()
        else:
            if self.display.text == "Error":
                self.display.text = ""
            self.display.text += key

    def calculate(self):
        try:
            result = safe_eval(self.display.text)
            if isinstance(result, float):
                result = round(result, 10)
                if result.is_integer():
                    result = int(result)
            self.display.text = str(result)
        except Exception:
            self.display.text = "Error"


if __name__ == "__main__":
    CalculatorApp().run()
