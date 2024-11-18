# Resume Parser and Ranker

  #### This project is a Resume Parser and Ranker system that leverages Natural Language Processing (NLP) techniques to extract, process, and rank resumes based on specified skill requirements. Designed for recruiters and hiring managers, this tool automates the resume screening process, making it more efficient and scalable.

### 1) Features

- `Resume Parsing`: Extracts structured data such as name, email, phone, degree, university, GitHub profiles, and technical skills from resumes in PDF format.
  
- `Skill Matching`: Matches extracted skills with required skills using keyword and fuzzy matching techniques.
  
- `Resume Ranking`: Scores and ranks candidates based on skill alignment with job requirements.
  
- `User-Friendly Interface`: Built using Streamlit, allowing users to upload resumes and input required skills seamlessly.
  
- `Multi-Resume Support`: Processes multiple resumes simultaneously.


### 2) File Structure
```md
resume-parser-ranker/
├── src/
│   ├── dataset/
│   │   └── skills.csv                # Dataset containing technical skills for matching
│   ├── resumes/
│   │   ├── 0testresume.pdf           # Sample resume files for testing
│   │   ├── 1sandeep.pdf
│   │   ├── New-York-Resume-Template.pdf
│   │   ├── OmkarResume.pdf
│   │   └── Vienna-Modern-Resume.pdf
├── app.py                            # Main application script
├── requirements.txt                  # Python dependencies for the project
├── .gitignore                        # Files and directories to ignore in version control
```

### 2) Prerequisites

- Python 3.8 or higher
  
- Libraries:
  - `streamlit`
  - `pandas`
  - `spacy`
  - `fuzzywuzzy`
  - `PyPDF2`
  - (See `requirements.txt` for the complete list of dependencies)

  To install all dependencies, run:

  ```bash
  pip install -r requirements.txt
  ```

### 4) Usage

  1. Clone this repository
     ```bash
     git clone https://github.com/Arvind-Sabarinathan/Resume-Parser.git
     ```
     
  2. Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```
     
  3. Run the application:
     ```bash
     cd src
     streamlit run app.py
     ```
     
  4. Open the application in your browser and:
       - Upload resumes in PDF format.
       - Enter required skills (comma-separated).
       - View extracted resume data and ranked candidates.
         
### 5) Contributors

- Gokul U (22MIS0291): gokul.u2022@vitstudent.ac.in

- Arvind S (22MIS0328): arvind.s2022@vitstudent.ac.in
