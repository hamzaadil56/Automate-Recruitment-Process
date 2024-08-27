import { useEffect, useState } from "react";
import AgentCard from "./components/agentCard";
import ResearchLogo from "./assets/research.png";
import LinkLogo from "./assets/link.png";
import ConversationLogo from "./assets/speech-bubble.png";
import ReporterLogo from "./assets/reporter.png";
import Alert from "./components/alert";
// import './App.css'

function App() {
  const [agentStatus, setAgentStatus] = useState({
    agent_name: "",
    status: "",
  });
  const [alertMessage, setAlertMessage] = useState("");

  const pollAgentStatus = () => {
    const intervalId = setInterval(async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/tasks");
        const data = await response.json();
        setAgentStatus(data);

        // Check if the status is 'Completed'
        if (data.status === "Completed") {
          clearInterval(intervalId); // Stop polling when completed
        }
      } catch (error) {
        console.error("Error fetching agent status:", error);
      }
    }, 1000); // Poll every second
  };

  const handleStartAgent = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/start-agents", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_description:
            "We are looking for a skilled and motivated Software Engineer with 2 years of professional experience to join our growing team. The ideal candidate is passionate about software development, eager to learn, and ready to contribute to a range of exciting projects. As a Software Engineer, you will work closely with cross-functional teams to design, develop, and maintain software applications that meet our high standards.Key Responsibilities:- Collaborate with product managers, designers, and other engineers to develop, test, and deploy high-quality software solutions.- Write clean, maintainable, and efficient code across various platforms and languages.- Participate in code reviews, providing constructive feedback to peers and improving the overall code quality.- Troubleshoot and debug issues, ensuring timely resolution of any problems.- Stay up-to-date with industry trends, technologies, and best practices to continually improve your skills and the team's output.- Contribute to the documentation of software processes, code, and system architecture.Required Skills and Qualifications:- Bachelor’s degree in Computer Science, Software Engineering, or a related field.- 2 years of professional software development experience.- Proficiency in at least one programming language (e.g., Python, JavaScript, Java, C++).- Experience with version control systems, particularly Git.- Familiarity with front-end technologies such as HTML, CSS, and JavaScript frameworks (e.g., React, Angular).- Understanding of back-end development, including server-side logic, database design, and RESTful APIs.- Strong problem-solving skills and attention to detail.- Excellent communication and teamwork abilities.Preferred Qualifications:- Experience with cloud platforms (e.g., AWS, Azure, Google Cloud).- Familiarity with DevOps practices and tools (e.g., Docker, Jenkins, Kubernetes).- Exposure to Agile methodologies and tools (e.g., Jira, Trello).- Knowledge of automated testing and CI/CD pipelines.What We Offer:- Competitive salary and benefits package.- Opportunities for professional growth and development.- A collaborative and inclusive work environment.- The chance to work on exciting projects that make an impact.",
        }),
      });
      const data = await response.json();
      if (data?.success) {
        setAlertMessage(data?.message);
      }
      pollAgentStatus();
    } catch (error) {
      console.error("Error starting agent:", error);
    }
  };

  return (
    <main className="w-full max-h-screen h-screen flex flex-col justify-center gap-10 text-blue-600 p-4">
      <Alert message={alertMessage} onClose={() => setAlertMessage("")} />
      <div>
        <h1 className="text-3xl font-bold text-center">
          HR Recruitment Automated Recruitment Process
        </h1>
      </div>
      <div className="flex justify-center w-full gap-10 ">
        <AgentCard logo={ResearchLogo} />
        <AgentCard logo={LinkLogo} />
        <AgentCard logo={ConversationLogo} />
        <AgentCard logo={ReporterLogo} />
      </div>
      <div className="w-full max-w-[700px]  mx-auto  relative">
        <div>
          {agentStatus?.agent_name} {agentStatus?.status}
        </div>
        <textarea
          id="message"
          rows={6}
          className="block p-2.5 w-full text-sm text-gray-900  rounded-lg border border-gray-300 focus:ring-blue-500 bg-[#d5e1f7] focus:border-blue-500    "
          placeholder="Write your job description here..."
          defaultValue={""}
        />
        <button
          onClick={handleStartAgent}
          className="absolute bottom-0 right-0 bg-blue-900 m-2 text-white rounded-full w-[40px] h-[40px]"
        >
          send
        </button>
      </div>
    </main>
  );
}

export default App;
