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
        self.root.title("AI Resume Screener By Abhishek")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Try to maximize window on startup
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass  # macOS or other
        
        # Enhanced modern dark theme colors
        self.colors = {
            'bg_primary': "#00030B", # Dark background
            'bg_secondary': '#161B22',# Card background
            'bg_tertiary': '#21262D',# Blue accent
            'accent_primary': "#3B44F6",    # New blue
            'accent_secondary': '#8B5CF6',  # New purple
            'text_primary': '#F0F6FC',
            'text_secondary': '#8B949E',
            'success': '#4ADE80',           # Bright green
            'warning': '#FACC15',           # Bright yellow
            'error': '#F87171',             # Soft red
            'hover_bg': '#30363D',
            'border': '#30363D',
            'gradient_start': '#1F2937',
            'gradient_end': '#111827',   # Gradient end
        }
        
        # Configure root window with enhanced styling
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Set minimum window size
        self.root.minsize(1200, 800)
        
        # Configure modern styles
        self.setup_styles()
        
        self.db = Database()
        self.db.create_tables()
        
        self.setup_ui()
    
    def setup_styles(self):
        """Configure modern TTK styles"""
        style = ttk.Style()
        
        # Configure notebook style
        style.theme_use('clam')
        style.configure('Modern.TNotebook', background=self.colors['bg_primary'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab', 
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Modern.TNotebook.Tab',  # Note the comma was incorrect here
                 background=[('selected', self.colors['accent_primary'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        # Configure treeview style
        style.configure('Modern.Treeview',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_tertiary'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['accent_primary'])])
    
    def create_modern_button(self, parent, text, command, bg_color=None, width=15, height=2):
        """Create a modern styled button"""
        if bg_color is None:
            bg_color = self.colors['accent_primary']
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat', borderwidth=0,
                       width=width, height=height,
                       cursor='hand2')
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening
        if color == self.colors['accent_primary']:
            return '#6CB6FF'
        elif color == self.colors['accent_secondary']:
            return '#8C4AED'
        elif color == self.colors['success']:
            return '#2EA043'
        elif color == self.colors['error']:
            return '#F85149'
        return color
    
    def create_modern_frame(self, parent, **kwargs):
        """Create a modern styled frame"""
        return tk.Frame(parent, bg=self.colors['bg_tertiary'], relief='flat', bd=1, **kwargs)
    
    def create_modern_label(self, parent, text, font_size=11, bold=False, color=None):
        """Create a modern styled label"""
        if color is None:
            color = self.colors['text_primary']
        
        font_weight = 'bold' if bold else 'normal'
        return tk.Label(parent, text=text,
                       bg=self.colors['bg_tertiary'], fg=color,
                       font=('Segoe UI', font_size, font_weight))
    
    def show_modern_error(self, title, message):
        """Show a modern error dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"❌ {title}")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Content frame
        content = self.create_modern_frame(dialog)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Error icon and title
        title_label = self.create_modern_label(content, f"❌ {title}", 16, True, self.colors['error'])
        title_label.pack(pady=(15, 0))
        
        # Message
        msg_label = self.create_modern_label(content, message, 11, color=self.colors['text_secondary'])
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = self.create_modern_button(content, "OK", dialog.destroy, self.colors['error'], 10, 1)
        ok_btn.pack(pady=10)
        
        dialog.wait_window()
    
    def show_modern_success(self, title, message):
        """Show a modern success dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"✅ {title}")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Content frame
        content = self.create_modern_frame(dialog)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Success icon and title
        title_label = self.create_modern_label(content, f"✅ {title}", 16, True, self.colors['success'])
        title_label.pack(pady=(20, 10))
        
        # Message
        msg_label = self.create_modern_label(content, message, 11, color=self.colors['text_secondary'])
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = self.create_modern_button(content, "OK", dialog.destroy, self.colors['success'], 10, 1)
        ok_btn.pack(pady=10)
        
        dialog.wait_window()
    
    def show_modern_warning(self, title, message):
        """Show a modern warning dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"⚠️ {title}")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Content frame
        content = self.create_modern_frame(dialog)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Warning icon and title
        title_label = self.create_modern_label(content, f"⚠️ {title}", 16, True, self.colors['warning'])
        title_label.pack(pady=(20, 10))
        
        # Message
        msg_label = self.create_modern_label(content, message, 11, color=self.colors['text_secondary'])
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = self.create_modern_button(content, "OK", dialog.destroy, self.colors['warning'], 10, 1)
        ok_btn.pack(pady=10)
        
        dialog.wait_window()
    
    def show_modern_confirm(self, title, message):
        """Show a modern confirmation dialog"""
        result = [False]  # Use list to modify from nested function
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"❓ {title}")
        dialog.geometry("450x220")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # Content frame
        content = self.create_modern_frame(dialog)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Question icon and title
        title_label = self.create_modern_label(content, f"❓ {title}", 16, True, self.colors['accent_primary'])
        title_label.pack(pady=(20, 10))
        
        # Message
        msg_label = self.create_modern_label(content, message, 11, color=self.colors['text_secondary'])
        msg_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(content, bg=self.colors['bg_tertiary'])
        buttons_frame.pack(pady=10)
        
        # Yes and No buttons
        yes_btn = self.create_modern_button(buttons_frame, "✅ Yes", on_yes, self.colors['success'], 10, 1)
        yes_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        no_btn = self.create_modern_button(buttons_frame, "❌ No", on_no, self.colors['error'], 10, 1)
        no_btn.pack(side=tk.LEFT)
        
        dialog.wait_window()
        return result[0]
    
    def setup_ui(self):
        # Create enhanced header with gradient-like effect
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=120)  # Increased height
        header_frame.pack(fill=tk.X, padx=25, pady=(25, 0))
        header_frame.pack_propagate(False)
        
        # Main title section
        title_section = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_section.pack(side=tk.LEFT, fill=tk.Y)
        
        # App title with enhanced styling
        title_label = tk.Label(title_section, text=" AI RESUME SCREENING SYSTEM",
                              bg=self.colors['bg_primary'], fg=self.colors['accent_primary'],
                              font=('Segoe UI', 28, 'bold'))
        title_label.pack(anchor='w', pady=(20, 2))  # Reduced top padding
        
        # Enhanced subtitle with version info
        subtitle_label = tk.Label(title_section, text="Intelligent Resume Screening Platform v1.0",
                                 bg=self.colors['bg_primary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 13, 'bold'))
        subtitle_label.pack(anchor='w', pady=(0, 10))  # Added bottom padding
        
        # Status indicator section
        status_section = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        status_section.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))
        
        # System status indicator
        status_frame = tk.Frame(status_section, bg=self.colors['bg_tertiary'], relief='flat', bd=1)
        status_frame.pack(pady=30)
        
        status_label = tk.Label(status_frame, text="🟢 SYSTEM ONLINE",
                               bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                               font=('Segoe UI', 11, 'bold'))
        status_label.pack(padx=15, pady=8)
        
        # Enhanced main container with better spacing
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Create enhanced notebook for tabs
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs with modern frames and enhanced spacing
        self.upload_tab = self.create_modern_frame(self.notebook)
        self.search_tab = self.create_modern_frame(self.notebook)
        self.keywords_tab = self.create_modern_frame(self.notebook)
        
        # Add tabs with enhanced icons and descriptions
        self.notebook.add(self.upload_tab, text="📁 Upload & Process")
        self.notebook.add(self.search_tab, text="🔍 Smart Search")
        self.notebook.add(self.keywords_tab, text="⚙️ Keyword Manager")
        
        # Setup each tab with enhanced functionality
        self.setup_upload_tab()
        self.setup_search_tab()
        self.setup_keywords_tab()
    
    def setup_upload_tab(self):
        # Header section
        header_section = self.create_modern_frame(self.upload_tab)
        header_section.pack(fill=tk.X, padx=30, pady=30)
        
        # Title and description
        title = self.create_modern_label(header_section, "📁 Upload & Process Resumes", 18, True)
        title.pack(anchor='w', padx=20, pady=(20, 5))
        
        desc = self.create_modern_label(header_section, "Upload resume files in PDF, DOCX, or TXT format for intelligent processing", 12, color=self.colors['text_secondary'])
        desc.pack(anchor='w', padx=20, pady=(0, 20))
        
        # Upload controls section
        controls_section = self.create_modern_frame(self.upload_tab)
        controls_section.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Upload button with modern styling
        button_frame = tk.Frame(controls_section, bg=self.colors['bg_tertiary'])
        button_frame.pack(pady=20)
        
        upload_btn = self.create_modern_button(button_frame, "📤 Upload Resumes", self.upload_resumes, width=20, height=2)
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = self.create_modern_button(button_frame, "🗑️ Delete Resume", self.delete_resume, 
                                             bg_color=self.colors['error'], width=20, height=2)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label with modern styling
        self.status_label = self.create_modern_label(controls_section, "", color=self.colors['success'])
        self.status_label.pack(pady=(0, 20))
        
        # Resume list section
        list_section = self.create_modern_frame(self.upload_tab)
        list_section.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Section title
        list_title = self.create_modern_label(list_section, "📋 Uploaded Resumes", 14, True)
        list_title.pack(anchor='w', padx=20, pady=(20, 10))
        
        # Listbox container
        listbox_container = tk.Frame(list_section, bg=self.colors['bg_tertiary'])
        listbox_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Modern scrollbar and listbox
        scrollbar = tk.Scrollbar(listbox_container, bg=self.colors['bg_secondary'], troughcolor=self.colors['bg_primary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        self.resume_listbox = tk.Listbox(listbox_container, 
                                        yscrollcommand=scrollbar.set,
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_primary'],
                                        selectbackground=self.colors['accent_primary'],
                                        selectforeground=self.colors['text_primary'],
                                        font=('Segoe UI', 11),
                                        relief='flat',
                                        borderwidth=0,
                                        activestyle='none')
        self.resume_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resume_listbox.yview)
        
        # Bind double-click event
        self.resume_listbox.bind('<Double-1>', self.view_resume_details)
        
        # Load existing resumes
        self.load_resumes()
    
    def setup_search_tab(self):
        # Header section
        header_section = self.create_modern_frame(self.search_tab)
        header_section.pack(fill=tk.X, padx=30, pady=30)
        
        # Title and description
        title = self.create_modern_label(header_section, "🔍 Smart Resume Search", 18, True)
        title.pack(anchor='w', padx=20, pady=(20, 5))
        
        desc = self.create_modern_label(header_section, "Search through resumes using AI-powered keyword matching and relevance scoring", 12, color=self.colors['text_secondary'])
        desc.pack(anchor='w', padx=20, pady=(0, 20))
        
        # Search controls section
        search_section = self.create_modern_frame(self.search_tab)
        search_section.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Search container
        search_container = tk.Frame(search_section, bg=self.colors['bg_tertiary'])
        search_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Search label
        search_label = self.create_modern_label(search_container, "🔎 Enter Keywords (comma-separated):", 12, True)
        search_label.pack(anchor='w', pady=(0, 10))
        
        # Search input frame
        input_frame = tk.Frame(search_container, bg=self.colors['bg_tertiary'])
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Modern search entry
        self.search_entry = tk.Entry(input_frame,
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12),
                                    relief='flat',
                                    borderwidth=2,
                                    insertbackground=self.colors['text_primary'])
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        # Modern search button
        search_btn = self.create_modern_button(input_frame, "🚀 Search", self.search_resumes, width=12, height=1)
        search_btn.pack(side=tk.RIGHT)
        
        # Results section
        results_section = self.create_modern_frame(self.search_tab)
        results_section.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Results title
        results_title = self.create_modern_label(results_section, "📊 Search Results", 14, True)
        results_title.pack(anchor='w', padx=20, pady=(20, 10))
        
        # Treeview container
        tree_container = tk.Frame(results_section, bg=self.colors['bg_tertiary'])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create modern treeview
        columns = ("id", "name", "email", "phone", "score")
        self.results_tree = ttk.Treeview(tree_container, columns=columns, show="headings", style='Modern.Treeview')
        
        # Define headings with icons
        self.results_tree.heading("id", text="🆔 ID")
        self.results_tree.heading("name", text="👤 Name")
        self.results_tree.heading("email", text="📧 Email")
        self.results_tree.heading("phone", text="📱 Phone")
        self.results_tree.heading("score", text="⭐ Score")
        
        # Define columns width
        self.results_tree.column("id", width=80)
        self.results_tree.column("name", width=180)
        self.results_tree.column("email", width=250)
        self.results_tree.column("phone", width=150)
        self.results_tree.column("score", width=120)
        
        # Add modern scrollbar
        scrollbar = tk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.results_tree.yview,
                               bg=self.colors['bg_secondary'], troughcolor=self.colors['bg_primary'])
        self.results_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event
        self.results_tree.bind('<Double-1>', self.view_search_result)
    
    def setup_keywords_tab(self):
        # Header section
        header_section = self.create_modern_frame(self.keywords_tab)
        header_section.pack(fill=tk.X, padx=30, pady=30)
        
        # Title and description
        title = self.create_modern_label(header_section, "⚙️ Keyword Management", 18, True)
        title.pack(anchor='w', padx=20, pady=(20, 5))
        
        desc = self.create_modern_label(header_section, "Define and manage keywords with custom weights for intelligent resume screening", 12, color=self.colors['text_secondary'])
        desc.pack(anchor='w', padx=20, pady=(0, 20))
        
        # Add keyword section
        add_section = self.create_modern_frame(self.keywords_tab)
        add_section.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Add keyword container
        add_container = tk.Frame(add_section, bg=self.colors['bg_tertiary'])
        add_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Add keyword title
        add_title = self.create_modern_label(add_container, "➕ Add New Keyword", 14, True)
        add_title.pack(anchor='w', pady=(0, 15))
        
        # Input frame
        input_frame = tk.Frame(add_container, bg=self.colors['bg_tertiary'])
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Keyword input
        keyword_label = self.create_modern_label(input_frame, "🏷️ Keyword:", 11, True)
        keyword_label.pack(anchor='w', pady=(0, 5))
        
        self.keyword_entry = tk.Entry(input_frame,
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     font=('Segoe UI', 11),
                                     relief='flat',
                                     borderwidth=2,
                                     insertbackground=self.colors['text_primary'])
        self.keyword_entry.pack(fill=tk.X, ipady=6, pady=(0, 15))
        
        # Weight input
        weight_label = self.create_modern_label(input_frame, "⚖️ Weight (1-10):", 11, True)
        weight_label.pack(anchor='w', pady=(0, 5))
        
        self.weight_entry = tk.Entry(input_frame,
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 11),
                                    relief='flat',
                                    borderwidth=2,
                                    width=10,
                                    insertbackground=self.colors['text_primary'])
        self.weight_entry.pack(anchor='w', ipady=6, pady=(0, 15))
        self.weight_entry.insert(0, "5")
        
        # Buttons frame
        buttons_frame = tk.Frame(input_frame, bg=self.colors['bg_tertiary'])
        buttons_frame.pack(fill=tk.X)
        
        # Add button
        add_btn = self.create_modern_button(buttons_frame, "✅ Add Keyword", self.add_keyword, width=15, height=1)
        add_btn.pack(side=tk.LEFT)
        
        # Keywords list section
        list_section = self.create_modern_frame(self.keywords_tab)
        list_section.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # List title
        list_title = self.create_modern_label(list_section, "📝 Current Keywords", 14, True)
        list_title.pack(anchor='w', padx=20, pady=(20, 10))
        
        # Treeview container
        tree_container = tk.Frame(list_section, bg=self.colors['bg_tertiary'])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create modern treeview for keywords
        columns = ("id", "keyword", "weight")
        self.keywords_tree = ttk.Treeview(tree_container, columns=columns, show="headings", style='Modern.Treeview')
        
        # Define headings with icons
        self.keywords_tree.heading("id", text="🆔 ID")
        self.keywords_tree.heading("keyword", text="🏷️ Keyword")
        self.keywords_tree.heading("weight", text="⚖️ Weight")
        
        # Define columns width
        self.keywords_tree.column("id", width=80)
        self.keywords_tree.column("keyword", width=400)
        self.keywords_tree.column("weight", width=120)
        
        # Add modern scrollbar
        scrollbar = tk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.keywords_tree.yview,
                               bg=self.colors['bg_secondary'], troughcolor=self.colors['bg_primary'])
        self.keywords_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.keywords_tree.pack(fill=tk.BOTH, expand=True)
        
        # Delete button
        delete_btn = self.create_modern_button(tree_container, "🗑️ Delete Selected", self.delete_keyword, 
                                              bg_color=self.colors['error'], width=18, height=1)
        delete_btn.pack(pady=15)
        
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
            title="🚀 Select Resume Files - AI Resume Screening Hub",
            filetypes=filetypes
        )
        
        if not filenames:
            self.status_label.config(text="⚠️ No files selected", fg=self.colors['warning'])
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
                
            except Exception as e:
                self.show_modern_error("Processing Error", f"Failed to process {os.path.basename(filename)}: {str(e)}")
        
        if processed > 0:
            self.status_label.config(text=f"✅ Successfully processed {processed} resume(s)", fg=self.colors['success'])
            self.load_resumes()
        else:
            self.status_label.config(text="❌ No resumes were processed", fg=self.colors['error'])
    
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
        
        # Add to listbox with modern formatting
        for resume in resumes:
            resume_id, filename, name, email, phone, _ = resume
            display_text = f"📄 {name} | 📧 {email} | 📱 {phone}"
            self.resume_listbox.insert(tk.END, display_text)
    
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
        
        # Create modern popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"📄 Resume Details - {name}")
        popup.geometry("800x600")
        popup.configure(bg=self.colors['bg_primary'])
        
        # Header
        header = tk.Frame(popup, bg=self.colors['bg_primary'], height=80)
        header.pack(fill=tk.X, padx=20, pady=(20, 0))
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=f"📄 {filename}",
                              bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                              font=('Segoe UI', 18, 'bold'))
        title_label.pack(side=tk.LEFT, pady=20)
        
        # Content frame
        content_frame = self.create_modern_frame(popup)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Info section
        info_frame = tk.Frame(content_frame, bg=self.colors['bg_tertiary'])
        info_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        info_title = self.create_modern_label(info_frame, "👤 Candidate Information", 14, True)
        info_title.pack(anchor='w', padx=20, pady=(15, 10))
        
        info_text = f"👤 Name: {name}\n📧 Email: {email}\n📱 Phone: {phone}"
        info_label = self.create_modern_label(info_frame, info_text, 11, color=self.colors['text_secondary'])
        info_label.pack(anchor='w', padx=20, pady=(0, 10))
        
        # Keywords section
        keywords_title = self.create_modern_label(info_frame, "🏷️ Keyword Matches", 12, True)
        keywords_title.pack(anchor='w', padx=20, pady=(10, 5))
        
        # Get keyword matches
        keyword_matches = self.db.get_keyword_matches(resume_id)
        
        if keyword_matches:
            keywords_text = ""
            for keyword, count, weight in keyword_matches:
                keywords_text += f"• {keyword} (Count: {count}, Weight: {weight})\n"
        else:
            keywords_text = "No keyword matches found."
        
        keywords_label = self.create_modern_label(info_frame, keywords_text, 10, color=self.colors['text_secondary'])
        keywords_label.pack(anchor='w', padx=20, pady=(0, 15))
        
        # Content section
        content_title = self.create_modern_label(content_frame, "📝 Resume Content", 14, True)
        content_title.pack(anchor='w', padx=20, pady=(10, 5))
        
        # Text widget container
        text_container = tk.Frame(content_frame, bg=self.colors['bg_tertiary'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Modern scrollbar and text widget
        scrollbar = tk.Scrollbar(text_container, bg=self.colors['bg_secondary'], troughcolor=self.colors['bg_primary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        text_widget = tk.Text(text_container, 
                             yscrollcommand=scrollbar.set, 
                             wrap=tk.WORD,
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 10),
                             relief='flat',
                             borderwidth=0,
                             insertbackground=self.colors['text_primary'])
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
    
    def search_resumes(self):
        # Get search keywords
        search_text = self.search_entry.get().strip()
        if not search_text:
            self.show_modern_warning("⚠️ Search Required", "Please enter keywords to search for resumes.")
            return
        
        # Split into individual keywords
        keywords = [k.strip() for k in search_text.split(',')]
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Search resumes
        results = self.db.search_resumes(keywords)
        
        # Display results with enhanced feedback
        if results:
            for result in results:
                resume_id, name, email, phone, score = result
                self.results_tree.insert("", tk.END, values=(resume_id, name, email, phone, f"{score:.2f}"))
        else:
            self.show_modern_warning("🔍 No Results", "No resumes found matching the specified keywords.")
    
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
            self.show_modern_warning("⚠️ Input Required", "Please enter a keyword before adding.")
            return
        
        try:
            weight = int(weight_str)
            if weight < 1 or weight > 10:
                raise ValueError("Weight must be between 1 and 10")
        except ValueError as e:
            self.show_modern_error("❌ Invalid Input", str(e))
            return
        
        # Add to database
        keyword_id = self.db.add_keyword(keyword, weight)
        
        # Add to treeview
        self.keywords_tree.insert("", tk.END, values=(keyword_id, keyword, weight))
        
        # Clear entries
        self.keyword_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, "5")
        
        self.show_modern_success("✅ Keyword Added", f"Keyword '{keyword}' with weight {weight} added successfully!")
    
    def delete_keyword(self):
        # Get selected item
        selection = self.keywords_tree.selection()
        if not selection:
            self.show_modern_warning("⚠️ Selection Required", "Please select a keyword to delete.")
            return
        
        item = selection[0]
        keyword_values = self.keywords_tree.item(item, "values")
        keyword_id = keyword_values[0]
        keyword_text = keyword_values[1]
        
        # Confirm deletion
        if self.show_modern_confirm("🗑️ Confirm Deletion", f"Are you sure you want to delete '{keyword_text}'?"):
            # Delete from database
            self.db.delete_keyword(keyword_id)
            
            # Delete from treeview
            self.keywords_tree.delete(item)
            
            self.show_modern_success("✅ Keyword Deleted", f"Keyword '{keyword_text}' deleted successfully!")
    
    def delete_resume(self):
        """Delete selected resume"""
        # Get selected resume
        selection = self.resume_listbox.curselection()
        if not selection:
            self.show_modern_warning("⚠️ Selection Required", "Please select a resume to delete.")
            return
        
        index = selection[0]
        
        # Get resume from database
        resumes = self.db.get_all_resumes()
        if index >= len(resumes):
            return
        
        resume = resumes[index]
        resume_id, filename, name, email, phone, _ = resume
        
        # Confirm deletion
        if self.show_modern_confirm("🗑️ Confirm Deletion", 
                                  f"Are you sure you want to delete the resume for {name}?\nThis action cannot be undone."):
            # Delete from database
            if self.db.delete_resume(resume_id):
                # Update listbox
                self.load_resumes()
                self.show_modern_success("✅ Resume Deleted", 
                                       f"Resume for {name} has been successfully deleted.")
            else:
                self.show_modern_error("❌ Deletion Error", 
                                     f"Failed to delete resume for {name}.")
    
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