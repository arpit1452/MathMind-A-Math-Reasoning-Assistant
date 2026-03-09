import streamlit as st
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.tools import Tool

load_dotenv()

st.title("Text To Math Problem Solver using Groq LLaMa")

groq_api=st.sidebar.text_input('Please enter your Groq API Key',type='password')
if not groq_api:
    st.info("Please enter your Groq API Key: ")
    st.stop()

model=ChatGroq(model='llama-3.1-8b-instant',groq_api_key=groq_api)

#Initialize Agents

wikipedia_wrapper=WikipediaAPIWrapper()

wikipedia_tool=Tool(
    name='wikipedia',
    func=wikipedia_wrapper.run,
    description='Useful for searching factual or general knowledge questions about people, history, science, etc.'
)

math_chain=LLMMathChain.from_llm(llm=model)

def math_tool_func(question):
    return math_chain.run(question)

calculator=Tool(
    name='calculator',
    func=math_tool_func,
    description="""Useful for solving math expressions and numerical calculations.
        Input should be a clean math expression like: 4 + 5, 3325 * 456, etc.
        Do NOT input full sentences, only math expressions."""
)

prompt=''' You are an agent Tasked with solving user mathematical problems.
Logically arrive at the solution and display it point wise for the question below:
Question:{question}
Answer:'''

prompt_template=PromptTemplate(template=prompt, input_variables=['question'])

chain=LLMChain(prompt=prompt_template,llm=model)

system_message = """You are a precise math problem solver.
When given a word problem:
1. Read carefully and extract only the numbers and operation needed
2. Use the Calculator tool with ONLY the required math expression
3. Give a clear, direct answer

Do not perform extra calculations. Solve only what is asked."""

Reasoning= Tool(
    name='Reasoning Tool',
    func=chain.run,
    description='A Tool used for answering logic based and reasoning questions'
)

# Build the Agent
assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator, Reasoning],
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": system_message
    }
)

if "messages" not in st.session_state:
    st.session_state['messages']=[
        {'role':'assistant','content':'Hi | I am Math Chatbot who can answer all your Maths Questions'}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

question=st.text_area("Please Ask your Question: ")

if st.button("Find My Answer"):
    if question:
        with st.spinner("Generating Response..."):
            st.session_state.messages.append({'role':'user','content':question})
            st.chat_message('user').write(question)

        if re.search(r'[\d\+\-\*\/\^\(\)]',question):
            response=calculator.run(question)

        else:
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(question,callbacks=[st_cb])
            
        st.session_state.messages.append({'role':'assistant','content':response})
        st.chat_message('assistant').write(response)

    else:
        st.warning("Please Enter the Question")



