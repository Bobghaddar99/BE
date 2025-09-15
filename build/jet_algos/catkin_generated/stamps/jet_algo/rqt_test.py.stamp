import os
from qt_gui.plugin import Plugin
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class MyRqtPlugin(Plugin):
    def __init__(self, context):
        super(MyRqtPlugin, self).__init__(context)
        self.setObjectName('MyRqtPlugin')

        # Create QWidget and set layout
        self._widget = QWidget()
        layout = QVBoxLayout()

        # Create label and button
        self.label = QLabel("Hello, RQT!")
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_click)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set layout for the main widget
        self._widget.setLayout(layout)
        context.add_widget(self._widget)

    def on_button_click(self):
        self.label.setText("Button Clicked!")

    def shutdown_plugin(self):
        # Cleanup when the plugin is shut down
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # Save plugin settings if necessary
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # Restore saved settings if necessary
        pass
