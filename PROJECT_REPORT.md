# PROJECT REPORT: HireAI - Job Application Assistant

## 1. Cover Page & Title Page
*(Note: Use official college specimen)*
- **Project Title**: HireAI - Job Application Assistant
- **Submitted By**: [Your Name], MCA [Section/Roll No]
- **Supervisor**: [Supervisor's Name], [Designation], Department of MCA
- **Institution**: GL Bajaj Institute of Technology & Management, Greater Noida

---

## 2. Acknowledgement
I would like to thank my supervisor [Supervisor's Name] for the guidance and support provided during the development of this project. Their technical suggestions helped me in structuring the AI pipeline and resolving several implementation hurdles. I also extend my thanks to the Department of MCA, GL Bajaj Institute of Technology & Management, for providing the necessary resources and environment to complete this work.

---

## 3. Certificate of Originality
*(Note: Use double line spacing, Times New Roman, Size 14)*
I hereby declare that the project work entitled "HireAI - Job Application Assistant" is an original record of the work performed by me. This project has not been submitted elsewhere for the award of any degree or diploma.

**Student Signature**: ____________________
**Date**: ____________________

---

## 4. Certificate of Acceptance
*(Note: Use double line spacing, Times New Roman, Size 14)*
This is to certify that the project titled "HireAI - Job Application Assistant" is a bona fide work carried out by [Your Name] under my supervision and is submitted in partial fulfillment of the requirements for the degree of Master of Computer Applications.

**SUPERVISOR**
[Supervisor's Name]
[Academic Designation]
Department of MCA
GL Bajaj Institute of Technology & Management, Greater Noida

---

## 5. Executive Summary
*(Note: Type as a one-page synopsis, double line spacing, Times New Roman, Size 14)*

The HireAI project is developed to help job seekers tailor their applications to meet the requirements of Applicant Tracking Systems (ATS). Most modern companies use these systems to filter resumes based on specific keywords and skill sets, which often leads to qualified candidates being rejected simply because their resume is not optimized for the software.

The system implements a multi-stage pipeline using a Large Language Model (Gemma 4) and a state-management framework called LangGraph. The process begins by extracting data from job descriptions provided as URLs or PDFs. The system then analyzes the user's professional profile and calculates a match score based on semantic similarity using vector embeddings in a Supabase database. Based on this analysis, the tool generates a tailored resume and cover letters in different tones. To ensure the quality of the output, a validation step was added to check for accuracy and grammar. Additionally, a mock interview simulator was built to help users prepare for the next stage of the hiring process. The final implementation uses FastAPI for the backend and Docker for deployment, aiming to reduce the time spent on application tailoring from hours to under a minute.

---

## 6. Table of Contents
1. Introduction .................................................... [Page]
2. Background Study ................................................ [Page]
3. Requirement Analysis ............................................ [Page]
4. System Design and Development .................................... [Page]
   4.1 Architecture
   4.2 Technology Stack
   4.3 Pipeline Modules
   4.4 Implementation Logic
5. Testing and Implementation ...................................... [Page]
6. Results and Discussion .......................................... [Page]
7. Conclusion and Future Work ...................................... [Page]
8. List of Tables ................................................... [Page]
9. List of Figures .................................................. [Page]
10. Abbreviations ................................................... [Page]
11. Appendices ..................................................... [Page]
12. References ..................................................... [Page]

---

## Chapter 1: Introduction

### 1.1 Project Overview
HireAI is a tool designed to assist candidates in creating job applications that are better aligned with specific job descriptions. Instead of sending the same resume to every employer, the system analyzes the specific needs of a job post and suggests modifications to the user's profile to increase the chances of getting an interview.

### 1.2 Problem Statement
Many job seekers struggle to understand why their resumes are rejected by automated systems. These ATS tools look for specific terminology and skill patterns. Manually rewriting a resume for every single application is impractical for most users, leading to a high volume of generic applications with low success rates.

### 1.3 Objectives
- To build a system that can read and structure data from different job sources (URLs/PDFs).
- To implement a scoring system that compares a user's skills with job requirements.
- To automate the creation of tailored cover letters and resumes.
- To provide a simulated environment for interview practice.

### 1.4 Scope of the Work
The project focuses on the AI backend development. It involves building a structured pipeline that handles data ingestion, skill matching, and document generation. The scope includes the integration of a vector database for semantic search and the use of a Large Language Model for text generation.

---

## Chapter 2: Background Study

### 2.1 Review of Existing Tools
There are several AI writing tools available today, such as ChatGPT. While these tools can write cover letters, they require the user to provide all the context manually in every prompt. There is no built-in mechanism to "verify" if the generated content actually matches the job requirements or to provide a numerical score of the match.

### 2.2 Gaps Identified
- **Lack of Structure**: Most AI tools are chat-based and don't follow a fixed professional workflow.
- **No Data Extraction**: Users have to copy-paste text manually; there is no direct integration with job URLs.
- **No Validation**: Once the AI generates a resume, there is no secondary check to ensure that the AI hasn't added skills the user doesn't actually possess.

### 2.3 Proposed Solution
To address these issues, this project uses a "Graph" based approach. By using LangGraph, the application follows a strict sequence of steps (Ingest $\rightarrow$ Analyze $\rightarrow$ Match $\rightarrow$ Generate $\rightarrow$ Validate). This ensures that the final output is based on actual data and has been checked for quality.

---

## Chapter 3: Requirement Analysis

### 3.1 Functional Requirements
- **Parsing**: The system must be able to extract text from PDF files and web pages.
- **Matching**: The system must compare the user's profile with the job description and provide a percentage score.
- **Generation**: The tool should produce at least three versions of a cover letter (Formal, Confident, and Conversational).
- **Interview Sim**: The system should maintain a conversation history to simulate a real interview.

### 3.2 Non-Functional Requirements
- **Performance**: The entire process from input to output should take less than 60 seconds.
- **Reliability**: The system should handle cases where a job URL is blocked or a PDF is unreadable.
- **Usability**: The API should be easy to integrate with a frontend.

### 3.3 Software and Hardware Specifications
- **Language**: Python 3.11
- **Framework**: FastAPI
- **State Management**: LangGraph
- **LLM**: Gemma 4 (Ollama Cloud)
- **Database**: Supabase (with pgvector)
- **Containers**: Docker
- **Libraries**: PyMuPDF (PDF parsing), Playwright (Web scraping)

---

## Chapter 4: System Design and Development

### 4.1 Architecture
The system is built as a microservice. The backend handles all AI logic and communicates via JSON APIs. The core of the system is a state-managed pipeline where the output of one stage is passed as the input to the next.

### 4.2 Technology Stack
- **FastAPI**: Used for the API layer because of its support for asynchronous operations.
- **LangGraph**: Used to manage the flow of the AI pipeline. It allows for a stateful transition between different nodes.
- **Supabase (pgvector)**: Used to store and compare skill embeddings. This allows the system to understand that "React.js" and "Frontend Development" are related.
- **Gemma 4**: Used as the primary LLM for reasoning and text generation.

### 4.3 Pipeline Modules
The project is divided into six main nodes:
1. **JD Ingestion**: Converts a URL or PDF into a structured JSON object.
2. **Portfolio Analysis**: Extracts the user's professional experience and skills.
3. **Skill Matching**: Uses cosine similarity to calculate the ATS match score.
4. **Doc Generation**: Creates the tailored resume and cover letters.
5. **QA Validation**: A secondary check to ensure the documents are accurate.
6. **Post-Apply Intel**: Generates a follow-up email strategy.

### 4.4 Implementation Logic
The system uses a `PipelineState` object. This object travels through the graph, getting updated at each node. For example, the `jd_ingestion_node` adds the `job_description` to the state, which is then used by the `skill_matching_node` to compare against the user's profile.

---

## Chapter 5: Testing and Implementation

### 5.1 Testing Approach
The system was tested in three stages:
1. **Node Testing**: Each node (e.g., the parser) was tested individually to ensure it could handle different file formats.
2. **Pipeline Testing**: The entire flow was tested to ensure the state was passing correctly between nodes.
3. **Edge Case Testing**: Tested with invalid URLs and empty PDF files to ensure the system doesn't crash.

### 5.2 Implementation Challenges
One of the main challenges was dealing with websites that block scrapers. To solve this, a fallback was implemented where the user can paste the raw text if the URL scraping fails. Another challenge was the LLM occasionally adding skills that weren't in the original resume; this was solved by adding the "QA Validation" node.

---

## Chapter 6: Results and Discussion

### 6.1 Outcomes
The system successfully automates the creation of a tailored application kit. In test runs, the generated documents were found to be more specific to the job requirements compared to generic AI-generated letters.

### 6.2 Comparison
| Activity | Manual Method | HireAI Method |
|-----------|----------------|---------------|
| Researching JD | 30 mins | 2 seconds |
| Tailoring Resume | 1-2 hours | 20 seconds |
| Writing Cover Letter | 45 mins | 15 seconds |
| Total Time | $\approx 3$ hours | $\approx 1$ minute |

### 6.3 Limitations
- **Web Scraping**: Some job boards have very strict security that prevents automated reading.
- **API Dependency**: The system depends on the availability of the Ollama Cloud API.

---

## Chapter 7: Conclusion and Future Work

### 7.1 Conclusion
The HireAI project successfully demonstrates how LLMs and graph-based orchestration can be used to automate professional tasks. The system reduces the effort required for job applications while increasing the quality of the submitted documents.

### 7.2 Future Work
- **Browser Extension**: Building a plugin to trigger the pipeline directly from a browser.
- **Voice Interviews**: Implementing speech-to-text for the interview simulator.
- **Direct Submission**: Adding the ability to send the generated email directly to the recruiter.

---

## List of Tables
- Table 1: Software Specifications
- Table 2: Comparison of Manual vs AI process

## List of Figures
- Figure 1: System Architecture
- Figure 2: LangGraph Workflow
- Figure 3: Sample Output JSON

## Abbreviations
- **ATS**: Applicant Tracking System
- **LLM**: Large Language Model
- **JD**: Job Description
- **API**: Application Programming Interface
- **JSON**: JavaScript Object Notation

## References
1. LangGraph Documentation, LangChain Inc.
2. FastAPI Documentation, Tiangolo.
3. Ollama Model Documentation.
4. Supabase Vector Guide.
