import re

from html2text import HTML2Text


class HTML2TextTransformer(HTML2Text):
    """
    Ignore links, images, formatting and line breaks
    """

    def __init__(self):
        super().__init__()
        self.ignore_links = True  # Ignore links
        self.ignore_images = True  # Ignore images
        self.ignore_emphasis = False  # Ignore formatting
        self.body_width = 0

    def handle(self, html: str) -> str:
        """
        Remove/replace <br>, </p>, and <p> with a space
        """
        html = re.sub(r"<br\s*/?>", " ", html)
        html = re.sub(r"</?p>", " ", html)
        html = re.sub(r"\s{2,}", " ", html)
        return super().handle(html)
