import streamlit as st
import pandas as pd
import spacy
import re
from PyPDF2 import PdfReader
from fuzzywuzzy import fuzz
import time
import os

# Load the skills list for matching using keyword-based and fuzzy matching techniques
skills_df = pd.read_csv("./dataset/skills.csv")
skills_list = set(skills_df['technical skills'].dropna().str.lower().tolist())

# Initialize spaCy model for Named Entity Recognition (NER) to extract entities like universities and degrees
nlp = spacy.load("en_core_web_sm")

# Define regex patterns for structured information extraction (email, phone, GitHub URLs)
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}"
phone_pattern = r"(?:\(?\d{2,3}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}[\s-]?\d{4}"
github_pattern = r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+"

# Define regex patterns for common degree types to assist in degree extraction
degree_keywords = [
    r"\bbachelor\b", r"\bmaster\b", r"\bphd\b", r"\bdoctorate\b", r"\bassociate\b", r"\bdiploma\b", r"\bengineer\b",
    r"\bb\.e\.\b", r"\bb\.tech\b", r"\bm\.tech\b", r"\bm\.sc\b", r"\bm\.eng\b", r"\bb\.sc\b", r"\bb\.eng\b", 
    r"\bph\.d\b", r"\bmsc\b", r"\bbachelor's\b", r"\bmaster's\b",r"b.sc"
]

# PDF Text Extraction with Error Handling
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text, len(reader.pages)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return "", 0

# Resume Parsing Function: Utilizes NLP techniques and regex to extract information
def parse_resume(text, page_count):
    parsed_data = {
        "name": None,
        "email": [],
        "phone": [],
        "github": None,
        "university": [],
        "degree": [],
        "skills": [],
        "no_of_pages": page_count
    }

    # Extract Name: Heuristic-based extraction (assumes the name is the first non-empty line)
    lines = text.splitlines()
    for line in lines:
        if line.strip():
            parsed_data["name"] = line.strip().title()
            break

    # Extract Email, Phone, GitHub using regex-based matching for structured data
    parsed_data["email"] = re.findall(email_pattern, text)
    parsed_data["phone"] = list(set(re.findall(phone_pattern, text)))
    github_match = re.search(github_pattern, text)
    parsed_data["github"] = github_match.group(0) if github_match else "Not Found"

    # Extract University/College Names using spaCy NER for organization entities
    doc = nlp(text.lower())
    parsed_data["university"] = [
        ent.text.title() for ent in doc.ents if ent.label_ == "ORG"
        and any(keyword in ent.text.lower() for keyword in ["university", "college", "institute", "academy"])
    ]

    # Extract Degree using flexible regex pattern matching for common degree types
    parsed_data["degree"] = []
    for degree_pattern in degree_keywords:
        match = re.search(degree_pattern, text, re.IGNORECASE)
        if match:
            parsed_data["degree"].append(match.group(0).capitalize())
    if not parsed_data["degree"]:
        parsed_data["degree"] = ["Not Found"]

    # Skill extraction using keyword-based matching and fuzzy matching for similar terms
    found_skills = set()
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)
        else:
            # Fuzzy matching applied to handle slight variations in skill names
            for word in text.split():
                if fuzz.ratio(skill, word) > 80:
                    found_skills.add(skill)
                    break
    parsed_data["skills"] = list(found_skills)

    # Handle missing data entries by assigning default "Not Found" value
    for key in ["name", "email", "phone", "university", "degree", "skills"]:
        if not parsed_data[key]:
            parsed_data[key] = ["Not Found"] if isinstance(parsed_data[key], list) else "Not Found"

    return parsed_data

# Function to rank resumes based on skill matching using a simple scoring mechanism
def rank_resumes(resumes_data, required_skills):
    ranking = []
    for resume in resumes_data:
        skill_match_count = sum(1 for skill in resume["skills"] if skill in required_skills)
        ranking.append((resume["name"], skill_match_count))
    
    # Sort resumes based on skill match count in descending order
    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
    return ranking

# Streamlit UI for uploading resumes and entering required skills
def main():
    st.title("Resume Parser and Ranker")

    # Upload Resumes (PDFs)
    uploaded_files = st.file_uploader("Upload Resumes", type="pdf", accept_multiple_files=True)
    
    # Input Required Skills (comma-separated)
    required_skills_input = st.text_area("Enter required skills (comma separated)")
    
    # Submit Button to trigger processing and ranking
    if st.button("Submit", type='primary'):
        if uploaded_files and required_skills_input:
            with st.spinner('Processing resumes...'):
                time.sleep(2)  # Simulate processing time
                resumes_data = []
                for file in uploaded_files:
                    text, page_count = extract_text_from_pdf(file)
                    parsed_data = parse_resume(text, page_count)
                    resumes_data.append(parsed_data)
                    
                    # Print extracted resume data to the terminal (for debugging)
                    print("-----------------------------------------------------------------------------")
                    print(f"Extracted Data from {file.name}:")
                    print("-----------------------------------------------------------------------------")
                    print(f"Name: {parsed_data['name']}")
                    print(f"Email: {', '.join(parsed_data['email'])}")
                    print(f"Phone: {', '.join(parsed_data['phone'])}")
                    print(f"GitHub: {parsed_data['github']}")
                    print(f"University: {', '.join(parsed_data['university'])}")
                    print(f"Degree: {', '.join(parsed_data['degree'])}")
                    print(f"Skills: {', '.join(parsed_data['skills'])}")
                    print(f"Total Pages: {parsed_data['no_of_pages']}")
                    print("-----------------------------------------------------------------------------")
                    print("\n")

                # Get the required skills as a list
                required_skills = [skill.strip().lower() for skill in required_skills_input.split(",")]

                # Rank the resumes based on skill matching
                ranked_resumes = rank_resumes(resumes_data, required_skills)

                # Display Ranked Results
                st.subheader("Ranked Resumes")
                for rank, (name, match_count) in enumerate(ranked_resumes, 1):
                    st.write(f"{rank}. {name} - Skill Match Count: {match_count}")
                    
                    # Display contact details (Email, Phone) below the name
                    resume_data = next(resume for resume in resumes_data if resume["name"] == name)
                    st.write(f"**Email**: {', '.join(resume_data['email'])}")
                    st.write(f"**Phone**: {', '.join(resume_data['phone'])}")
        else:
            st.error("Please upload resumes and enter required skills.")

if __name__ == "__main__":
    main()
