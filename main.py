from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from first_screen import FirstScreen  # Import the FirstScreen class
from events_screen import EventsScreen  # Import the EventsScreen class
from kivy.core.window import Window  # Import Window to set the title

class MyApp(App):
    def build(self):
        # ScreenManager to manage multiple windows
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))  # Add the first screen
        sm.add_widget(EventsScreen(name='events'))  # Add the events screen
        return sm

    def on_start(self):
        # Set the window title
        Window.set_title('DUNE :: LEDCube')  # Set your custom title here


if __name__ == '__main__':
    MyApp().run()  # Run the Kivy application
