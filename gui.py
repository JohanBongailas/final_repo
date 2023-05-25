import tkinter as tk
from tkinter.filedialog import askopenfilename
import requests
import bs4
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sysinfo import project_path
import webbrowser as wb
import unittest

font_size = 15


def create_frame():
    """
        Instantiate the Frame
    """
    root = tk.Tk()
    return root


def gui_config(root):
    """
        Configure the GUI
    """
    root.title("Wikipedia Web Scraping And Document Comparison")
    root.geometry("1920x1080")
    root.configure(bg='#2c2825')


# TODO: Put Similarity Score In content section by creating them, hiding them and than show them accordingly
def content(root):
    """
        Create the required content
    """
    global keyword, keyword_entry, keyword_submit, comparison_selection_label, comparison_selection_website, \
        comparison_selection_document, feedback_button, zoom_button, url_label, url_input, url_button, \
        lbl_filler_similarity_score, lbl_similarity_score, lbl_document, file, lbl_file
    keyword = tk.Label(root, text="Please enter keyword: ", font=("Times New Roman", 15), fg='#e3bd4b', bg='#2c2825',
                       padx=20, pady=20)
    keyword.grid(column=0, row=0)
    keyword_entry = tk.Entry(root, width=40, font=(
        "Times New Roman", 15), fg='#e3bd4b', bg='#785c54')
    keyword_entry.grid(column=1, row=0)

    keyword_submit = tk.Button(root, text='Submit Keyword', bg='#e3bd4b',
                               font=("Times New Roman", 15))
    keyword_submit.grid(column=2, row=0, padx=15)

    keyword_submit.bind("<Button-1>", keyword_submit_clicked)

    comparison_selection_label = tk.Label(root, text="Compare Method: ", font=("Times New Roman", 15), fg='#e3bd4b',
                                          bg='#2c2825')
    comparison_selection_label.grid(column=0, row=1)

    comparison_selection_website = tk.Button(
        root, text='Website', bg="#e3bd4b", font=("Times New Roman", 15), width=12)
    comparison_selection_website.grid(column=1, row=1)

    comparison_selection_document = tk.Button(root, text='Document', bg="#e3bd4b", font=("Times New Roman", 15),
                                              width=12)
    comparison_selection_document.grid(column=2, row=1)

    comparison_selection_website.bind("<Button-1>", website_comparison_clicked)

    feedback_button = tk.Button(
        root, text='Feedback', bg="#e3bd4b", font=("Times New Roman", 15), width=12)
    feedback_button.grid(column=2, row=4, pady=5)
    feedback_button.bind("<Button-1>", feedback_button_clicked)

    comparison_selection_document.bind("<Button-1>", ButtonDocumentClicked)
    zoom_button = tk.Button(root, text="Zoom", bg="#e3bd4b", font=(
        "Times New Roman", 15), width=12)
    zoom_button.grid(column=2, row=3, pady=5)
    zoom_button.bind("<Button-1>", zoom_button_clicked)

    url_label = tk.Label(text="URL: ", font=(
        "Times New Roman", 15), fg='#e3bd4b', bg='#2c2825')
    url_label.grid(column=0, row=2, pady=15)
    url_input = tk.Entry(width=40, font=(
        "Times New Roman", 15), fg='#e3bd4b', bg='#785c54')
    url_input.grid(column=1, row=2, pady=15)
    url_button = tk.Button(text="Submit URL", font=(
        "Times New Roman", 15), bg='#e3bd4b', width=12)
    url_button.grid(column=2, row=2, pady=15)

    url_label.grid_forget()
    url_input.grid_forget()
    url_button.grid_forget()

    lbl_filler_similarity_score = tk.Label(text="Similarity score: ", font=("Times New Roman", 15), fg='#e3bd4b',
                                           bg='#2c2825')
    lbl_filler_similarity_score.grid(column=0, row=3, pady=15, padx=15)
    lbl_similarity_score = tk.Label(text="", font=("Times New Roman", 15), fg='#e3bd4b',
                                    bg='#2c2825')
    lbl_similarity_score.grid(column=1, row=3, pady=15)

    lbl_document = tk.Label(text="Selected document: ", font=(
        "Times New Roman", 15), fg='#e3bd4b', bg='#2c2825')
    lbl_document.grid(column=0, row=2, pady=15)
    lbl_file = tk.Label(text="", font=(
        "Times New Roman", 15), fg='#e3bd4b', bg='#2c2825')
    lbl_file.grid(column=1, row=2, pady=15)

    lbl_filler_similarity_score.grid_forget()
    lbl_similarity_score.grid_forget()
    lbl_document.grid_forget()
    lbl_file.grid_forget()


def feedback_button_clicked(event=None):
    wb.open(url="https://forms.office.com/e/rqrWyG31hr")


def website_comparison_clicked(event=None):
    url_label.grid(column=0, row=2, pady=15)
    url_input.grid(column=1, row=2, pady=15)
    url_button.grid(column=2, row=2, pady=15)
    comparison_selection_website.config(state='disabled')
    comparison_selection_document.config(state='disabled')
    url_button.bind("<Button-1>", url_button_clicked)


def zoom_button_clicked(event=None):
    global font_size
    font_size += 2
    keyword.config(font=("Times New Roman", font_size))

    # Update font size for inp_keyword
    keyword_entry.config(font=("Times New Roman", font_size))

    # Update font size for btn_keyword
    keyword_submit.config(font=("Times New Roman", font_size))

    # Update font size for lbl_choice
    comparison_selection_label.config(font=("Times New Roman", font_size))

    # Update font size for btn_website
    comparison_selection_website.config(font=("Times New Roman", font_size))

    comparison_selection_document.config(font=("Times New Roman", font_size))

    zoom_button.config(font=("Times New Roman", font_size))

    feedback_button.config(font=("Times New Roman", font_size))

    url_label.config(font=("Times New Roman", font_size))

    url_input.config(font=("Times New Roman", font_size))
    url_button.config(font=("Times New Roman", font_size))
    lbl_filler_similarity_score.config(font=("Times New Roman", font_size))
    lbl_similarity_score.config(font=("Times New Roman", font_size))

    lbl_document.config(font=("Times New Roman", font_size))
    lbl_file.config(font=("Times New Roman", font_size))


#  Button Handlers
def keyword_submit_clicked(event=None):
    submitted_keyword = keyword_entry.get().strip()

    if submitted_keyword:
        submitted_keyword = submitted_keyword.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{submitted_keyword}"
        response = requests.get(url)
        try:
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            textual_data = soup.get_text()
            with open(project_path + "\\filtered_wiki.txt", "w", encoding="utf-8") as wiki:
                wiki.write(textual_data)
        except requests.exceptions.HTTPError as e:
            print(f"Error occurred: {e}")


def remove_stopwords(file):
    """
    Remove stopwords from a text file

    Args:
        file (str): File name or file object to be processed

    Returns:
        list: List of filtered words
    """
    try:
        with open(file, "r", encoding="utf-8") as fh:
            content = fh.read()
            tokens = word_tokenize(content)
            filtered_words = [
                word for word in tokens if word not in stopwords.words("english")]
            return filtered_words
    except FileNotFoundError:
        print(f"Error: File {file} not found")
        return []
    except Exception as e:
        print(f"Error: {e}")


def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


filtered_words_i = remove_stopwords(project_path + "\\filtered_wiki.txt")
lemmatized_words_i = lemmatize_words(filtered_words_i)
filtered_words_ii = remove_stopwords(project_path + "\\filtered_website.txt")
lemmatized_words_ii = lemmatize_words(filtered_words_ii)


def calculate_cosine_similarity(words_i, words_ii):
    """
    Calculate cosine similarity between two sets of words

    Args:
        words_i (list): List of lemmatized words for the first set
        words_ii (list): List of lemmatized words for the second set

    Returns:
        float: Cosine similarity score
    """

    # Convert the lists of words into strings
    text_i = ' '.join(words_i)
    text_ii = ' '.join(words_ii)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Create TF-IDF vectorizer
    tfidf_matrix = vectorizer.fit_transform([text_i, text_ii])

    # Calculate cosine similarity between the TF-IDF vectors
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim[0][1]


def url_button_clicked(event=None):
    submitted_url = url_input.get()
    response = requests.get(submitted_url)
    try:
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        textual_data = soup.get_text()
        with open(project_path + "\\filtered_website.txt", "w", encoding='utf-8') as wiki:
            wiki.write(textual_data)
        lbl_filler_similarity_score.grid(column=0, row=3, pady=15, padx=15)
        lbl_similarity_score.grid(column=1, row=3, pady=15)

        document_cosine_similarity = calculate_cosine_similarity(
            lemmatized_words_i, lemmatized_words_ii)
        lbl_similarity_score.config(text=document_cosine_similarity)

        with (open(project_path + "\\results.txt", "w")) as result:
            result.write(str(document_cosine_similarity))
    except requests.exceptions.HTTPError as e:
        print(f"Error occurred: {e}")


def ButtonDocumentClicked(event=None):
    lbl_document.grid(column=0, row=2, pady=15)
    file = askopenfilename(filetypes=[("Text Files", "*.txt")])
    lbl_file.config(text=f"{file}")
    lbl_file.grid(column=1, row=2, pady=15)
    if file:
        # Perform content analysis on the selected document file
        filtered_words = remove_stopwords(file)
        lemmatized_words = lemmatize_words(filtered_words)
        document_cosine_similarity = calculate_cosine_similarity(
            lemmatized_words_i, lemmatized_words)
        lbl_similarity_score.config(text=document_cosine_similarity)
        with (open(project_path + "\\results.txt", "w")) as result:
            result.write(str(document_cosine_similarity))
        # Update the UI or perform other actions based on the analyzed content of the document
        # For example, you can display the cosine similarity score in a label or print it to the console
        print("Cosine Similarity Score:", document_cosine_similarity)

    comparison_selection_website.config(state='disabled')
    comparison_selection_document.config(state='disabled')

    lbl_filler_similarity_score.grid(column=0, row=3, pady=15, padx=15)
    lbl_similarity_score.grid(column=1, row=3, pady=15)

    class TestGuiConfig(unittest.TestCase):
        def test_gui_config(self):
            # Create the root object
            root = tk.Tk()
            # Call the gui_config function
            self.gui_config(root)
            # Check the properties of the root object
            self.assertEqual(
                root.title(), "Wikipedia Web Scraping And Document Comparison")
            self.assertEqual(root.geometry(), "1920x1080")
            self.assertEqual(root.cget("bg"), "#2c2825")


if __name__ == "__main__":
    unittest.main()
