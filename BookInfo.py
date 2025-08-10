class BookInfo: 
    
    def __init__(self, title, author, downloads):
        self.title = title
        self.author = author
        self.downloads = int(downloads)

    def __repr__(self):                                    
        return f"{self.author}: {self.title} ({self.downloads} Downloads)"

    # Getter
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author
    
    def get_downloads(self):
        return self.downloads
                                                



