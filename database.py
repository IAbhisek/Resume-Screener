import sqlite3
import os

class Database:
    def __init__(self, db_file="resume_screening.db"):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the database file path
        self.db_path = os.path.join(script_dir, db_file)
        # Connect to the database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Create resumes table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            name TEXT,
            email TEXT,
            phone TEXT,
            content TEXT NOT NULL
        )
        ''')
        
        # Create keywords table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            weight INTEGER DEFAULT 5
        )
        ''')
        
        # Create keyword_matches table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            keyword_id INTEGER,
            count INTEGER DEFAULT 0,
            FOREIGN KEY (resume_id) REFERENCES resumes (id) ON DELETE CASCADE,
            FOREIGN KEY (keyword_id) REFERENCES keywords (id) ON DELETE CASCADE
        )
        ''')
        
        self.conn.commit()
    
    def add_resume(self, filename, name, email, phone, content):
        """Add a new resume to the database"""
        self.cursor.execute('''
        INSERT INTO resumes (filename, name, email, phone, content)
        VALUES (?, ?, ?, ?, ?)
        ''', (filename, name, email, phone, content))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_keyword(self, keyword, weight=5):
        """Add a new keyword to the database"""
        try:
            self.cursor.execute('''
            INSERT INTO keywords (keyword, weight)
            VALUES (?, ?)
            ''', (keyword, weight))
            
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Keyword already exists, update weight instead
            self.cursor.execute('''
            UPDATE keywords
            SET weight = ?
            WHERE keyword = ?
            ''', (weight, keyword))
            
            self.conn.commit()
            
            # Get the ID of the existing keyword
            self.cursor.execute('''
            SELECT id FROM keywords WHERE keyword = ?
            ''', (keyword,))
            
            return self.cursor.fetchone()[0]
    
    def add_keyword_match(self, resume_id, keyword_id, count):
        """Add a keyword match for a resume"""
        self.cursor.execute('''
        INSERT INTO keyword_matches (resume_id, keyword_id, count)
        VALUES (?, ?, ?)
        ''', (resume_id, keyword_id, count))
        
        self.conn.commit()
    
    def get_all_resumes(self):
        """Get all resumes from the database"""
        self.cursor.execute('''
        SELECT id, filename, name, email, phone, content FROM resumes
        ORDER BY id DESC
        ''')
        
        return self.cursor.fetchall()
    
    def get_resume_by_id(self, resume_id):
        """Get a resume by its ID"""
        self.cursor.execute('''
        SELECT id, filename, name, email, phone, content FROM resumes
        WHERE id = ?
        ''', (resume_id,))
        
        return self.cursor.fetchone()
    
    def get_all_keywords(self):
        """Get all keywords from the database"""
        self.cursor.execute('''
        SELECT id, keyword, weight FROM keywords
        ORDER BY keyword
        ''')
        
        return self.cursor.fetchall()
    
    def delete_keyword(self, keyword_id):
        """Delete a keyword from the database"""
        self.cursor.execute('''
        DELETE FROM keywords WHERE id = ?
        ''', (keyword_id,))
        
        self.conn.commit()
    
    def get_keyword_matches(self, resume_id):
        """Get all keyword matches for a resume"""
        self.cursor.execute('''
        SELECT k.keyword, km.count, k.weight
        FROM keyword_matches km
        JOIN keywords k ON km.keyword_id = k.id
        WHERE km.resume_id = ?
        ORDER BY km.count * k.weight DESC
        ''', (resume_id,))
        
        return self.cursor.fetchall()
    
    def search_resumes(self, keywords):
        """Search resumes by keywords and return ranked results"""
        if not keywords:
            return []
        
        # Build query to calculate score based on keyword matches
        query = '''
        SELECT r.id, r.name, r.email, r.phone,
               SUM(CASE WHEN k.keyword IS NULL THEN 0 ELSE km.count * k.weight END) as score
        FROM resumes r
        LEFT JOIN keyword_matches km ON r.id = km.resume_id
        LEFT JOIN keywords k ON km.keyword_id = k.id
        '''        
        
        # Add content search for keywords not in the keywords table
        content_conditions = []
        for keyword in keywords:
            content_conditions.append(f"r.content LIKE '%{keyword}%'")
        
        if content_conditions:
            query += " WHERE " + " OR ".join(content_conditions)
        
        query += '''
        GROUP BY r.id
        ORDER BY score DESC
        '''
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def __del__(self):
        """Close the database connection when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()