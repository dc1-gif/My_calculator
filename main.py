from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class CalculatorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # حقل إدخال النص (الذي ستكتب فيه العملية الحسابية)
        self.input_box = TextInput(font_size=32, multiline=False, halign='right')
        self.layout.add_widget(self.input_box)
        
        # زر الحساب
        calc_button = Button(text='احسب (Calculate)', font_size=24)
        calc_button.bind(on_press=self.calculate)
        self.layout.add_widget(calc_button)
        
        return self.layout

    def calculate(self, instance):
        try:
            # استخدام eval التي تدربت عليها لمعالجة النص الرياضي
            user_input = self.input_box.text
            result = eval(user_input)
            
            # تحويل النتيجة إلى رقم صحيح إذا كانت تقبل القسمة بدون باقي
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            self.input_box.text = str(result)
        except Exception:
            self.input_box.text = "خطأ (Error)"

if __name__ == '__main__':
    CalculatorApp().run()
