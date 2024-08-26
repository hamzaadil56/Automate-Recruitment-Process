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
    Check which agent is running and update the status of the agent in the API.
    Tracks the progress of each agent. 
    After completing the task by an agent, this function returns the status, and the name of the agent.
    This information is sent to the API using the API sender tool.
    :param agent_name: The name of the agent
    :param status: The status of the agent
    :return: The status and the name of the agent
    :rtype: dict
    """

    data = {
        "agent_name": agent_name,
        "status": status,
    }
    # Send progress to API
    api_sender_tool(data)
