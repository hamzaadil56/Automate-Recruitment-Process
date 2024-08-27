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
def progress_callback(agent_name, status):
    """
    Checks which agent is running and return the status of the agent. The status must be either 'InProgress' or 'Completed'. If the agent starts its task, this tool will return the status of that agent as 'InProgress'. If the agent has completed its task, this tool will return the status as 'Completed'.

    Args:
        agent_name (str): The name of the agent.
        status (str): The status of the agent.

    Returns:
        dict: A dictionary containing the agent_name and status.

    Example:
        >>> progress_callback('Agent1', 'InProgress')
        {'agent_name': 'Agent1', 'status': 'InProgress'}



    """

    data = {
        "agent_name": agent_name,
        "status": status,
    }
    # Send progress to API
    api_sender_tool(data)
