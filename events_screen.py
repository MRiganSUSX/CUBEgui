from kivy.uix.floatlayout import FloatLayout  # Ensure FloatLayout is imported
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for the input layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner  # Import Spinner for dropdowns
from kivy.uix.textinput import TextInput  # Import TextInput for the input box
from kivy.uix.scrollview import ScrollView  # Import ScrollView for scrolling
from kivy.graphics import Color, Rectangle  # For creating backgrounds
import json


def load_select():
    # Load the JSON file
    with open('select.json', 'r') as file:  # Replace 'select.json' with your file name
        data = json.load(file)
        return data


class EventsScreen(Screen):
    def __init__(self, **kwargs):
        super(EventsScreen, self).__init__(**kwargs)

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
        input_container = BoxLayout(orientation='vertical', size_hint=(1, 0.6), padding=[0, 0],
                                    pos_hint={'center_y': 0.55})

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

        # Set the background color of the ScrollView to black
        with scroll_view.canvas.before:
            Color(0, 0, 0, 1)  # Set color for the background (black)
            self.bg_rect = Rectangle(pos=(0, 0), size=scroll_view.size)

        # Update the background rectangle on resize
        scroll_view.bind(size=self.update_bg_rect)

        # Add the ScrollView to the input container
        input_container.add_widget(scroll_view)

        # Add the input container to the main layout
        layout.add_widget(input_container)

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

    def update_bg_rect(self, instance, value):
        """Update the position and size of the background rectangle."""
        self.bg_rect.pos = (0, 0)
        self.bg_rect.size = instance.size

    def add_input_row(self, instance=None):
        """Adds a new row of input fields."""
        input_row = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50,
            padding=[30, 0]  # Side padding for the new row
        )

        # Prep the dropdown data
        data = load_select()
        flavour_options = data["flavours"] + ["Background"]

        # Dropdown 1 (Spinner)
        dropdown1 = Spinner(
            text='Flavour',
            values=flavour_options,  # Example options
            size_hint=(20 / 100, None),  # Set size hint ratio
            height=40
        )
        dropdown1.bind(text=self.update_energy_dropdown)  # Bind the first dropdown

        input_row.add_widget(dropdown1)

        # Dropdown 2 (Spinner)
        dropdown2 = Spinner(
            text='Energy',
            values=[],  # Initially empty
            size_hint=(20 / 100, None),  # Set size hint ratio
            height=40,
            disabled=True  # Initially disabled
        )
        input_row.add_widget(dropdown2)

        # Text Input Box with centered text
        text_input = TextInput(
            hint_text='Event numbers',
            size_hint=(50 / 100, None),  # Set size hint ratio
            height=40,
            halign='center',  # Center text horizontally
            multiline=False,  # Set to False to keep it a single line
            padding_y=(10, 10),  # Add vertical padding for centering effect
            disabled=True  # Initially disabled
        )
        text_input.bind(on_text_validate=lambda instance: self.validate_input(instance, text_input.text, data))  # Bind to validation method
        input_row.add_widget(text_input)

        # Add the new input row to the main input layout (stacking below)
        self.input_layout.add_widget(input_row)

        # Store the input row in the list for later access
        self.input_rows.append((dropdown1, dropdown2, text_input))

    def update_energy_dropdown(self, spinner, text):
        """Update the second dropdown based on the selection in the first dropdown."""
        data = load_select()

        if text == "Background":
            energy_options = data["background"]["energy"]
        else:
            energy_options = data["neutrino"]["energy"]

        # Ensure energy options are strings
        energy_options = [str(option) for option in energy_options]

        if self.input_rows:
            last_row = self.input_rows[-1][1]  # Get the dropdown2 from the last input row
            last_row.values = energy_options  # Set new values for the second dropdown
            last_row.text = energy_options[0] if energy_options else ''  # Reset selection
            last_row.disabled = False  # Enable the energy dropdown

            # Enable the text input box for event numbers
            last_text_input = self.input_rows[-1][2]  # Get the TextInput from the last input row
            last_text_input.disabled = False  # Enable the text input

    def validate_input(self, instance, value, data):
        """Validate the input to ensure it only contains integers or arrays of integers."""
        if value.strip() == "":
            return False  # Ignore empty input

        # Get the maximum value from the evs limit
        max_value = max(data["neutrino"]["evs"]) if data["neutrino"]["evs"] else 0

        # Check if the input is a single integer, a list of integers, or a range
        try:
            # Allow comma-separated values, and ranges like "1-10"
            if '-' in value:
                start, end = value.split('-')
                start, end = int(start.strip()), int(end.strip())
                if start > max_value or end > max_value or start > end:
                    instance.text = ''  # Clear input if the range exceeds the limit or is invalid
                    return False
            elif ',' in value:
                # Split the input by commas and convert to integers
                int_list = [int(num.strip()) for num in value.split(',')]
                if any(num > max_value for num in int_list):
                    instance.text = ''  # Clear the input if any number exceeds the limit
                    return False
            else:
                # Single integer input
                num = int(value)
                if num > max_value:
                    instance.text = ''  # Clear the input if it exceeds the limit
                    return False

        except ValueError:
            instance.text = ''  # Clear the input if it's not a valid integer or list
            return False

        return True  # Input is valid

    def submit_data(self, instance, mode):
        """Collects data from all input rows and handles submission logic."""
        data = load_select()  # Load data for validation
        valid_submission = True  # Flag to track if all inputs are valid

        for dropdown1, dropdown2, text_input in self.input_rows:
            selected_option1 = dropdown1.text
            selected_option2 = dropdown2.text
            entered_text = text_input.text

            # Validate the input before processing it
            if not self.validate_input(text_input, entered_text, data):  # Validate during submission
                valid_submission = False  # Mark the submission as invalid
                print(f'Invalid input for: {selected_option1}, {selected_option2}')
                continue  # Skip to the next row

            # If the input is valid, proceed with submission
            print(
                f'Selected Option 1: {selected_option1}, Selected Option 2: {selected_option2}, '
                f'Entered Text: {entered_text}'
            )

        # Optionally handle the case if there are no valid submissions
        if not valid_submission:
            print("Submission failed due to invalid inputs.")

    def go_back(self, instance):
        # This will transition back to the first screen
        self.manager.current = 'first'  # Assuming the first screen is named 'first'
