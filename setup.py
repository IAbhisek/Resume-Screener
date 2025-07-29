from setuptools import setup, find_packages

setup(
    name="resume_screening_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "docx2txt>=0.8",
        "python-docx>=0.8.11",
    ],
    entry_points={
        'console_scripts': [
            'resume-screening=app:main',
        ],
    },
    author="Resume Screening App",
    author_email="example@example.com",
    description="A resume screening application to help filter and search through resumes",
    keywords="resume, screening, hr, recruitment",
    python_requires=">=3.6",
)