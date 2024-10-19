from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line
from kivy.core.text import LabelBase
import json

# Register the custom font
LabelBase.register(name='DejaVuSans', fn_regular='fonts/dejavu-sans/DejaVuSans.ttf')


# Custom SpinnerOption class to apply font to dropdown items
class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super(CustomSpinnerOption, self).__init__(**kwargs)
        self.font_name = 'DejaVuSans'  # Apply the custom font for each option


def load_select():
    # Load the JSON file
    with open('select.json', 'r') as file:  # Replace 'select.json' with your file name
        data = json.load(file)
        return data


class EventsScreen(Screen):
    def __init__(self, **kwargs):
        super(EventsScreen, self).__init__(**kwargs)

        # Path to the custom font that supports Greek symbols
        font_path = "DejaVuSans"  # Use the registered font

        # Initialize the input rows list
        self.input_rows = []  # Ensure this is defined here

        # Use FloatLayout to allow absolute positioning
        layout = FloatLayout()
        layout.padding = [20, 10, 10, 20]  # Set padding for the layout

        # Add a title label for the Events screen at the top
        title_label = Label(
            text='Events Selection',
            font_size='30sp',
            size_hint_y=None,
            height=40,
            pos_hint={'x': 0, 'top': 0.98}  # Position at the very top
        )
        layout.add_widget(title_label)

        # Create a BoxLayout for the ScrollView with fixed dimensions
        self.input_container = BoxLayout(orientation='vertical', size_hint=(0.9, 0.6), padding=[30, 10],
                                         pos_hint={'center_y': 0.55, 'center_x': 0.5})

        # Create a ScrollView for the input fields
        scroll_view = ScrollView(size_hint=(1, 1))  # Fill the available space

        # Create a vertical BoxLayout to hold input rows
        self.input_layout = BoxLayout(
            orientation='vertical',  # Stack input rows vertically
            spacing=10,
            size_hint_y=None,
            padding=[0, 0]  # No additional padding
        )
        self.input_layout.bind(minimum_height=self.input_layout.setter('height'))  # Allow dynamic height

        # Initial input row
        self.add_input_row()

        # Add the input layout to the ScrollView
        scroll_view.add_widget(self.input_layout)

        # Add the ScrollView to the input container
        self.input_container.add_widget(scroll_view)

        # Create a white border around the visible area of the scroll view
        with self.input_container.canvas.after:
            self.border_color = Color(1, 1, 1, 1)  # Set color to white
            self.border_line = Line()

        # Bind size and position changes of the input container to update the border
        self.input_container.bind(pos=self.update_border, size=self.update_border)

        # Add the input container to the main layout
        layout.add_widget(self.input_container)

        # Add "+" button to add more input rows
        add_button = Button(text='+', size_hint=(None, None), size=(30, 30))
        add_button.bind(on_press=self.add_input_row)  # Bind the button to add a new input row
        add_button.pos_hint = {'center_x': 0.95, 'center_y': 0.95}  # Position it below the input row
        layout.add_widget(add_button)

        # Add Static Submit Button
        static_button = Button(text='Submit Static', size_hint=(None, None), size=(185, 50))
        static_button.bind(on_press=lambda instance: self.submit_data(instance, "Static"))  # Bind with flag
        static_button.pos_hint = {'center_x': 0.35, 'center_y': 0.15}  # Position near the middle
        layout.add_widget(static_button)

        # Add Dynamic Submit Button
        dynamic_button = Button(text='Submit Dynamic', size_hint=(None, None), size=(185, 50))
        dynamic_button.bind(on_press=lambda instance: self.submit_data(instance, "Dynamic"))  # Bind with flag
        dynamic_button.pos_hint = {'center_x': 0.65, 'center_y': 0.15}  # Position near the middle
        layout.add_widget(dynamic_button)

        # Add a back button at the bottom
        back_button = Button(text='Back to Main Menu', size_hint=(None, None), size=(170, 40))
        back_button.bind(on_press=self.go_back)  # Bind action for the back button
        back_button.pos_hint = {'center_x': 0.5, 'center_y': 0.05}  # Position at the bottom
        layout.add_widget(back_button)

        # Add the main layout to the screen
        self.add_widget(layout)

    def update_border(self, instance, value):
        """Update the white border around the input container dynamically."""
        self.border_line.rectangle = (self.input_container.x, self.input_container.y,
                                      self.input_container.width, self.input_container.height)

    def add_input_row(self, instance=None):
        """Adds a new row of input fields."""
        input_row = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50,
            padding=[30, 0]  # Side padding for the new row
        )

        # Load the data with Greek symbols
        data = load_select()

        # Extract flavour symbols for display and names for logic
        flavour_names = data["flavours"]["name"]
        flavour_symbols = data["flavours"]["symbol"]

        # Map the symbols to their corresponding names for later use
        self.symbol_to_name = {symbol: name for name, symbol in zip(flavour_names, flavour_symbols)}

        # Display symbols in the dropdown but use names for internal logic
        flavour_options = flavour_symbols + ["Background"]

        # Dropdown 1 (Spinner)
        dropdown1 = Spinner(
            text='Flavour',
            values=flavour_options,  # Show the symbols in the dropdown
            size_hint=(20 / 100, None),  # Set size hint ratio
            height=40,
            font_name="DejaVuSans",  # Use the registered font for the selected item
            option_cls=CustomSpinnerOption  # Apply the custom SpinnerOption class for dropdown items
        )

        # Dropdown 2 (Spinner)
        dropdown2 = Spinner(
            text='Energy',
            values=[],  # Initially empty
            size_hint=(20 / 100, None),  # Set size hint ratio
            height=40,
            disabled=True,  # Initially disabled
            font_name="DejaVuSans"  # Use the registered font
        )

        # Text Input Box with centered text
        text_input = TextInput(
            hint_text='Event numbers',
            size_hint=(50 / 100, None),  # Set size hint ratio
            height=40,
            halign='center',  # Center text horizontally
            multiline=False,  # Set to False to keep it a single line
            padding_y=(10, 10),  # Add vertical padding for centering effect
            disabled=True,  # Initially disabled
            font_name="DejaVuSans"  # Use the registered font
        )

        # Bind the flavour dropdown to update the energy dropdown for the specific row
        dropdown1.bind(text=lambda spinner, text: self.update_energy_dropdown(spinner, text, dropdown2, text_input))

        # Bind text validation to the on_text_validate event (pressing "Enter")
        text_input.bind(on_text_validate=lambda instance: self.validate_input(text_input, text_input.text, data))

        input_row.add_widget(dropdown1)
        input_row.add_widget(dropdown2)
        input_row.add_widget(text_input)

        # Add the new input row to the main input layout (stacking below)
        self.input_layout.add_widget(input_row)

        # Store the input row in the list for later access
        self.input_rows.append((dropdown1, dropdown2, text_input))

    def update_energy_dropdown(self, spinner, text, dropdown2, text_input):
        """Update the second dropdown (energy) based on the selection in the first dropdown (flavour)."""
        data = load_select()

        # Map the selected symbol back to its corresponding name
        flavour_name = self.symbol_to_name.get(text, text)  # Get the name or use 'text' if it's 'Background'

        if flavour_name == "Background":
            energy_options = data["background"]["energy"]
            evs_limits = data["background"]["evs"]
        else:
            energy_options = data["neutrino"]["energy"]
            evs_limits = data["neutrino"]["evs"]

        # Convert energy options to strings for consistency
        energy_options = [str(option) for option in energy_options]

        # Update the energy dropdown for the specific row
        dropdown2.values = energy_options  # Set new values for the second dropdown
        dropdown2.text = energy_options[0] if energy_options else ''  # Reset selection
        dropdown2.disabled = False  # Enable the energy dropdown

        # Enable the text input box for event numbers
        text_input.disabled = False  # Enable the text input

        # Bind the energy dropdown to dynamically adjust the limit based on the selected energy
        dropdown2.bind(text=lambda spinner, energy_text: self.update_event_limit(text_input, energy_text, evs_limits))

    def update_event_limit(self, text_input, energy_text, evs_limits):
        """Update the limit for event numbers based on the selected energy."""
        try:
            # Check if energy_text is 'N/A' (for Background)
            if energy_text == "N/A":
                event_limit = evs_limits[0]  # Background has only one limit
            else:
                # Convert energy_text to a string and get the index
                energy_index = self.input_rows[-1][1].values.index(str(energy_text))  # Get the index of the energy
                event_limit = evs_limits[energy_index]

            # Set the event limit on the text input (store it for validation)
            text_input.event_limit = event_limit
            print(f"Event limit for energy {energy_text}: {event_limit}")
        except (ValueError, IndexError) as e:
            # Handle the case where energy_text is not a valid index or out of bounds
            text_input.event_limit = 30  # Set a default limit if necessary
            print(f"Failed to update event limit for energy {energy_text}: {str(e)}.")

    def validate_input(self, instance, value, data):
        """Validate the input to ensure it only contains integers or arrays of integers."""
        if value.strip() == "":
            return False  # Ignore empty input and mark invalid

        # Get the maximum value from the evs limit (stored in the input field)
        max_value = getattr(instance, 'event_limit', 30)  # Default to 30 if no event limit is set

        try:
            # Allow comma-separated values, and ranges like "1-10"
            if '-' in value:
                start, end = value.split('-')
                start, end = int(start.strip()), int(end.strip())
                if start > max_value or end > max_value or start > end:
                    instance.text = ''  # Clear input if the range exceeds the limit or is invalid
                    return False  # Invalid input
            elif ',' in value:
                # Split the input by commas and convert to integers
                int_list = [int(num.strip()) for num in value.split(',')]
                if any(num > max_value for num in int_list):
                    instance.text = ''  # Clear the input if any number exceeds the limit
                    return False  # Invalid input
            else:
                # Single integer input
                num = int(value)
                if num > max_value:
                    instance.text = ''  # Clear the input if it exceeds the limit
                    return False  # Invalid input

            # If the input is valid, return True
            return True
        except ValueError:
            # If the input is not a valid integer or range, clear it and return False
            instance.text = ''  # Clear the input if it's not a valid integer or list
            return False

    def submit_data(self, instance, mode):
        """Collects data from all input rows and handles submission logic."""
        data = load_select()  # Load data for validation
        valid_submission_found = False  # Track if at least one valid submission is found

        for dropdown1, dropdown2, text_input in self.input_rows:
            selected_option1_symbol = dropdown1.text
            selected_option2 = dropdown2.text
            entered_text = text_input.text

            # Map the selected symbol to its corresponding name
            selected_option1_name = self.symbol_to_name.get(selected_option1_symbol, selected_option1_symbol)

            # Validate the input again before processing it
            if not self.validate_input(text_input, entered_text, data):  # Validate during submission
                print(f'Invalid input for: {selected_option1_name}, {selected_option2}')
                continue  # Skip to the next row if validation fails

            # If the input is valid, set the flag to True and proceed with submission
            valid_submission_found = True  # At least one valid submission is found
            print(
                f'Selected Option 1: {selected_option1_name}, Selected Option 2: {selected_option2}, '
                f'Entered Text: {entered_text}'
            )

        # Handle the case if no valid submissions were found
        if not valid_submission_found:
            print("Submission failed: No valid rows found.")
        else:
            print("Submission successful: At least one valid row was submitted.")

    def go_back(self, instance):
        # This will transition back to the first screen
        self.manager.current = 'first'  # Assuming the first screen is named 'first'
