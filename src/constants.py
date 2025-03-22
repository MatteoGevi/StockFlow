import os
import json

openai_api_key = os.getenv("OPENAI_API_KEY")

SAP_ASHOST = os.getenv("SAP_ASHOST")
SAP_USER = os.getenv("SAP_USER")
SAP_PASSWORD = os.getenv("SAP_PASSWORD")
SAP_SYSNR = os.getenv("SAP_SYSNR")
SAP_CLIENT = os.getenv("SAP_CLIENT")

system_prompt = """
You are a helpful assistant that can answer questions and help with tasks.
"""

user_prompt = """

"""