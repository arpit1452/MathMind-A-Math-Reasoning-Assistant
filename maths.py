import streamlit as st
import re

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.tools import Tool

load_dotenv()

st.title("Text To Math Problem Solver using Groq LLaMa")

groq_api=st.sidebar.text_input('Please enter your Groq API Key',type='password')
if not groq_api:
    st.info("Please enter your Groq API Key: ")
    st.stop()

model=ChatGroq(model='openai/gpt-oss-20b',groq_api_key=groq_api)

#Initialize Agents

wikipedia_wrapper=WikipediaAPIWrapper()

wikipedia_tool=Tool(
    name='wikipedia',
    func=wikipedia_wrapper.run,
    description='Useful for searching factual or general knowledge questions about people, history, science, etc.'
)

def math_tool_func(question):
    try:
        if not re.fullmatch(r'[\d\s+\-*/().]+', question):
            return "Invalid mathematical expression."

        result = eval(question, {"__builtins__": None}, {})
        return str(result)

    except Exception as e:
        return f"Error calculating expression: {e}"

calculator = Tool(
    name='calculator',
    func=math_tool_func,
    description="""Useful for solving mathematical expressions.
    Input should be a clean mathematical expression such as:
    4 + 5
    3325 * 456
    100 / 4
    """
)

prompt = """You are an agent tasked with solving user mathematical problems.

Logically arrive at the solution and display it point wise for the question below:

Question: {question}

Answer:"""

prompt_template = PromptTemplate(
    template=prompt,
    input_variables=["question"]
)

chain = prompt_template | model


def reasoning_tool_func(question):
    response = chain.invoke({"question": question})
    return response.content


Reasoning = Tool(
    name="reasoning_tool",
    func=reasoning_tool_func,
    description="A tool used for answering logic based and reasoning questions."
)

system_message = """You are a precise math problem solver.

When given a word problem:
1. Read carefully and extract only the numbers and operation needed.
2. Use the Calculator tool with ONLY the required math expression.
3. Give a clear, direct answer.

For general knowledge questions, use the Wikipedia tool when appropriate.

Do not perform extra calculations. Solve only what is asked."""

# Build the Agent
assistant_agent = create_agent(
    model=model,
    tools=[wikipedia_tool, calculator, Reasoning],
    system_prompt=system_message
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

        if re.fullmatch(r'(?=.*\d)(?=.*[+\-*/])[\d\s+\-*/().]+', question):

            response = calculator.invoke(question)

        else:

            st_cb = StreamlitCallbackHandler(
                st.container(),
                expand_new_thoughts=False
            )

            result = assistant_agent.invoke(
                {
                    "messages": [
                        ("user", question)
                    ]
                },
                config={
                    "callbacks": [st_cb]
                }
            )

            response = result["messages"][-1].content
            
        st.session_state.messages.append({'role':'assistant','content':response})
        st.chat_message('assistant').write(response)

    else:
        st.warning("Please Enter the Question")


