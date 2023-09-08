import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Define the file paths for the CSV files
books_csv_path = 'data/books.csv'
papers_csv_path = 'data/papers.csv'

# Load existing data from CSV files
def load_data_from_csv(file_path):
    data = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass  
    return data

# Save data to CSV files
def save_data_to_csv(data, file_path):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Initialize data from CSV files
library = {
    'books': load_data_from_csv(books_csv_path),
    'papers': load_data_from_csv(papers_csv_path),
}

@app.route('/')
def index():
    return render_template('index.html', library=library)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    entry_type = request.form['entry_type']
    author = request.form['author']
    year = request.form['year']
    title = request.form['title']
    date_read = datetime.strptime(request.form['date_read'], '%Y-%m-%d')
    summary = request.form.get('summary', '')

    if entry_type == 'book':
        publisher = request.form.get('publisher', '')
        entry = {
            'author': author,
            'year': year,
            'title': title,
            'publisher': publisher,
            'date_read': date_read,
            'summary': summary,
        }
        library['books'].append(entry)
        library['books'].sort(key=lambda x: x['date_read'], reverse=True)
        save_data_to_csv(library['books'], books_csv_path)
    elif entry_type == 'paper':
        publisher = request.form.get('publisher', '')
        entry = {
            'author': author,
            'year': year,
            'title': title,
            'publisher': publisher,
            'date_read': date_read,
            'summary': summary,
        }
        library['papers'].append(entry)
        library['papers'].sort(key=lambda x: x['date_read'], reverse=True)
        save_data_to_csv(library['papers'], papers_csv_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
