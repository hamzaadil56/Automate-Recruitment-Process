from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    status: str = ""


class AgentResponse(BaseModel):
    result: str = ""


# Create an instance of FastAPI
app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize a global object to store the status of tasks
task_status = TaskStatus()

inital_agent = AgentOutPut()

agents_response = AgentResponse()


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
    asyncio.create_task(background_task(job_description.job_description))
    return {"message": "Agents started successfully", "success": True}


async def background_task(description: str):
    # Simulate a long-running task
    try:
        result = await run(description)
        # Update the global variable with the result when the task is complete
        global agents_response

        agents_response.result = result  # Store the result of the task
    except Exception as e:
        # Handle exceptions and update status accordingly
        agents_response.status = f"Failed: {str(e)}"


@app.get("/agents-response", response_model=AgentResponse)
async def get_agents_response():
    """
    Retrieve the result of the background task once it is completed.
    """
    return agents_response


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
