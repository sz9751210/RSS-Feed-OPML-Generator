import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QTextBrowser, QVBoxLayout, QWidget
import feedparser
import markdown

class RSSReader(QMainWindow):
    def __init__(self, feed_url):
        super().__init__()

        self.feed_url = feed_url
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("RSS Reader")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Title"])
        self.tree_widget.setColumnCount(1)
        self.tree_widget.itemClicked.connect(self.display_item_content)

        self.text_browser = QTextBrowser()

        self.layout.addWidget(self.tree_widget)
        self.layout.addWidget(self.text_browser)

        self.central_widget.setLayout(self.layout)

        self.populate_tree_widget()

    def populate_tree_widget(self):
        feed = feedparser.parse(self.feed_url)
        self.feed_entries = feed.entries
        for entry in self.feed_entries:
            title_item = QTreeWidgetItem([entry.title])
            title_item.entry = entry
            self.tree_widget.addTopLevelItem(title_item)

    def display_item_content(self, item):
        entry = item.entry
        if entry:
            content = entry.content[0].value if hasattr(entry, 'content') else entry.summary
            markdown_content = self.convert_to_markdown(content)
            self.text_browser.setOpenExternalLinks(True)
            self.text_browser.setMarkdown(markdown_content)

    def convert_to_markdown(self, html_content):
        md = markdown.Markdown()
        return md.convert(html_content)

if __name__ == "__main__":
    feed_url = 'https://zhangguanzhang.github.io/atom.xml'  # Replace with your RSS feed URL
    app = QApplication(sys.argv)
    reader = RSSReader(feed_url)
    reader.show()
    sys.exit(app.exec_())
