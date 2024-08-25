import os
import requests
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool

# Custom Tool to send data to API


class SendToAPI:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

    def __call__(self, data):
        response = requests.put(self.api_endpoint, json=data)
        return response.json()


# Create an API sender tool
api_sender_tool = SendToAPI(
    api_endpoint="http://127.0.0.1:8000/tasks")

# Custom callback function to track progress


@tool("Progress Callback Tool")
def progress_callback(agent_name, task_description, progress, output):
    """Tracks the progress of each agent. After completing the task, agent return the progress whether it is inprogress or completed."""

    data = {
        "agent_name": agent_name,
        "task_description": task_description,
        "progress": progress,
        "report_candidates_task": output,
    }
    # Send progress to API
    api_sender_tool(data)
