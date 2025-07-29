# Resume Screening Application

A Python application that helps you screen and search through resumes based on keywords and skills.

## Features

- Upload and process resumes in PDF, DOCX, and TXT formats
- Automatically extract candidate information (name, email, phone)
- Define and manage keywords with customizable weights
- Search resumes based on keywords
- View detailed resume information and content

## Requirements

- Python 3.6 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python app.py
```

### Upload Resumes

1. Go to the "Upload Resumes" tab
2. Click the "Upload Resumes" button
3. Select one or more resume files (PDF, DOCX, TXT)
4. The application will process the resumes and extract information

### Manage Keywords

1. Go to the "Manage Keywords" tab
2. Add keywords that are important for your screening process
3. Assign weights to keywords (1-10) based on their importance
4. Delete keywords you no longer need

### Search Resumes

1. Go to the "Search Resumes" tab
2. Enter keywords separated by commas
3. Click the "Search" button
4. View the results ranked by relevance
5. Double-click on a result to view the full resume details

## How It Works

- The application extracts text from resume files
- It attempts to identify candidate information using pattern matching
- Keywords are matched against resume content
- Search results are ranked based on keyword matches and their weights

## Database

The application uses SQLite to store:
- Resume information and content
- Keywords and their weights
- Keyword matches for each resume

The database file (resume_screening.db) is created in the application directory.

## License

This project is open source and available under the MIT License.