from kivy.core.text import LabelBase
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# Register the font
LabelBase.register(name='DejaVuSans', fn_regular='fonts/dejavu-sans/DejaVuSans.ttf')


# Create a custom SpinnerOption class to apply font
class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super(CustomSpinnerOption, self).__init__(**kwargs)
        self.font_name = 'DejaVuSans'  # Apply the custom font for each option


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Greek symbol for νₑ
        label = Label(
            text="\u03BD\u2091",  # νₑ symbol
            font_name='DejaVuSans',  # Apply font
            font_size='40sp'
        )
        layout.add_widget(label)

        # Dropdown with Greek flavours
        flavour_options = [
            "\u03BD\u2091",  # νₑ
            "\u03BD\u0304\u2091",  # ν̅ₑ
            "\u03BD\u03BC",  # ν_μ
            "\u03BD\u0304\u03BC",  # ν̅_μ
            "\u03BD\u03C4",  # ν_τ
            "\u03BD\u0304\u03C4"  # ν̅_τ
        ]

        dropdown1 = Spinner(
            text='Flavour',
            values=flavour_options,  # Greek symbol options
            size_hint=(1, 0.2),
            font_name='DejaVuSans',  # Use the registered font for the selected item
            option_cls=CustomSpinnerOption  # Apply the custom SpinnerOption class for the dropdown items
        )

        # Bind to ensure dropdown items use the custom font when shown
        dropdown1.bind(on_dropdown=self.on_dropdown_open)

        layout.add_widget(dropdown1)

        return layout

    def on_dropdown_open(self, spinner, dropdown):
        """Ensure the font is set correctly for all SpinnerOption items when the dropdown opens."""
        for option in dropdown.container.children:
            option.font_name = 'DejaVuSans'  # Apply custom font for each dropdown item


if __name__ == '__main__':
    TestApp().run()
