# USIU Multi-Agent Student Support System

**Lab 2 Assignment: Building a Multi-Agent AI System for Real-World Applications**

A sophisticated multi-agent chatbot system designed to handle student inquiries at United States International University (USIU) using LangGraph's hierarchical supervisor pattern.

## 📋 Use Case & Rationale

**Selected Domain:** Customer Care Team (Educational Institution Support)

**Why Multi-Agent?**
- **Specialization**: Different types of student queries require different expertise (academic, financial, technical)
- **Quality Control**: Built-in review process ensures accurate, helpful responses
- **Scalability**: Easy to add new specialized agents for emerging needs
- **Human Oversight**: Automatic escalation for complex cases
- **Reliability**: Agents can critique each other's outputs before delivery

Traditional single-agent chatbots struggle with:
- Maintaining deep knowledge across diverse domains (academics, finance, IT)
- Providing quality-controlled responses
- Knowing when to escalate to humans
- Adapting tone and approach based on query type

## 🏗️ Agent Team Architecture

```
                         ┌─────────────────┐
                         │   SUPERVISOR    │
                         │  (Orchestrator) │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            ┌───────▼────────┐          ┌──────▼──────┐
            │    GREETER     │          │   QUALITY   │
            │ Intent Classifier│        │   REVIEWER  │
            └───────┬────────┘          └──────▲──────┘
                    │                           │
        ┌───────────┼───────────┬──────────────┘
        │           │           │
  ┌─────▼────┐ ┌───▼────┐ ┌───▼────┐ ┌────▼─────┐
  │ ACADEMIC │ │FINANCE │ │STUDENT │ │IT SUPPORT│
  │ ADVISOR  │ │ AGENT  │ │  LIFE  │ │  AGENT   │
  └──────────┘ └────────┘ └────────┘ └──────────┘
                                │
                         ┌──────▼──────┐
                         │ ESCALATION  │
                         │    AGENT    │
                         └─────────────┘
```

### Agent Roles & Responsibilities

1. **Greeter Agent** (Intent Classifier)
   - Welcomes students warmly
   - Classifies query intent: academic, finance, student_life, it_support, general
   - Asks clarifying questions when needed

2. **Academic Advisor Agent**
   - Course information and registration
   - Academic requirements and deadlines
   - GPA calculations
   - Prerequisite checks

3. **Finance Agent**
   - Tuition and fee inquiries
   - Payment methods and deadlines
   - Scholarship information
   - Financial aid guidance

4. **Student Life Agent**
   - Housing information
   - Student clubs and organizations
   - Campus events and activities
   - Facilities and amenities

5. **IT Support Agent**
   - Student portal access issues
   - Email and Office 365 support
   - WiFi connectivity
   - Password resets

6. **Quality Reviewer Agent**
   - Validates response accuracy
   - Checks completeness and tone
   - Ensures actionable next steps
   - Flags cases needing human intervention

7. **Escalation Agent**
   - Handles complex cases
   - Provides human contact information
   - Issues reference numbers
   - Sets expectations for response time

## 🚀 How to Run

### Prerequisites

1. **Python 3.9+** installed
2. **Anthropic API Key** (Claude access)

### Installation Steps

```bash
# Clone the repository
git clone <your-repo-url>
cd usiu-multiagent-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### Running the Chatbot

#### Option 1: Command Line
```bash
python usiu_multiagent_system.py
```

#### Option 2: Web Interface
```bash
# Open the HTML file in your browser
open usiu_chatbot_interface.html
```

#### Option 3: Jupyter Notebook
```bash
jupyter notebook usiu_demo.ipynb
```

## 📊 Example Interactions

### Example 1: Academic Query

**Student Input:**
> "When is the registration deadline for Spring 2026 semester?"

**Agent Flow:**
1. **Greeter**: Classifies intent as "academic"
2. **Academic Advisor**: Retrieves registration deadlines from knowledge base
   - Regular registration: Jan 6-17, 2026
   - Late registration: Jan 20-24, 2026 (with penalty)
3. **Quality Reviewer**: Validates accuracy and completeness - APPROVED
4. **Response Delivered**

**Final Output:**
> "Hello! Welcome to USIU Student Support. 
> 
> The registration deadlines for Spring 2026 semester are:
> - Regular Registration: January 6-17, 2026
> - Late Registration: January 20-24, 2026 (penalty fees apply)
> 
> To register, please:
> 1. Log into the student portal
> 2. Ensure you've paid at least 60% of fees
> 3. Check that you have no library fines or academic holds
> 4. Select your courses and submit
> 
> Need help with registration? I'm here to assist!"

---

### Example 2: Financial Query

**Student Input:**
> "How much is tuition per credit and do you have scholarships available?"

**Agent Flow:**
1. **Greeter**: Classifies intent as "finance"
2. **Finance Agent**: Retrieves tuition and scholarship information
3. **Quality Reviewer**: Validates completeness - APPROVED

**Final Output:**
> "Great question! Here's the tuition information:
> 
> **Tuition Rates:**
> - Undergraduate: $850 per credit hour
> - Graduate: $950 per credit hour
> - Payment plans available in 3-4 installments
> 
> **Scholarships Available:**
> - Merit-based: 25-50% tuition waiver for GPA 3.5+
> - Need-based: Apply through financial aid office
> - Athletic: Contact the sports department
> 
> **Payment Methods:** M-Pesa, bank transfer, credit card (Visa/Mastercard)
> 
> Would you like more details about any specific scholarship?"

---

### Example 3: IT Support with Escalation

**Student Input:**
> "I can't log into my student portal and I've tried resetting my password three times but it's still not working!"

**Agent Flow:**
1. **Greeter**: Classifies intent as "it_support"
2. **IT Support Agent**: Provides initial troubleshooting steps
3. **Quality Reviewer**: Detects complexity, flags for escalation
4. **Escalation Agent**: Provides human contact information

**Final Output:**
> "I understand how frustrating portal access issues can be, especially when password resets aren't working.
> 
> This requires hands-on technical support. I'm escalating your case to our IT helpdesk.
> 
> **Immediate Action:**
> Please contact USIU IT Support:
> - Phone: +254 730 116 000
> - Location: IT Helpdesk, Main Campus
> - Hours: Mon-Fri 8:00 AM - 5:00 PM
> 
> **Reference Number:** USIU-IT-2026020001
> 
> The IT team will assist you within 2 hours during business hours. Bring your student ID!"

## 🔧 Technical Implementation

### Framework Choice: LangGraph
**Why LangGraph?**
- Hierarchical supervisor pattern ideal for routing
- Excellent state management across agents
- Built-in streaming for transparency
- Conditional branching for complex workflows
- Strong integration with Claude (Anthropic)

### Key Features Implemented

✅ **Supervisor/Orchestrator Pattern**
- Central supervisor routes queries to specialists
- Intent-based routing logic
- Iteration limits prevent infinite loops

✅ **Specialized Worker Agents (7 agents)**
- Greeter, Academic, Finance, Student Life, IT, Quality Reviewer, Escalation
- Distinct roles with targeted knowledge bases

✅ **Shared State/Memory**
- Query history tracked
- Agent findings accumulated
- Student context preserved
- Escalation flags maintained

✅ **Tool Integration**
- Simulated USIU database (knowledge base)
- Intent classification
- Response validation

✅ **Human-in-the-Loop**
- Quality reviewer can flag for escalation
- Escalation agent provides human contact info
- Reference number generation

✅ **Reflection/Critique Loop**
- Quality reviewer validates all responses
- Checks accuracy, completeness, tone
- Ensures actionable guidance

✅ **Streaming Visibility**
- Real-time agent thought process
- Transparent decision-making
- Debugging capability

✅ **Termination Conditions**
- Maximum iteration limit (5)
- Successful response delivery
- Escalation to human

## 🎯 Challenges & Solutions

### Challenge 1: Agent Coordination Overhead
**Problem:** Multiple agents increase latency
**Solution:** 
- Optimized routing to avoid unnecessary hops
- Limit conversation context to last 3 messages
- Single-pass through specialist agents

### Challenge 2: Knowledge Base Accuracy
**Problem:** Hallucinations when info not in KB
**Solution:**
- Explicit instruction to admit when info unavailable
- Quality reviewer validates against KB
- Clear directive to reference official sources

### Challenge 3: Infinite Loops
**Problem:** Agents could theoretically route endlessly
**Solution:**
- Iteration counter with max limit (5)
- Conditional edges with explicit END states
- Quality reviewer has final say

### Challenge 4: Cost Management
**Problem:** Multiple LLM calls per query
**Solution:**
- Reduced context window (last 3 messages)
- Shorter, focused system prompts
- Single specialist per query path

### Challenge 5: Tone Consistency
**Problem:** Different agents might sound inconsistent
**Solution:**
- Shared tone guidelines in all system prompts
- Quality reviewer checks for professional yet friendly tone
- Greeter sets warm, welcoming atmosphere

## 📈 Advantages Over Single-Agent Approach

### 1. **Domain Expertise**
- **Multi-Agent:** Each agent deeply specialized (finance, IT, academics)
- **Single-Agent:** Jack of all trades, master of none

### 2. **Quality Assurance**
- **Multi-Agent:** Built-in quality review and validation
- **Single-Agent:** No self-critique mechanism

### 3. **Scalability**
- **Multi-Agent:** Easy to add new specialists (e.g., international students agent)
- **Single-Agent:** Monolithic prompt becomes unwieldy

### 4. **Maintainability**
- **Multi-Agent:** Update individual agent knowledge independently
- **Single-Agent:** Changes risk breaking unrelated functionality

### 5. **Transparency**
- **Multi-Agent:** Clear workflow visibility, audit trail
- **Single-Agent:** Black box decision-making

### 6. **Human Escalation**
- **Multi-Agent:** Dedicated escalation logic and agent
- **Single-Agent:** Must handle escalation inline

### 7. **Error Isolation**
- **Multi-Agent:** One agent's error doesn't cascade
- **Single-Agent:** Single point of failure

## 🔮 Future Enhancements

1. **Real Database Integration**
   - Connect to actual USIU student information system
   - Real-time course availability
   - Personal student data (with authentication)

2. **Advanced Tools**
   - Web search for latest USIU news/updates
   - Calendar API for appointment booking
   - Email integration for ticket creation

3. **Memory & Personalization**
   - Remember student preferences across sessions
   - Track common issues per student
   - Personalized recommendations

4. **Analytics Dashboard**
   - Query volume by category
   - Agent performance metrics
   - Escalation rate tracking

5. **Multi-Language Support**
   - Swahili language support
   - Auto-detect student's language preference

6. **Proactive Assistance**
   - Send reminders for deadlines
   - Alert students about relevant events
   - Follow-up on escalated cases

## 📝 Ethical Considerations

- **Privacy**: No real student data stored; designed for authenticated access only
- **Transparency**: Students know they're interacting with AI
- **Human Oversight**: Complex cases always escalated
- **Accuracy**: Quality review prevents misinformation
- **Bias**: Neutral, helpful tone for all students
- **Data Security**: Production version would use encrypted connections

## 📚 Resources Used

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangGraph Multi-Agent Tutorial](https://python.langchain.com/docs/langgraph/tutorials/multi_agent/)
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- DeepLearning.AI: Multi AI Agent Systems with CrewAI
- Academic papers on multi-agent systems architecture

## 👥 Team

**Student Name:** [Your Name]
**Course:** DSA 2020A - Artificial Intelligence
**Institution:** United States International University (USIU)
**Semester:** Spring 2026

## 📄 License

This project is created for educational purposes as part of Lab 2 Assignment.

---

**Note:** This system uses simulated USIU data for demonstration. In production, it would connect to real university databases with proper authentication and security measures.
