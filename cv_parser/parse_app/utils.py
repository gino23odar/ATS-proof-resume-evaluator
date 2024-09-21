import json
import boto3
import pymupdf
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.conf import settings
from botocore.exceptions import ClientError

def read_uploaded_file(file_object: UploadedFile, file_extension: str):
    with pymupdf.open(stream=file_object.read(), filetype=file_extension) as pdf:
        text = ""
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
    
    return text


ai_credentials_options = {
    "region_name": settings.GEN_AI_REGION,
    "aws_access_key_id": settings.GEN_AI_ACCESS_KEY,
    "aws_secret_access_key": settings.GEN_AI_SECRET_KEY
}


prompt_data = """
You are an AI bot designed to extract information from resumes. You have been given a resume to extract information from, his is the information you must extract from the resume:
    
1. applicant_name: ""
2. highest_level_of_education: ""
3. area_of_study: ""
4. institution: ""
5. introduction: ""
6. skills: string[]
7. english_proficiency_level: ""
8. experiences: [{"employer_name": "", role: "", duration: ""}]

Give the extracted information in JSON format only.
Note: if the info is not present, leave the field blank. Avoid repeating the same things in the response.
"""

def test_credentials():
    try:
        client = boto3.client("sts", region_name=settings.GEN_AI_REGION, 
                              aws_access_key_id=settings.GEN_AI_ACCESS_KEY, 
                              aws_secret_access_key=settings.GEN_AI_SECRET_KEY)
        response = client.get_caller_identity()
        print("Credentials are valid:", response)
    except Exception as e:
        print("Error validating credentials:", e)


def test_bedrock_invoke():
    try:
        # Initialize the Bedrock client
        client = boto3.client(
            "bedrock-runtime",
            region_name=settings.GEN_AI_REGION,
            aws_access_key_id=settings.GEN_AI_ACCESS_KEY,
            aws_secret_access_key=settings.GEN_AI_SECRET_KEY
        )
        
        # Define your payload
        payload = {
            "prompt": "Hello, world!",
            "max_gen_len": 50,
            "temperature": 0.7
        }
        
        # Invoke the model
        response = client.invoke_model(
            body=json.dumps(payload),
            modelId="meta.llama3-8b-instruct-v1:0",  # Replace with your actual model ID
            accept="application/json",
            contentType="application/json"
        )
        
        # Print the response
        response_body = json.loads(response.get("body").read())
        print("Model response:", response_body)
        
    except ClientError as e:
        print("Error invoking model:", e)
    except Exception as e:
        print("Unexpected error:", e)

def extract_resume_info(text: str):
    # test_credentials()
    # test_bedrock_invoke()
    try:
        bedrock = boto3.client("bedrock-runtime", **ai_credentials_options)
        
        payload = {
            "prompt": "[INST]" + prompt_data + "Resume Content::" + text + "[INST]",
            "max_gen_len": 2048,
            "temperature": 0.4,
            "top_p": 0.9,
        }
        body = json.dumps(payload)
        model_id = "meta.llama3-8b-instruct-v1:0"

        response = bedrock.invoke_model(
            modelId = model_id,
            contentType="application/json",
            accept="application/json",
            body = body,
        )

        response_body = json.loads(response.get("body").read())
        #print(response)
        response_text: str = response_body["generation"]
        #print("response: " + response_text + "endoftext.")

        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        # print(start, end)
        # print(response_text[start:end])
        json_str = response_text[start:end]
        data = json.loads(json_str)

    except Exception as e:
        raise ValidationError(f"Something went wrong while extracting resume info: {e}", 500)
    return data

prompt_data2 = """
Pretend you are a professional recruiter with over 30 years of experience in resume screening and also an expert in ATS systems. 
You have been given a resume and a job posting to extract insights from. This is the information extracted from the resume: 
"""

prompt_data3 = """
    Evaluate the resume in regards to how appropriate it is for a job posting and give out the following insights in JSON format only:
    1. Matched skills: string[]
    2. Important skills missing: string[]
    3. improved descriptions
    4. general improvements
    5. things to remove from the resume
    6. things to add to the resume
    7. Resume score: 0-100

    Note: if you find the information sufficient, add a simple 'ok' to the field.
    Use the following description about the job posting to make the evaluation: 
"""

def extract_resume_insights(resume: str, job_posting: str):
    test_credentials()
    test_bedrock_invoke()
    try:
        bedrock = boto3.client("bedrock-runtime", **ai_credentials_options)
        
        payload = {
            "prompt": "[INST]" + prompt_data2 + resume + prompt_data3 + job_posting + "[INST]",
            "max_gen_len": 2048,
            "temperature": 0.4,
            "top_p": 0.9,
        }
        body = json.dumps(payload)
        model_id = "meta.llama3-8b-instruct-v1:0"

        response = bedrock.invoke_model(
            modelId = model_id,
            contentType="application/json",
            accept="application/json",
            body = body,
        )

        response_body = json.loads(response.get("body").read())
        #print(response)
        response_text: str = response_body["generation"]
        print("response: " + response_text + "endoftext.")

        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        #print(response_text[start:end])
        json_str = response_text[start:end]
        data = json.loads(json_str)

    except Exception as e:
        raise ValidationError(f"Something went wrong while extracting resume info: {e}", 500)
    return data