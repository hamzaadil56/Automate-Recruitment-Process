from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from .main import run
import asyncio

# Define the data model to store task statuses


class TaskStatus(BaseModel):
    research_candidates_task: bool = False
    match_and_score_candidates_task: bool = False
    outreach_strategy_task: bool = False
    report_candidates_task: bool = False


class JobDescription(BaseModel):
    job_description: str


class AgentOutPut(BaseModel):
    agent_name: str = ""
    task_description: str = ""
    progress: str = ""
    report_candidates_task: str = ""


# Create an instance of FastAPI
app = FastAPI()

# Initialize a global object to store the status of tasks
task_status = TaskStatus()

inital_agent = AgentOutPut()


@app.get("/tasks", response_model=AgentOutPut)
async def get_task_status():
    """
    Retrieve the current status of all tasks.
    """
    return inital_agent


@app.post("/start-agents")
async def start_agents(job_description: JobDescription):
    """
    Start the agents with the provided job description.
    """
    asyncio.create_task(run(job_description.job_description))
    # await run(job_description.job_description)
    # Implement logic to start agents with the provided job description
    return {"message": "Agents started successfully"}


@app.put("/tasks")
async def update_task_status(agent_output: AgentOutPut):
    """
    Update the status of tasks.
    """
    global inital_agent
    inital_agent = agent_output
    return {"message": "Task statuses updated successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
