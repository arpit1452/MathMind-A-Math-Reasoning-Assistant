# MathMind-A-Math-Reasoning-Assistant
MathMind is an AI-powered mathematical reasoning assistant that solves math problems expressed in natural language.
The system combines Groq LLaMA (LLM) with LangChain agents and tool-based computation to interpret questions and produce accurate solutions.
The application provides an interactive chat interface built with Streamlit, enabling users to ask mathematical questions conversationally.

# Demo
Example queries the assistant can solve:
- 3325 * 456
- Solve x^2 - 5x + 6 = 0
- If Ram is twice as old as Shyam and their total age is 36, what are their ages?

# Features
- Natural language math queries
- Arithmetic Calculations
- Algebraic reasoning
- Logical word problem solving
- Tool-based LLM reasoning
- External knowledge retrieval using Wikipedia
- Interactive Streamlit chat interface
- LangChain agent-based architecture

# System Architecture
MathMind uses a Tool-Augmented LLM Architecture where the language model performs reasoning and delegates computations to tools.

''' User
│
▼
Streamlit Chat Interface
│
▼
LangChain Agent
│
▼
Groq LLaMA Model
│
▼
Tool Selection
├── Calculator Tool (LLMMathChain)
├── Wikipedia Knowledge Tool
└── Reasoning Tool (LLMChain)
│
▼
Final Answer Generation
│
▼
Streamlit Chat Output

# Running the Application
- Start the streamlit app
- Live Demo --(https://mathmind-a-math-reasoning-assistant-gpcqkcul7excuenx9dkkbi.streamlit.app/)

# How It Works

-The user enters a math query in the Streamlit interface.
- The LangChain agent sends the query to the Groq LLaMA model.
- The model interprets the problem and determines the required tool.
- The selected tool performs computation or reasoning.
- The final answer is returned and displayed in the chat interface.

# Current Limitations
- Some complex symbolic mathematics may require specialized libraries.
- Mathematical reasoning for advanced equations depends on LLM interpretation.
- Graph visualization for functions is not yet implemented.

# Future Implementations

- Integration with symbolic math engines such as SymPy
- Graph plotting for mathematical functions
- Improved tool routing for mathematical queries
- Step-by-step mathematical solution explanations
