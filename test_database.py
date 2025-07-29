import os
import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a test database file
        self.test_db_file = "test_resume_screening.db"
        # Remove the test database file if it exists
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
        # Create a new database instance
        self.db = Database(self.test_db_file)
        self.db.create_tables()
    
    def tearDown(self):
        # Close the database connection
        del self.db
        # Remove the test database file
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    
    def test_add_resume(self):
        # Test adding a resume
        resume_id = self.db.add_resume(
            "test_resume.pdf",
            "John Doe",
            "john.doe@example.com",
            "123-456-7890",
            "This is a test resume content."
        )
        
        # Check if the resume was added
        self.assertIsNotNone(resume_id)
        self.assertGreater(resume_id, 0)
        
        # Get the resume and check its values
        resume = self.db.get_resume_by_id(resume_id)
        self.assertIsNotNone(resume)
        self.assertEqual(resume[1], "test_resume.pdf")
        self.assertEqual(resume[2], "John Doe")
        self.assertEqual(resume[3], "john.doe@example.com")
        self.assertEqual(resume[4], "123-456-7890")
        self.assertEqual(resume[5], "This is a test resume content.")
    
    def test_add_keyword(self):
        # Test adding a keyword
        keyword_id = self.db.add_keyword("Python", 8)
        
        # Check if the keyword was added
        self.assertIsNotNone(keyword_id)
        self.assertGreater(keyword_id, 0)
        
        # Get all keywords and check if the added keyword is there
        keywords = self.db.get_all_keywords()
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0][1], "Python")
        self.assertEqual(keywords[0][2], 8)
    
    def test_add_keyword_match(self):
        # Add a resume
        resume_id = self.db.add_resume(
            "test_resume.pdf",
            "John Doe",
            "john.doe@example.com",
            "123-456-7890",
            "This is a test resume with Python skills."
        )
        
        # Add a keyword
        keyword_id = self.db.add_keyword("Python", 8)
        
        # Add a keyword match
        self.db.add_keyword_match(resume_id, keyword_id, 1)
        
        # Get keyword matches for the resume
        matches = self.db.get_keyword_matches(resume_id)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Python")
        self.assertEqual(matches[0][1], 1)  # count
        self.assertEqual(matches[0][2], 8)  # weight
    
    def test_search_resumes(self):
        # Add resumes with different content
        resume1_id = self.db.add_resume(
            "resume1.pdf",
            "John Doe",
            "john.doe@example.com",
            "123-456-7890",
            "Experienced Python developer with Django and Flask."
        )
        
        resume2_id = self.db.add_resume(
            "resume2.pdf",
            "Jane Smith",
            "jane.smith@example.com",
            "987-654-3210",
            "Java developer with Spring Boot experience."
        )
        
        # Add keywords
        python_id = self.db.add_keyword("Python", 8)
        django_id = self.db.add_keyword("Django", 7)
        java_id = self.db.add_keyword("Java", 6)
        
        # Add keyword matches
        self.db.add_keyword_match(resume1_id, python_id, 1)
        self.db.add_keyword_match(resume1_id, django_id, 1)
        self.db.add_keyword_match(resume2_id, java_id, 1)
        
        # Search for Python
        results = self.db.search_resumes(["Python"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "John Doe")
        
        # Search for Java
        results = self.db.search_resumes(["Java"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Jane Smith")
        
        # Search for both Python and Java
        results = self.db.search_resumes(["Python", "Java"])
        self.assertEqual(len(results), 2)

if __name__ == "__main__":
    unittest.main()