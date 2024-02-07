import streamlit as st#streamlit is used for creating interactive web applications
import google.generativeai as genai#Google.generativeai is the module providing the Gemini AI functionality.
import os#os is a standard library for interacting with the operating system
import PyPDF2 as pdf#Python package that allows you to work with PDF files. 
                    #It provides functionalities for reading, manipulating, and extracting information from PDF documents

                    
from dotenv import load_dotenv
load_dotenv() ##load all the environment variables from .env file

#This line configures the Gemini AI by setting its API key. The API key is retrieved from the environment variables using os.getenv.
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')#here we are loading model
    response = model.generate_content(input)
    return response.text

#Fuction to extract the content from the pdf file(Taking the PDF and extracting the text)
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader(len(reader.pages)):#here we iterate through all the pages
        page = reader.pages[page] #extract all the information from particular pages
        text+= str(page.extract_text())#here we extract the entire content from particular page to this text variable
    return text

#Prompt Template
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science,
data Analyst and big data engineer. Your task is to evaluate the resume based
on the given job description. You must consider the jon market is very competitive
and you should provide best assistance for inproving the resumes.
Assign the percentage matching based on JD and the missing keywords with the accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%", "MissingKeywords":"[]", "Profile Summary":""}}
"""

##streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume",type = "pdf",help = "Please upload the pdf")

submit = st.button("Submit")

#convert the uploaded file into text
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)