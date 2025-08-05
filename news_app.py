from tkinter import *
from tkinter import messagebox
from urllib.parse import urlencode
import os
import requests

# Constants
API_KEY = os.getenv("NEWSAPI_KEY", "24998c027203417cb77e2d0609741910")
BASE_URL = (
    'http://newsapi.org/v2/top-headlines?country=in&category={}&apiKey=' + API_KEY
)
EVERYTHING_URL = 'https://newsapi.org/v2/everything?'

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700+0+0')
        self.root.title("eNewsPaper")

        # ==== Categories ==== #
        self.news_categories = ["general", "entertainment", "business", "sports", "technology", "health"]

        # ==== Styling ==== #
        bg_color = "#404040"
        text_area_bg = "#b8e0c4"
        basic_font_color = "#ccc4c4"

        # ==== Title Frame ==== #
        title = Label(self.root, text="NewsPaper Software", font=("times new roman", 30, "bold"),
                      pady=2, bd=12, relief=GROOVE, bg=bg_color, fg=basic_font_color)
        title.pack(fill=X)

        # ==== Search Frame ==== #
        search_frame = LabelFrame(
            self.root,
            text="Search",
            font=("times new roman", 20, "bold"),
            bg=bg_color,
            fg=basic_font_color,
            bd=10,
            relief=GROOVE,
        )
        search_frame.place(x=0, y=80, width=300, height=260)

        # Keyword
        Label(
            search_frame,
            text="Keyword",
            font=("arial", 12, "bold"),
            bg=bg_color,
            fg=basic_font_color,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.query_entry = Entry(search_frame, font=("arial", 12))
        self.query_entry.grid(row=0, column=1, padx=5, pady=5)

        # Source filter
        Label(
            search_frame,
            text="Source",
            font=("arial", 12, "bold"),
            bg=bg_color,
            fg=basic_font_color,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = Entry(search_frame, font=("arial", 12))
        self.source_entry.grid(row=1, column=1, padx=5, pady=5)

        # Date filter
        Label(
            search_frame,
            text="From (YYYY-MM-DD)",
            font=("arial", 12, "bold"),
            bg=bg_color,
            fg=basic_font_color,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.from_entry = Entry(search_frame, font=("arial", 12))
        self.from_entry.grid(row=2, column=1, padx=5, pady=5)

        # Language option
        Label(
            search_frame,
            text="Language",
            font=("arial", 12, "bold"),
            bg=bg_color,
            fg=basic_font_color,
        ).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.lang_var = StringVar(value="en")
        OptionMenu(search_frame, self.lang_var, "en", "ar").grid(
            row=3, column=1, padx=5, pady=5
        )

        Button(
            search_frame,
            text="SEARCH",
            width=20,
            bd=7,
            font="arial 12 bold",
            command=self.search_news,
        ).grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # ==== Category Frame ==== #
        category_frame = LabelFrame(
            self.root,
            text="Category",
            font=("times new roman", 20, "bold"),
            bg=bg_color,
            fg=basic_font_color,
            bd=10,
            relief=GROOVE,
        )
        category_frame.place(x=0, y=350, width=300, relheight=0.6)

        for idx, category in enumerate(self.news_categories):
            button = Button(
                category_frame,
                text=category.upper(),
                width=20,
                bd=7,
                font="arial 15 bold",
                command=lambda c=category: self.display_news(c),
            )
            button.grid(row=idx, column=0, padx=10, pady=5)

        # ==== News Frame ==== #
        news_frame = Frame(self.root, bd=7, relief=GROOVE)
        news_frame.place(x=320, y=80, relwidth=0.7, relheight=0.8)

        news_title = Label(news_frame, text="News Area", font=("arial", 20, "bold"), bd=7, relief=GROOVE)
        news_title.pack(fill=X)

        scroll_y = Scrollbar(news_frame, orient=VERTICAL)
        self.news_text_area = Text(news_frame, yscrollcommand=scroll_y.set, font=("times new roman", 15, "bold"),
                                   bg=text_area_bg, fg="#3206b8")
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.news_text_area.yview)

        self.news_text_area.insert(
            END, "PLEASE SELECT A CATEGORY TO VIEW HEADLINES. CONNECTION SPEED MAY AFFECT LOADING!")
        self.news_text_area.pack(fill=BOTH, expand=1)

    def display_news(self, category):
        url = BASE_URL.format(category)
        self.news_text_area.delete("1.0", END)
        self.news_text_area.insert(END, f"Fetching news for category: {category.upper()}...\n\n")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP status codes
            articles = response.json().get('articles', [])

            if articles:
                for article in articles:
                    self.news_text_area.insert(END, f"Title: {article['title']}\n")
                    self.news_text_area.insert(END, f"Description: {article.get('description', 'No description')}\n")
                    self.news_text_area.insert(END, f"Read more: {article['url']}\n")
                    self.news_text_area.insert(END, "-" * 80 + "\n")
            else:
                self.news_text_area.insert(END, "No news available for this category.\n")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                messagebox.showerror("Error", "Invalid API Key. Please check your API Key.")
            else:
                messagebox.showerror("Error", f"HTTP Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def search_news(self):
        query = self.query_entry.get()
        source = self.source_entry.get()
        from_date = self.from_entry.get()
        language = self.lang_var.get()

        if not query:
            messagebox.showerror("Error", "Please enter a keyword to search.")
            return

        params = {"q": query, "apiKey": API_KEY, "language": language}
        if source:
            params["sources"] = source
        if from_date:
            params["from"] = from_date
        url = EVERYTHING_URL + urlencode(params)

        self.news_text_area.delete("1.0", END)
        self.news_text_area.insert(END, f"Searching for: {query}\n\n")

        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get("articles", [])

            if articles:
                for article in articles:
                    self.news_text_area.insert(END, f"Title: {article['title']}\n")
                    self.news_text_area.insert(
                        END, f"Description: {article.get('description', 'No description')}\n"
                    )
                    self.news_text_area.insert(END, f"Read more: {article['url']}\n")
                    self.news_text_area.insert(END, "-" * 80 + "\n")

                self.generate_html(articles)
            else:
                self.news_text_area.insert(END, "No news articles found.\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_html(self, articles, filename="search_results.html"):
        try:
            with open(filename, "w", encoding="utf-8") as html_file:
                html_file.write(
                    "<html><head><meta charset='utf-8'><title>Search Results" "</title></head><body>"
                )
                for article in articles:
                    html_file.write(
                        f"<h2><a href='{article['url']}'>{article['title']}</a></h2>"
                    )
                    html_file.write(
                        f"<p>{article.get('description', 'No description')}</p><hr>"
                    )
                html_file.write("</body></html>")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write HTML: {e}")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = NewsApp(root)
    root.mainloop()
