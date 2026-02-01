"""
USIU Multi-Agent Student Support System
Lab 2 Assignment: Building a Multi-Agent AI System

This system uses a team of specialized AI agents to handle student inquiries
at United States International University (USIU).

Architecture:
- Supervisor Agent: Routes requests to appropriate specialized agents
- Greeter Agent: Classifies intent and welcomes students
- Academic Advisor Agent: Handles course, registration, and academic queries
- Finance Agent: Manages fee inquiries, payment issues, scholarships
- Student Life Agent: Covers housing, clubs, events, facilities
- IT Support Agent: Handles portal, email, and technical issues
- Escalation Agent: Manages complex cases requiring human intervention
- Quality Reviewer Agent: Validates responses before delivery
"""

from typing import Annotated, TypedDict, Sequence
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
import json
from datetime import datetime
import operator

# ===========================
# STATE DEFINITION
# ===========================

class AgentState(TypedDict):
    """Shared state across all agents"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_agent: str
    intent: str
    user_query: str
    findings: dict
    needs_human: bool
    escalation_reason: str
    iteration_count: int
    final_response: str
    student_context: dict  # Could store student ID, history, preferences

# ===========================
# SIMULATED USIU DATABASE
# ===========================

USIU_KNOWLEDGE_BASE = {
    "academic": {
        "registration": {
            "deadlines": "Registration for Spring 2026 semester: Jan 6-17, 2026. Late registration with penalty: Jan 20-24, 2026.",
            "process": "1. Log into student portal 2. Check cleared status 3. Select courses 4. Submit registration 5. Print confirmation",
            "requirements": "Must have paid at least 60% of fees and have no library fines or academic holds"
        },
        "courses": {
            "DSA 2020A": {
                "name": "Artificial Intelligence",
                "credits": 3,
                "prerequisites": "DSA 1011 (Data Structures)",
                "instructor": "Dr. Kimani",
                "schedule": "Mon/Wed 2:00-3:30 PM, Lab: Fri 10:00-12:00"
            },
            "BUS 3010": {
                "name": "Strategic Management",
                "credits": 3,
                "prerequisites": "BUS 2010",
                "instructor": "Prof. Odhiambo"
            }
        },
        "gpa": {
            "calculation": "Grade points × credit hours, divided by total credit hours",
            "grading_scale": "A=4.0, A-=3.7, B+=3.3, B=3.0, B-=2.7, C+=2.3, C=2.0, C-=1.7, D+=1.3, D=1.0, F=0.0"
        }
    },
    "finance": {
        "tuition": {
            "undergraduate": "$850 per credit hour",
            "graduate": "$950 per credit hour",
            "payment_plans": "Available in 3 or 4 installments with approval"
        },
        "scholarships": {
            "merit": "Academic excellence scholarship: 25-50% tuition waiver for GPA 3.5+",
            "need_based": "Apply through financial aid office with required documents",
            "sports": "Athletic scholarships available through sports department"
        },
        "payment_methods": "M-Pesa, bank transfer, credit card (Visa/Mastercard), or in-person at cashier"
    },
    "student_life": {
        "housing": {
            "on_campus": "Limited spaces. Apply by Dec 15 for Spring semester. Cost: $1,200-1,800/semester",
            "off_campus": "Housing office maintains list of verified landlords near campus"
        },
        "clubs": "60+ student clubs including Debate, Tech Club, Drama, Sports clubs. Join via student portal",
        "events": "Check USIU Events calendar on portal. Major events: Cultural Week (March), Career Fair (April)"
    },
    "it_support": {
        "portal": "https://portal.usiu.ac.ke - Use student ID as username. Reset password at IT helpdesk",
        "email": "Format: firstname.lastname@usiu.ac.ke - Access via Office 365",
        "wifi": "Network: USIU-Student, Password provided during orientation"
    },
    "general": {
        "contact": {
            "phone": "+254 730 116 000",
            "email": "admissions@usiu.ac.ke",
            "location": "Nairobi, Kenya - Off Thika Road",
            "hours": "Mon-Fri 8:00 AM - 5:00 PM, Sat 9:00 AM - 1:00 PM"
        },
        "semester_dates": {
            "spring_2026": "Jan 20 - May 15, 2026",
            "fall_2026": "Aug 25 - Dec 18, 2026"
        }
    }
}

# ===========================
# AGENT DEFINITIONS
# ===========================

class USIUAgentTeam:
    def __init__(self, model_name="claude-sonnet-4-20250514"):
        self.llm = ChatAnthropic(model=model_name, temperature=0.3)
        
    def create_agent(self, role: str, system_prompt: str):
        """Factory method to create specialized agents"""
        def agent_node(state: AgentState):
            messages = [SystemMessage(content=system_prompt)]
            messages.extend(state["messages"][-3:])  # Last 3 messages for context
            
            response = self.llm.invoke(messages)
            return {
                "messages": [response],
                "current_agent": role
            }
        return agent_node
    
    # ===== GREETER AGENT =====
    def greeter_agent(self, state: AgentState):
        """Classifies intent and provides warm welcome"""
        system_prompt = f"""You are the Greeter Agent for USIU's student support system.
        
Your responsibilities:
1. Warmly welcome the student
2. Classify their inquiry intent into ONE category: academic, finance, student_life, it_support, general, or unclear
3. Ask clarifying questions if intent is unclear

Current query: {state['user_query']}

Respond warmly and classify the intent. Format your response as:
INTENT: [category]
RESPONSE: [your warm greeting and any clarifying questions]
"""
        
        messages = [SystemMessage(content=system_prompt)]
        response = self.llm.invoke(messages)
        
        # Parse intent
        response_text = response.content
        intent = "general"
        if "INTENT:" in response_text:
            intent_line = [line for line in response_text.split("\n") if "INTENT:" in line][0]
            intent = intent_line.split("INTENT:")[1].strip().lower()
        
        return {
            "messages": [response],
            "current_agent": "greeter",
            "intent": intent
        }
    
    # ===== ACADEMIC ADVISOR AGENT =====
    def academic_advisor_agent(self, state: AgentState):
        """Handles academic queries"""
        kb = json.dumps(USIU_KNOWLEDGE_BASE["academic"], indent=2)
        system_prompt = f"""You are the Academic Advisor Agent for USIU.

You help with: course registration, course information, academic requirements, GPA calculations, deadlines.

USIU Academic Knowledge Base:
{kb}

Student Query: {state['user_query']}

Provide accurate, helpful information based on the knowledge base. If information isn't available, say so and suggest contacting the registrar's office.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "academic_advisor",
            "findings": {**state.get("findings", {}), "academic_info_provided": True}
        }
    
    # ===== FINANCE AGENT =====
    def finance_agent(self, state: AgentState):
        """Handles financial queries"""
        kb = json.dumps(USIU_KNOWLEDGE_BASE["finance"], indent=2)
        system_prompt = f"""You are the Finance Agent for USIU.

You help with: tuition fees, payment methods, scholarships, financial aid, payment deadlines.

USIU Finance Knowledge Base:
{kb}

Student Query: {state['user_query']}

Provide accurate financial information. For specific account inquiries, direct students to the finance office.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "finance",
            "findings": {**state.get("findings", {}), "finance_info_provided": True}
        }
    
    # ===== STUDENT LIFE AGENT =====
    def student_life_agent(self, state: AgentState):
        """Handles campus life queries"""
        kb = json.dumps(USIU_KNOWLEDGE_BASE["student_life"], indent=2)
        system_prompt = f"""You are the Student Life Agent for USIU.

You help with: housing, student clubs, campus events, facilities, student activities.

USIU Student Life Knowledge Base:
{kb}

Student Query: {state['user_query']}

Provide engaging information about campus life. Encourage student involvement.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "student_life",
            "findings": {**state.get("findings", {}), "student_life_info_provided": True}
        }
    
    # ===== IT SUPPORT AGENT =====
    def it_support_agent(self, state: AgentState):
        """Handles technical queries"""
        kb = json.dumps(USIU_KNOWLEDGE_BASE["it_support"], indent=2)
        system_prompt = f"""You are the IT Support Agent for USIU.

You help with: student portal access, email issues, WiFi connectivity, password resets.

USIU IT Knowledge Base:
{kb}

Student Query: {state['user_query']}

Provide clear technical guidance. For complex issues, direct to IT helpdesk.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "it_support",
            "findings": {**state.get("findings", {}), "it_info_provided": True}
        }
    
    # ===== QUALITY REVIEWER AGENT =====
    def quality_reviewer_agent(self, state: AgentState):
        """Reviews and validates responses"""
        last_response = state["messages"][-1].content if state["messages"] else ""
        
        system_prompt = f"""You are the Quality Reviewer Agent for USIU.

Review this response for:
1. Accuracy (based on USIU knowledge base)
2. Completeness (addresses the student's query)
3. Tone (professional yet friendly)
4. Actionability (clear next steps if needed)

Original Query: {state['user_query']}
Response to Review: {last_response}

If the response is good, approve it with "APPROVED: [reason]"
If it needs improvement, suggest changes with "NEEDS_REVISION: [specific feedback]"
If it requires human intervention, say "ESCALATE: [reason]"
"""
        
        messages = [SystemMessage(content=system_prompt)]
        response = self.llm.invoke(messages)
        
        review_text = response.content
        needs_human = "ESCALATE:" in review_text
        escalation_reason = ""
        
        if needs_human:
            escalation_reason = review_text.split("ESCALATE:")[1].strip()
        
        return {
            "messages": [response],
            "current_agent": "quality_reviewer",
            "needs_human": needs_human,
            "escalation_reason": escalation_reason
        }
    
    # ===== SUPERVISOR AGENT =====
    def supervisor_agent(self, state: AgentState):
        """Routes to appropriate specialist agent"""
        system_prompt = f"""You are the Supervisor Agent coordinating USIU's student support team.

Current situation:
- Intent: {state.get('intent', 'unknown')}
- Current agent: {state.get('current_agent', 'none')}
- Iteration: {state.get('iteration_count', 0)}

Available specialist agents:
- academic_advisor: courses, registration, grades, academic requirements
- finance: tuition, payments, scholarships, financial aid
- student_life: housing, clubs, events, campus facilities
- it_support: portal, email, technical issues
- quality_reviewer: validates responses before delivery

Based on the intent, route to the appropriate specialist. If a specialist has already responded, route to quality_reviewer.

Respond with ONLY the agent name to route to next, or FINISH if complete.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        response = self.llm.invoke(messages)
        
        next_agent = response.content.strip().lower()
        
        return {
            "messages": [response],
            "current_agent": "supervisor",
            "iteration_count": state.get("iteration_count", 0) + 1
        }
    
    # ===== ROUTING LOGIC =====
    def route_after_greeter(self, state: AgentState) -> str:
        """Route from greeter to appropriate specialist"""
        intent = state.get("intent", "general")
        
        intent_routing = {
            "academic": "academic_advisor",
            "finance": "finance",
            "student_life": "student_life",
            "it_support": "it_support",
            "general": "academic_advisor",  # Default
            "unclear": "academic_advisor"
        }
        
        return intent_routing.get(intent, "academic_advisor")
    
    def route_after_specialist(self, state: AgentState) -> str:
        """Route from specialist to quality reviewer or finish"""
        if state.get("iteration_count", 0) > 5:
            return END
        
        return "quality_reviewer"
    
    def route_after_reviewer(self, state: AgentState) -> str:
        """Route from reviewer to end or escalation"""
        if state.get("needs_human", False):
            return "escalation"
        return END
    
    def escalation_agent(self, state: AgentState):
        """Handles escalation to human"""
        system_prompt = f"""You are the Escalation Agent.

A case requires human intervention.
Reason: {state.get('escalation_reason', 'Complex inquiry')}

Provide the student with:
1. Acknowledgment of their complex inquiry
2. Specific contact information for human assistance
3. Expected response time
4. Reference number for follow-up

USIU Contact Info:
Phone: +254 730 116 000
Email: support@usiu.ac.ke
Hours: Mon-Fri 8AM-5PM
"""
        
        messages = [SystemMessage(content=system_prompt)]
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "current_agent": "escalation"
        }

# ===========================
# GRAPH CONSTRUCTION
# ===========================

def create_usiu_workflow():
    """Build the multi-agent workflow graph"""
    
    agent_team = USIUAgentTeam()
    
    # Create workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("greeter", agent_team.greeter_agent)
    workflow.add_node("academic_advisor", agent_team.academic_advisor_agent)
    workflow.add_node("finance", agent_team.finance_agent)
    workflow.add_node("student_life", agent_team.student_life_agent)
    workflow.add_node("it_support", agent_team.it_support_agent)
    workflow.add_node("quality_reviewer", agent_team.quality_reviewer_agent)
    workflow.add_node("escalation", agent_team.escalation_agent)
    
    # Set entry point
    workflow.set_entry_point("greeter")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "greeter",
        agent_team.route_after_greeter,
        {
            "academic_advisor": "academic_advisor",
            "finance": "finance",
            "student_life": "student_life",
            "it_support": "it_support"
        }
    )
    
    # Route all specialists to quality reviewer
    for specialist in ["academic_advisor", "finance", "student_life", "it_support"]:
        workflow.add_edge(specialist, "quality_reviewer")
    
    # Route from quality reviewer
    workflow.add_conditional_edges(
        "quality_reviewer",
        agent_team.route_after_reviewer,
        {
            "escalation": "escalation",
            END: END
        }
    )
    
    # Escalation ends the workflow
    workflow.add_edge("escalation", END)
    
    return workflow.compile()

# ===========================
# MAIN EXECUTION
# ===========================

def run_usiu_chatbot(user_query: str):
    """Execute the multi-agent chatbot"""
    
    print(f"\n{'='*60}")
    print(f"USIU Multi-Agent Student Support System")
    print(f"{'='*60}\n")
    print(f"Student Query: {user_query}\n")
    
    # Initialize state
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "current_agent": "none",
        "intent": "",
        "user_query": user_query,
        "findings": {},
        "needs_human": False,
        "escalation_reason": "",
        "iteration_count": 0,
        "final_response": "",
        "student_context": {}
    }
    
    # Create and run workflow
    app = create_usiu_workflow()
    
    # Stream execution
    print("Agent Workflow Execution:\n")
    for output in app.stream(initial_state):
        for agent_name, agent_state in output.items():
            print(f"🤖 Agent: {agent_name.upper()}")
            if "messages" in agent_state and agent_state["messages"]:
                last_message = agent_state["messages"][-1]
                print(f"Response: {last_message.content[:200]}...")
            print(f"{'-'*60}\n")
    
    return output

if __name__ == "__main__":
    # Example queries
    example_queries = [
        "When is the registration deadline for Spring 2026?",
        "How much does tuition cost per credit hour?",
        "I can't access my student portal, what should I do?",
        "What student clubs are available at USIU?"
    ]
    
    # Run first example
    print("\n" + "="*60)
    print("DEMO: Running Multi-Agent System")
    print("="*60)
    
    result = run_usiu_chatbot(example_queries[0])
    
    print("\n" + "="*60)
    print("Workflow Complete!")
    print("="*60)
