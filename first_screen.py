from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup  # Import Popup for exit confirmation
from kivy.uix.label import Label
from kivy.uix.widget import Widget  # Import Widget for spacing
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for the popup
from kivy.app import App  # Import App to stop the application
from kivy.core.window import Window  # Import Window to close the application
from PIL import Image as PILImage  # Import Pillow for image handling

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        # Use FloatLayout to allow for absolute positioning
        layout = FloatLayout()

        # Load the logo using Pillow to get its size
        pil_image = PILImage.open('logo.png')
        original_width, original_height = pil_image.size  # Get original dimensions

        # Desired new width (you can change this value as needed)
        new_width = 380
        aspect_ratio = original_width / original_height
        new_height = new_width / aspect_ratio  # Calculate new height

        # Add the logo/picture at the center with padding
        logo = Image(source='logo.png', size_hint=(None, None), size=(new_width, new_height))

        # Center the logo
        logo.pos_hint = {'center_x': 0.5, 'center_y': 0.65}  # Center horizontally and set a vertical position

        layout.add_widget(logo)

        # Add an invisible widget to create space below the logo
        layout.add_widget(Widget(size_hint_y=None, height=30))  # Adjust height for desired spacing

        # Add the DEMO button
        demo_button = Button(text='DEMO', size_hint=(None, None), size=(170, 40))  # Slightly larger than exit button
        demo_button.bind(on_press=self.show_demo_popup)  # Bind action for the button
        demo_button.pos_hint = {'center_x': 0.5, 'center_y': 0.28}  # Center the button below the logo
        layout.add_widget(demo_button)

        # Add the GAME button
        game_button = Button(text='GAME', size_hint=(None, None), size=(170, 40))  # Slightly larger than exit button
        game_button.bind(on_press=self.show_game_popup)  # Bind action for the button
        game_button.pos_hint = {'center_x': 0.5, 'center_y': 0.20}  # Center the button below the logo
        layout.add_widget(game_button)

        # Add the EVENTS button
        events_button = Button(text='EVENTS', size_hint=(None, None), size=(170, 40))  # Slightly larger than exit button
        events_button.bind(on_press=self.events_action)  # Bind action for the button
        events_button.pos_hint = {'center_x': 0.5, 'center_y': 0.12}  # Center the button below the logo
        layout.add_widget(events_button)

        # Add the exit button
        exit_button = Button(text='Exit', size_hint=(None, None), size=(60, 30))  # Small size for the exit button
        exit_button.bind(on_press=self.exit_app)
        exit_button.pos_hint = {'center_x': 0.5, 'center_y': 0.04}  # Center exit button at the bottom
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def show_demo_popup(self, instance):
        """Show the popup for the DEMO button."""
        self.show_action_popup("DEMO")

    def show_game_popup(self, instance):
        """Show the popup for the GAME button."""
        self.show_action_popup("GAME")

    def show_action_popup(self, action):
        """Create and show a popup with Play, Pause, and Exit buttons."""
        popup_content = BoxLayout(orientation='vertical', padding=10)

        # Add a label for the action type
        popup_content.add_widget(Label(text=f"{action} Options"))

        # Play button
        play_button = Button(text='Play')
        play_button.bind(on_press=lambda x: self.popup_action(action, "Play"))  # Bind action

        # Pause button
        pause_button = Button(text='Pause')
        pause_button.bind(on_press=lambda x: self.popup_action(action, "Pause"))  # Bind action

        # Exit button
        exit_button = Button(text='Exit')
        exit_button.bind(on_press=lambda x: self.popup_exit_action(action))  # Bind exit action

        # Add buttons to the popup layout
        popup_content.add_widget(play_button)
        popup_content.add_widget(pause_button)
        popup_content.add_widget(exit_button)

        # Create the popup
        popup = Popup(title=f"{action} Menu", content=popup_content, size_hint=(0.5, 0.5))
        popup.open()
        # Store the popup for later dismissal
        self.current_popup = popup

    def popup_exit_action(self, action):
        """Handle exit action from popup and return to first screen."""
        self.manager.current = 'first'  # Transition back to the first screen
        self.current_popup.dismiss()  # Dismiss the popup

    def popup_action(self, action, option):
        """Handle actions from the popup."""
        print(f"{action} - {option} selected!")

    def demo_action(self, instance):
        print("DEMO button pressed!")  # Action for DEMO button

    def game_action(self, instance):
        print("GAME button pressed!")  # Action for GAME button

    def events_action(self, instance):
        self.manager.current = 'events'  # Change to the EventsScreen

    def exit_app(self, instance):
        # Create a popup for exit confirmation
        popup = Popup(title='Exit Confirmation',
                      content=BoxLayout(orientation='vertical'),  # Use BoxLayout for popup content
                      size_hint=(0.5, 0.5))

        # Label for the popup
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(Label(text='Are you sure you want to exit?'))

        # Yes button
        yes_button = Button(text='Yes')
        yes_button.bind(on_press=self.confirm_exit)  # Bind the yes button to exit logic

        # No button
        no_button = Button(text='No')
        no_button.bind(on_press=popup.dismiss)  # Just dismiss the popup

        # Add buttons to the popup layout
        popup_content.add_widget(yes_button)
        popup_content.add_widget(no_button)

        # Set the popup content
        popup.content = popup_content
        popup.open()

    def confirm_exit(self, instance):
        App.get_running_app().stop()  # Stops the application
        Window.close()  # Closes the window
