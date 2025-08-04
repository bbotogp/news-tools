from tkinter import *
from tkinter import messagebox
import requests

# Constants
API_KEY = '24998c027203417cb77e2d0609741910'
BASE_URL = 'http://newsapi.org/v2/top-headlines?country=in&category={}&apiKey=' + API_KEY

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

        # ==== Category Frame ==== #
        category_frame = LabelFrame(self.root, text="Category", font=("times new roman", 20, "bold"),
                                    bg=bg_color, fg=basic_font_color, bd=10, relief=GROOVE)
        category_frame.place(x=0, y=80, width=300, relheight=0.88)

        for idx, category in enumerate(self.news_categories):
            button = Button(category_frame, text=category.upper(), width=20, bd=7, font="arial 15 bold",
                            command=lambda c=category: self.display_news(c))
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

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = NewsApp(root)
    root.mainloop()
