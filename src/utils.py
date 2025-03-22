from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import List
import os
from exa_py import Exa 

load_dotenv(override=True)


mcp = FastMCP(
    name="SAP Supply Chain Search", 
    version="1.0.0",
    description="Web search capability using Exa API that provides real-time internet search results. Supports both basic and advanced search with filtering options including domain restrictions, text inclusion requirements, and date filtering. Returns formatted results with titles, URLs, publication dates, and content summaries."
)