from kivymd.uix.menu import MDDropdownMenu


class MessageMenu(MDDropdownMenu):
    def __init__(self, text, link, post, pictures, **kwargs):
        super().__init__(**kwargs)
        self.items = [
            {
                "text": "Text Message",
                "leading_icon": "text",
                "on_release": text,
            },
            {
                "text": "Link",
                "leading_icon": "link",
                "on_release": link,
            },
            {
                "text": "Your Post",
                "leading_icon": "movie-roll",
                "on_release": post,
            },
            {
                "text": "Pictures",
                "leading_icon": "image",
                "on_release": pictures,
            },
        ]
