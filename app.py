import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import os
import re
import PyPDF2
import docx2txt
from database import Database

class ResumeScreeningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Screening Application")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.db = Database()
        self.db.create_tables()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frames
        self.top_frame = tk.Frame(self.root, pady=10)
        self.top_frame.pack(fill=tk.X)
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.upload_tab = tk.Frame(self.notebook)
        self.search_tab = tk.Frame(self.notebook)
        self.keywords_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.upload_tab, text="Upload Resumes")
        self.notebook.add(self.search_tab, text="Search Resumes")
        self.notebook.add(self.keywords_tab, text="Manage Keywords")
        
        # Setup each tab
        self.setup_upload_tab()
        self.setup_search_tab()
        self.setup_keywords_tab()
    
    def setup_upload_tab(self):
        # Frame for upload controls
        upload_frame = tk.Frame(self.upload_tab, pady=20)
        upload_frame.pack(fill=tk.X)
        
        # Upload button
        upload_btn = tk.Button(upload_frame, text="Upload Resumes", command=self.upload_resumes, 
                              width=15, height=2)
        upload_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(upload_frame, text="")
        self.status_label.pack(pady=5)
        
        # Frame for resume list
        list_frame = tk.Frame(self.upload_tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar and Listbox for uploaded resumes
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resume_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.resume_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resume_listbox.yview)
        
        # Bind double-click event to view resume
        self.resume_listbox.bind('<Double-1>', self.view_resume_details)
        
        # Load existing resumes
        self.load_resumes()
    
    def setup_search_tab(self):
        # Search controls frame
        search_controls = tk.Frame(self.search_tab, pady=20)
        search_controls.pack(fill=tk.X)
        
        # Search entry
        tk.Label(search_controls, text="Search Keywords:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_controls, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search button
        search_btn = tk.Button(search_controls, text="Search", command=self.search_resumes, width=10)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = tk.Frame(self.search_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for search results
        columns = ("id", "name", "email", "phone", "score")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Define headings
        self.results_tree.heading("id", text="ID")
        self.results_tree.heading("name", text="Name")
        self.results_tree.heading("email", text="Email")
        self.results_tree.heading("phone", text="Phone")
        self.results_tree.heading("score", text="Match Score")
        
        # Define columns width
        self.results_tree.column("id", width=50)
        self.results_tree.column("name", width=150)
        self.results_tree.column("email", width=200)
        self.results_tree.column("phone", width=150)
        self.results_tree.column("score", width=100)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event to view resume
        self.results_tree.bind('<Double-1>', self.view_search_result)
    
    def setup_keywords_tab(self):
        # Keywords management frame
        keywords_frame = tk.Frame(self.keywords_tab, pady=20)
        keywords_frame.pack(fill=tk.X)
        
        # Keyword entry
        tk.Label(keywords_frame, text="Keyword:").pack(side=tk.LEFT, padx=5)
        self.keyword_entry = tk.Entry(keywords_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        
        # Weight entry
        tk.Label(keywords_frame, text="Weight (1-10):").pack(side=tk.LEFT, padx=5)
        self.weight_entry = tk.Entry(keywords_frame, width=5)
        self.weight_entry.pack(side=tk.LEFT, padx=5)
        self.weight_entry.insert(0, "5")
        
        # Add button
        add_btn = tk.Button(keywords_frame, text="Add Keyword", command=self.add_keyword, width=12)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Keywords list frame
        list_frame = tk.Frame(self.keywords_tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for keywords
        columns = ("id", "keyword", "weight")
        self.keywords_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.keywords_tree.heading("id", text="ID")
        self.keywords_tree.heading("keyword", text="Keyword")
        self.keywords_tree.heading("weight", text="Weight")
        
        # Define columns width
        self.keywords_tree.column("id", width=50)
        self.keywords_tree.column("keyword", width=300)
        self.keywords_tree.column("weight", width=100)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.keywords_tree.yview)
        self.keywords_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.keywords_tree.pack(fill=tk.BOTH, expand=True)
        
        # Delete button
        delete_btn = tk.Button(list_frame, text="Delete Selected", command=self.delete_keyword)
        delete_btn.pack(pady=10)
        
        # Load existing keywords
        self.load_keywords()
    
    def upload_resumes(self):
        filetypes = [
            ("Resume files", "*.pdf;*.docx;*.doc;*.txt"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx;*.doc"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=filetypes
        )
        
        if not filenames:
            return
        
        processed = 0
        for filename in filenames:
            try:
                # Extract text from resume
                text = self.extract_text(filename)
                
                # Extract candidate information
                name = self.extract_name(text)
                email = self.extract_email(text)
                phone = self.extract_phone(text)
                
                # Save to database
                resume_id = self.db.add_resume(os.path.basename(filename), name, email, phone, text)
                
                # Process keywords
                self.process_keywords(resume_id, text)
                
                processed += 1
                
                # Add to listbox
                self.resume_listbox.insert(tk.END, f"{name} - {email}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {os.path.basename(filename)}: {str(e)}")
        
        self.status_label.config(text=f"Successfully processed {processed} resume(s)")
    
    def extract_text(self, filename):
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(filename)
        elif file_ext in ['.docx', '.doc']:
            return self.extract_text_from_docx(filename)
        elif file_ext == '.txt':
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def extract_text_from_pdf(self, filename):
        text = ""
        with open(filename, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def extract_text_from_docx(self, filename):
        return docx2txt.process(filename)
    
    def extract_name(self, text):
        # Simple name extraction - first line or first capitalized words
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and not re.match(r'^[\W_]+$', line):  # Not just special characters
                # Return first line that looks like a name (no special chars, reasonable length)
                if len(line) < 50 and not re.search(r'@|http|www|\.com', line.lower()):
                    return line
        
        # Fallback: look for capitalized words
        name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
        if name_match:
            return name_match.group(1)
        
        return "Unknown"
    
    def extract_email(self, text):
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            return email_match.group(0)
        return "Unknown"
    
    def extract_phone(self, text):
        # Look for phone numbers in various formats
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 123.456.7890
            r'\(\d{3}\)[-. ]?\d{3}[-.]?\d{4}',  # (123) 456-7890
            r'\+\d{1,2}[-. ]?\d{3}[-. ]?\d{3}[-. ]?\d{4}'  # +1 123-456-7890
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                return phone_match.group(0)
        
        return "Unknown"
    
    def process_keywords(self, resume_id, text):
        # Get all keywords
        keywords = self.db.get_all_keywords()
        
        for keyword_id, keyword, weight in keywords:
            # Count occurrences of keyword in text (case insensitive)
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
            
            if count > 0:
                # Add keyword match to database
                self.db.add_keyword_match(resume_id, keyword_id, count)
    
    def load_resumes(self):
        # Clear listbox
        self.resume_listbox.delete(0, tk.END)
        
        # Get all resumes from database
        resumes = self.db.get_all_resumes()
        
        # Add to listbox
        for resume in resumes:
            resume_id, filename, name, email, phone, _ = resume
            self.resume_listbox.insert(tk.END, f"{name} - {email}")
    
    def view_resume_details(self, event):
        # Get selected index
        selection = self.resume_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # Get resume from database
        resumes = self.db.get_all_resumes()
        if index >= len(resumes):
            return
        
        resume = resumes[index]
        resume_id, filename, name, email, phone, text = resume
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Resume: {name}")
        popup.geometry("600x500")
        
        # Resume details
        details_frame = tk.Frame(popup, pady=10)
        details_frame.pack(fill=tk.X)
        
        tk.Label(details_frame, text=f"Name: {name}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"Email: {email}").pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"Phone: {phone}").pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"File: {filename}").pack(anchor="w", padx=10)
        
        # Keywords matches
        tk.Label(details_frame, text="Keyword Matches:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        # Get keyword matches
        keyword_matches = self.db.get_keyword_matches(resume_id)
        
        keywords_text = ""
        for keyword, count, weight in keyword_matches:
            keywords_text += f"{keyword} (Count: {count}, Weight: {weight})\n"
        
        if not keywords_text:
            keywords_text = "No keyword matches found."
        
        keywords_label = tk.Label(details_frame, text=keywords_text, justify=tk.LEFT)
        keywords_label.pack(anchor="w", padx=10)
        
        # Resume text
        text_frame = tk.Frame(popup)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(text_frame, text="Resume Content:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Text widget with scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Make read-only
    
    def search_resumes(self):
        # Get search keywords
        search_text = self.search_entry.get().strip()
        if not search_text:
            messagebox.showinfo("Info", "Please enter search keywords")
            return
        
        # Split into individual keywords
        keywords = [k.strip() for k in search_text.split(',')]
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Search resumes
        results = self.db.search_resumes(keywords)
        
        # Display results
        for result in results:
            resume_id, name, email, phone, score = result
            self.results_tree.insert("", tk.END, values=(resume_id, name, email, phone, f"{score:.2f}"))
    
    def view_search_result(self, event):
        # Get selected item
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        resume_id = self.results_tree.item(item, "values")[0]
        
        # Get resume from database
        resume = self.db.get_resume_by_id(resume_id)
        if not resume:
            return
        
        _, filename, name, email, phone, text = resume
        
        # Create popup window (same as view_resume_details)
        popup = tk.Toplevel(self.root)
        popup.title(f"Resume: {name}")
        popup.geometry("600x500")
        
        # Resume details
        details_frame = tk.Frame(popup, pady=10)
        details_frame.pack(fill=tk.X)
        
        tk.Label(details_frame, text=f"Name: {name}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"Email: {email}").pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"Phone: {phone}").pack(anchor="w", padx=10)
        tk.Label(details_frame, text=f"File: {filename}").pack(anchor="w", padx=10)
        
        # Keywords matches
        tk.Label(details_frame, text="Keyword Matches:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        # Get keyword matches
        keyword_matches = self.db.get_keyword_matches(resume_id)
        
        keywords_text = ""
        for keyword, count, weight in keyword_matches:
            keywords_text += f"{keyword} (Count: {count}, Weight: {weight})\n"
        
        if not keywords_text:
            keywords_text = "No keyword matches found."
        
        keywords_label = tk.Label(details_frame, text=keywords_text, justify=tk.LEFT)
        keywords_label.pack(anchor="w", padx=10)
        
        # Resume text
        text_frame = tk.Frame(popup)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(text_frame, text="Resume Content:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Text widget with scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Make read-only
    
    def add_keyword(self):
        # Get keyword and weight
        keyword = self.keyword_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        
        if not keyword:
            messagebox.showinfo("Info", "Please enter a keyword")
            return
        
        try:
            weight = int(weight_str)
            if weight < 1 or weight > 10:
                raise ValueError("Weight must be between 1 and 10")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        # Add to database
        keyword_id = self.db.add_keyword(keyword, weight)
        
        # Add to treeview
        self.keywords_tree.insert("", tk.END, values=(keyword_id, keyword, weight))
        
        # Clear entries
        self.keyword_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, "5")
    
    def delete_keyword(self):
        # Get selected item
        selection = self.keywords_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a keyword to delete")
            return
        
        item = selection[0]
        keyword_id = self.keywords_tree.item(item, "values")[0]
        
        # Delete from database
        self.db.delete_keyword(keyword_id)
        
        # Delete from treeview
        self.keywords_tree.delete(item)
    
    def load_keywords(self):
        # Clear treeview
        for item in self.keywords_tree.get_children():
            self.keywords_tree.delete(item)
        
        # Get all keywords from database
        keywords = self.db.get_all_keywords()
        
        # Add to treeview
        for keyword in keywords:
            keyword_id, keyword_text, weight = keyword
            self.keywords_tree.insert("", tk.END, values=(keyword_id, keyword_text, weight))


def main():
    root = tk.Tk()
    app = ResumeScreeningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()