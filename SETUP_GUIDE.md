# USIU Multi-Agent System - Setup & Troubleshooting Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Detailed Installation](#detailed-installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)
7. [FAQ](#faq)

---

## Quick Start

For those who want to get running immediately:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd usiu-multiagent-chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# 4. Run demo
python usiu_multiagent_system.py
```

---

## Detailed Installation

### Prerequisites

**Required:**
- Python 3.9 or higher
- pip (Python package manager)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

**Optional:**
- Jupyter Notebook (for interactive demo)
- Git (for version control)
- Virtual environment tool (venv, conda, or virtualenv)

### Step 1: Environment Setup

#### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv usiu_venv

# Activate it
# On macOS/Linux:
source usiu_venv/bin/activate

# On Windows:
usiu_venv\Scripts\activate

# Verify activation (you should see (usiu_venv) in prompt)
```

#### Option B: Using conda

```bash
# Create conda environment
conda create -n usiu_env python=3.9

# Activate it
conda activate usiu_env
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "langgraph|langchain|anthropic"
```

**Expected output:**
```
anthropic                 0.25.0
langchain                 0.2.0
langchain-anthropic       0.1.0
langchain-core            0.2.0
langgraph                 0.2.0
```

### Step 3: API Key Configuration

#### Option A: Environment Variable (Temporary)

```bash
# Set for current session only
export ANTHROPIC_API_KEY='sk-ant-api03-...'

# Verify
echo $ANTHROPIC_API_KEY
```

#### Option B: .env File (Recommended)

```bash
# Create .env file in project root
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." > .env

# Add to .gitignore to avoid committing
echo ".env" >> .gitignore
```

#### Option C: System-wide Configuration

**macOS/Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
```powershell
# Add to environment variables
setx ANTHROPIC_API_KEY "sk-ant-api03-..."
```

### Step 4: Verify Installation

```bash
# Test Python imports
python -c "from usiu_multiagent_system import create_usiu_workflow; print('✅ Installation successful!')"
```

---

## Configuration

### Customizing the System

#### 1. Modify Knowledge Base

Edit `usiu_multiagent_system.py` and update `USIU_KNOWLEDGE_BASE`:

```python
USIU_KNOWLEDGE_BASE = {
    "academic": {
        "registration": {
            "deadlines": "Your updated deadlines here",
            # ... add more fields
        }
    },
    # ... other categories
}
```

#### 2. Change LLM Model

```python
# In USIUAgentTeam.__init__()
self.llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",  # Change model here
    temperature=0.3  # Adjust creativity (0.0 = deterministic, 1.0 = creative)
)
```

Available models:
- `claude-opus-4-20250514` (Most capable, slower)
- `claude-sonnet-4-20250514` (Balanced - recommended)
- `claude-haiku-4-20250301` (Fastest, lighter)

#### 3. Adjust Agent Behavior

Modify system prompts in each agent method:

```python
def academic_advisor_agent(self, state: AgentState):
    system_prompt = f"""
    You are the Academic Advisor Agent for USIU.
    
    [Customize this prompt to change agent behavior]
    
    Your tone should be: [friendly/formal/casual]
    Your response length: [concise/detailed/comprehensive]
    """
```

#### 4. Configure Iteration Limits

```python
# In route_after_specialist()
if state.get("iteration_count", 0) > 5:  # Change this number
    return END
```

---

## Running the System

### Method 1: Command Line

**Basic execution:**
```bash
python usiu_multiagent_system.py
```

**Custom query:**
```python
# Modify the bottom of usiu_multiagent_system.py
if __name__ == "__main__":
    my_query = "Your custom question here"
    result = run_usiu_chatbot(my_query)
```

### Method 2: Web Interface

```bash
# Option 1: Direct file open
open usiu_chatbot_interface.html

# Option 2: Local server (for better security)
python -m http.server 8000
# Then open: http://localhost:8000/usiu_chatbot_interface.html
```

### Method 3: Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open usiu_demo.ipynb
# Run cells sequentially
```

### Method 4: Python REPL (Interactive)

```python
from usiu_multiagent_system import run_usiu_chatbot

# Ask questions interactively
while True:
    query = input("Ask USIU Support: ")
    if query.lower() in ['quit', 'exit']:
        break
    run_usiu_chatbot(query)
```

---

## Troubleshooting

### Common Issues

#### 1. "Module not found" Error

**Error:**
```
ModuleNotFoundError: No module named 'langgraph'
```

**Solution:**
```bash
# Verify you're in the correct virtual environment
which python  # Should point to venv

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. API Key Issues

**Error:**
```
anthropic.AuthenticationError: Invalid API key
```

**Solution:**
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Verify key format (should start with 'sk-ant-')
# Get new key from: https://console.anthropic.com/

# Set correctly
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

#### 3. Rate Limit Errors

**Error:**
```
anthropic.RateLimitError: Rate limit exceeded
```

**Solution:**
```python
# Add retry logic in usiu_multiagent_system.py
from anthropic import Anthropic
import time

def call_llm_with_retry(self, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return self.llm.invoke(messages)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

#### 4. Slow Response Times

**Issue:** Queries taking >10 seconds

**Solutions:**

A. **Reduce context window:**
```python
# In create_agent() method
messages.extend(state["messages"][-2:])  # Use 2 instead of 3
```

B. **Use faster model:**
```python
self.llm = ChatAnthropic(model="claude-haiku-4-20250301")
```

C. **Simplify knowledge base:**
```python
# Remove unnecessary details from USIU_KNOWLEDGE_BASE
```

#### 5. Graph Visualization Not Working

**Error:**
```
ImportError: cannot import name 'draw_mermaid_png'
```

**Solution:**
```bash
# Install graphviz
pip install pygraphviz

# On macOS:
brew install graphviz

# On Ubuntu/Debian:
sudo apt-get install graphviz graphviz-dev

# On Windows:
# Download from: https://graphviz.org/download/
```

#### 6. Web Interface Not Loading

**Issue:** HTML file shows blank page

**Solution:**
```javascript
// Check browser console for errors (F12)

// Common fix: CORS issues when loading locally
// Use local server instead:
python -m http.server 8000

// Or use Live Server in VS Code
```

#### 7. Out of Memory Errors

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:**
```python
# Reduce conversation history
messages.extend(state["messages"][-1:])  # Only last message

# Or clear old messages
if len(state["messages"]) > 10:
    state["messages"] = state["messages"][-5:]
```

---

## Advanced Usage

### 1. Adding a New Agent

```python
# Step 1: Create agent method
def library_agent(self, state: AgentState):
    kb = json.dumps(USIU_KNOWLEDGE_BASE.get("library", {}), indent=2)
    system_prompt = f"""You are the Library Agent for USIU.
    
    Knowledge Base:
    {kb}
    """
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(state["messages"][-2:])
    response = self.llm.invoke(messages)
    
    return {
        "messages": [response],
        "current_agent": "library",
        "findings": {**state.get("findings", {}), "library_info": True}
    }

# Step 2: Add to workflow
workflow.add_node("library", agent_team.library_agent)

# Step 3: Add routing logic
workflow.add_conditional_edges(
    "greeter",
    agent_team.route_after_greeter,
    {
        "library": "library",  # Add this line
        # ... existing routes
    }
)
```

### 2. Integrating Real Database

```python
import psycopg2  # or your preferred DB library

class USIUDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="your-db-host",
            database="usiu_db",
            user="your-user",
            password="your-password"
        )
    
    def get_registration_deadlines(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM registration_deadlines WHERE semester='Spring 2026'")
        return cur.fetchall()

# Use in agent:
db = USIUDatabase()
deadlines = db.get_registration_deadlines()
```

### 3. Adding Web Search Tool

```python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

def academic_advisor_agent_with_search(self, state: AgentState):
    # Check KB first
    kb_response = self.get_kb_info(state["user_query"])
    
    # If not found, search web
    if not kb_response:
        search_results = search.run(f"USIU {state['user_query']}")
        return self.format_search_response(search_results)
    
    return kb_response
```

### 4. Implementing Persistent Memory

```python
import json
from pathlib import Path

class StudentMemory:
    def __init__(self, student_id):
        self.student_id = student_id
        self.memory_file = Path(f"memory/{student_id}.json")
        self.load()
    
    def load(self):
        if self.memory_file.exists():
            with open(self.memory_file) as f:
                self.data = json.load(f)
        else:
            self.data = {"queries": [], "preferences": {}}
    
    def save(self):
        self.memory_file.parent.mkdir(exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.data, f)
    
    def add_query(self, query, response):
        self.data["queries"].append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
```

### 5. Deployment to Production

**Using Flask:**

```python
from flask import Flask, request, jsonify
from usiu_multiagent_system import run_usiu_chatbot

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    result = run_usiu_chatbot(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Using Docker:**

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "usiu_multiagent_system.py"]
```

---

## FAQ

### Q: How much does it cost to run?

**A:** With Claude Sonnet 4, approximately $0.04 per query. Costs breakdown:
- Input tokens: ~1500 tokens @ $3/million = $0.0045
- Output tokens: ~800 tokens @ $15/million = $0.012
- Multiple agents: ~3-4 calls per query
- **Total: ~$0.04 per student query**

### Q: Can I use OpenAI models instead?

**A:** Yes, but requires code changes:

```python
from langchain_openai import ChatOpenAI

# Replace in __init__:
self.llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.3
)
```

### Q: How do I limit agent responses to be shorter?

**A:** Add to system prompts:

```python
system_prompt = """
...
IMPORTANT: Keep responses under 150 words. Be concise.
"""
```

### Q: Can this work offline?

**A:** Not with cloud LLMs. For offline:
1. Use local LLM (Ollama, LLaMA)
2. Replace ChatAnthropic with local model client
3. Accept lower quality responses

### Q: How do I log all conversations?

**A:** Add logging:

```python
import logging

logging.basicConfig(
    filename='usiu_chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# In run_usiu_chatbot():
logging.info(f"Query: {user_query}")
logging.info(f"Response: {final_response}")
```

### Q: What's the maximum query length?

**A:** Claude supports ~200k tokens (~150k words), but for efficiency:
- Recommended max: 500 words per query
- System will work with longer queries but slower

### Q: How do I update USIU information?

**A:** Two approaches:

1. **Manual:** Edit `USIU_KNOWLEDGE_BASE` dictionary
2. **Automated:** Load from JSON/database:

```python
import json

with open('usiu_data.json') as f:
    USIU_KNOWLEDGE_BASE = json.load(f)
```

---

## Support & Contributing

**Issues:** Report bugs via GitHub Issues  
**Questions:** Email support@your-domain.com  
**Contributing:** Pull requests welcome!

**Project Structure:**
```
usiu-multiagent-chatbot/
├── usiu_multiagent_system.py    # Main system
├── usiu_chatbot_interface.html  # Web UI
├── usiu_demo.ipynb              # Jupyter demo
├── requirements.txt             # Dependencies
├── README.md                    # Documentation
├── REFLECTION_REPORT.md         # Analysis
├── ARCHITECTURE_DIAGRAM.txt     # Visual guide
└── SETUP_GUIDE.md              # This file
```

---

**Last Updated:** February 2026  
**Version:** 1.0.0  
**License:** Educational Use - Lab Assignment
