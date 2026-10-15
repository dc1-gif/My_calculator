import ast
import operator

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button

Window.clearcolor = (0.07, 0.07, 0.08, 1)

KV = """
<CalcButton>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    font_size: '32sp'
    color: self.fg
    canvas.before:
        Color:
            rgba: self.bg if self.state == 'normal' else [min(c + 0.15, 1) for c in self.bg]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height / 2.5]

BoxLayout:
    orientation: 'vertical'
    padding: 16
    spacing: 16

    Label:
        id: display
        size_hint_y: 0.25
        text: ''
        font_size: '72sp' if len(self.text) < 9 else '44sp'
        halign: 'right'
        valign: 'bottom'
        text_size: self.size
        color: 1, 1, 1, 1

    GridLayout:
        id: grid
        cols: 4
        spacing: 12
"""

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


class CalcButton(Button):
    bg = ListProperty([0.2, 0.2, 0.22, 1])
    fg = ListProperty([1, 1, 1, 1])


NUMBER = ([0.2, 0.2, 0.22, 1], [1, 1, 1, 1])
FUNCTION = ([0.65, 0.65, 0.68, 1], [0, 0, 0, 1])
OPERATOR = ([1, 0.58, 0, 1], [1, 1, 1, 1])

KEYS = [
    ("C", FUNCTION), ("<", FUNCTION), ("%", FUNCTION), ("÷", OPERATOR),
    ("7", NUMBER), ("8", NUMBER), ("9", NUMBER), ("×", OPERATOR),
    ("4", NUMBER), ("5", NUMBER), ("6", NUMBER), ("−", OPERATOR),
    ("1", NUMBER), ("2", NUMBER), ("3", NUMBER), ("+", OPERATOR),
    ("00", NUMBER), ("0", NUMBER), (".", NUMBER), ("=", OPERATOR),
]

SYMBOLS = {"÷": "/", "×": "*", "−": "-"}


class CalculatorApp(App):
    def build(self):
        root = Builder.load_string(KV)
        self.display = root.ids.display
        self.just_calculated = False

        for label, (bg, fg) in KEYS:
            btn = CalcButton(text=label, bg=bg, fg=fg)
            btn.bind(on_press=self.on_key)
            root.ids.grid.add_widget(btn)
        return root

    def on_key(self, button):
        key = button.text
        text = self.display.text

        if key == "C":
            self.display.text = ""
        elif key == "<":
            self.display.text = text[:-1]
        elif key == "=":
            self.calculate()
        else:
            if text == "Error" or (self.just_calculated and key.isdigit()):
                text = ""
            self.display.text = text + key
        if key != "=":
            self.just_calculated = False

    def calculate(self):
        expr = self.display.text
        for shown, real in SYMBOLS.items():
            expr = expr.replace(shown, real)
        try:
            result = safe_eval(expr)
            if isinstance(result, float):
                result = round(result, 10)
                if result.is_integer():
                    result = int(result)
            self.display.text = str(result)
            self.just_calculated = True
        except Exception:
            self.display.text = "Error"


if __name__ == "__main__":
    CalculatorApp().run()
