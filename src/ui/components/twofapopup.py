
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Builder.load_string(
    """
<twofaPopupContent>:
    orientation: "vertical"
    spacing: "30dp"
    padding: "30dp"
    size_hint_y: None
    height: self.minimum_height
    MDTextField:
        id: twofa
        hint_text: "Enter 2FA Code"
        text: ""
        helper_text: "Enter the code from your authentication app"
        pos_hint: {"center_x": 0.5}
        required: True
        mode: "fill"
        multiline: False
    """
)


class twofaPopupContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class twofaPopup(MDDialog):
    content_cls: twofaPopupContent = None

    ok_button: MDRaisedButton = None

    cancel_button: MDFlatButton = None

    def __init__(self, **kwargs):
        self.content_cls = twofaPopupContent()
        self.ok_button = MDRaisedButton(text="Verify")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.cancel_button.bind(on_release=self.dismiss)
        super().__init__(
            title="Two Factor Authentication",
            type="custom",
            content_cls=twofaPopupContent(),
            buttons=[self.cancel_button, self.ok_button],
        )
