import os
from database import Database

def example_usage():
    print("Resume Screening App - Example Usage")
    print("-" * 40)
    
    # Initialize database
    db = Database("example_resume_screening.db")
    db.create_tables()
    
    # Add some keywords
    print("Adding keywords...")
    keywords = [
        ("Python", 8),
        ("Java", 7),
        ("SQL", 6),
        ("JavaScript", 6),
        ("Machine Learning", 9),
        ("Data Analysis", 8),
        ("AWS", 7),
        ("Docker", 7),
        ("React", 6),
        ("Node.js", 6)
    ]
    
    for keyword, weight in keywords:
        db.add_keyword(keyword, weight)
        print(f"  Added: {keyword} (weight: {weight})")
    
    print("\nAdding example resumes...")
    
    # Example resume 1
    resume1_content = """
    John Smith
    john.smith@example.com
    (123) 456-7890
    
    SUMMARY
    Experienced software engineer with 5 years of experience in Python development,
    machine learning, and data analysis. Proficient in SQL and AWS cloud services.
    
    SKILLS
    - Python (Django, Flask, NumPy, Pandas)
    - Machine Learning (TensorFlow, scikit-learn)
    - SQL (PostgreSQL, MySQL)
    - AWS (EC2, S3, Lambda)
    - Data Analysis and Visualization
    
    EXPERIENCE
    Senior Python Developer - ABC Tech (2020-Present)
    - Developed machine learning models for predictive analytics
    - Created data pipelines using Python and AWS services
    - Implemented SQL databases for efficient data storage
    
    Data Analyst - XYZ Corp (2018-2020)
    - Performed data analysis using Python and SQL
    - Created visualizations and reports for stakeholders
    """
    
    resume1_id = db.add_resume(
        "john_smith_resume.pdf",
        "John Smith",
        "john.smith@example.com",
        "(123) 456-7890",
        resume1_content
    )
    print(f"  Added: John Smith's resume")
    
    # Example resume 2
    resume2_content = """
    Jane Doe
    jane.doe@example.com
    (987) 654-3210
    
    SUMMARY
    Full-stack developer with expertise in JavaScript, React, and Node.js.
    Experience with Docker containerization and cloud deployment.
    
    SKILLS
    - JavaScript (React, Vue.js)
    - Node.js, Express
    - Docker, Kubernetes
    - AWS, Azure
    - HTML/CSS, Responsive Design
    
    EXPERIENCE
    Senior Frontend Developer - Web Solutions Inc (2019-Present)
    - Developed responsive web applications using React
    - Implemented CI/CD pipelines with Docker
    - Created RESTful APIs with Node.js and Express
    
    Web Developer - Digital Agency (2017-2019)
    - Built interactive websites using JavaScript and HTML/CSS
    - Worked with various CMS platforms
    """
    
    resume2_id = db.add_resume(
        "jane_doe_resume.pdf",
        "Jane Doe",
        "jane.doe@example.com",
        "(987) 654-3210",
        resume2_content
    )
    print(f"  Added: Jane Doe's resume")
    
    # Process keywords for the resumes
    print("\nProcessing keywords for resumes...")
    
    # Get all keywords
    all_keywords = db.get_all_keywords()
    
    # Process resume 1
    for keyword_id, keyword, weight in all_keywords:
        # Count occurrences (case insensitive)
        count = resume1_content.lower().count(keyword.lower())
        if count > 0:
            db.add_keyword_match(resume1_id, keyword_id, count)
            print(f"  John Smith's resume: '{keyword}' found {count} times")
    
    # Process resume 2
    for keyword_id, keyword, weight in all_keywords:
        # Count occurrences (case insensitive)
        count = resume2_content.lower().count(keyword.lower())
        if count > 0:
            db.add_keyword_match(resume2_id, keyword_id, count)
            print(f"  Jane Doe's resume: '{keyword}' found {count} times")
    
    # Search examples
    print("\nSearch Examples:")
    
    # Search for Python skills
    print("\nSearching for 'Python' skills:")
    results = db.search_resumes(["Python"])
    for resume_id, name, email, phone, score in results:
        print(f"  {name} (Score: {score})")
    
    # Search for JavaScript skills
    print("\nSearching for 'JavaScript' skills:")
    results = db.search_resumes(["JavaScript"])
    for resume_id, name, email, phone, score in results:
        print(f"  {name} (Score: {score})")
    
    # Search for multiple skills
    print("\nSearching for 'Python, JavaScript, AWS' skills:")
    results = db.search_resumes(["Python", "JavaScript", "AWS"])
    for resume_id, name, email, phone, score in results:
        print(f"  {name} (Score: {score})")
    
    print("\nExample completed. Check 'example_resume_screening.db' for the database.")

if __name__ == "__main__":
    example_usage()