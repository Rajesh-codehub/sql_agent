import streamlit as st
import time
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
import json

# Configure page settings
st.set_page_config(
    page_title="SQL Query Assistant",
    page_icon="🤖",
    layout="wide"
)

# Enhanced CSS with modern design elements
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #6c5ce7, #a363d8);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Output container styling */
    .output-container {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Query box styling */
    .query-box {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6c5ce7, #a363d8);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(108, 92, 231, 0.2);
    }
    
    /* Text area styling */
    .stTextArea > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div:focus-within {
        border-color: #6c5ce7;
        box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Footer styling */
    .footer {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Loading spinner styling */
    .stSpinner > div {
        border-color: #6c5ce7 !important;
    }
    
    /* Custom card component */
    .custom-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_executor' not in st.session_state:
    st.session_state.agent_executor = None


def initialize_agent():
    try:
        with st.spinner('🔄 Initializing SQL Agent...'):
            # Initialize LLM
            llm = Ollama(model="llama3")

            #db_config access

            with open('db_config.json', "r") as file:
                config = json.load(file)
            host = config['host']
            username = config['username']
            password = config['password']
            db_name = config['db_name']
            
            
            
            # Initialize database connection
            # mysql_uri = 'mysql+mysqlconnector://root:Rajubay%40123@localhost:3306/mydb'
            mysql_uri = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{db_name}"
            db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=3)
            
            # Create SQL Agent
            st.session_state.agent_executor = create_sql_agent(
                llm=llm,
                db=db,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
            return True
    except Exception as e:
        st.error(f"🚫 Error initializing agent: {str(e)}")
        return False

# Main UI with enhanced header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🤖 SQL Query Assistant")
st.markdown("""
    Transform your database questions into insights with AI-powered SQL queries.
    Simply describe what you want to know, and let the AI handle the rest.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize button with enhanced styling
if st.session_state.agent_executor is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Initialize SQL Agent", key="init_button"):
            success = initialize_agent()
            if success:
                st.success("✨ SQL Agent initialized successfully!")

# Query input section with enhanced UI
if st.session_state.agent_executor is not None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 💭 Ask Your Question")
    with st.form(key='query_form'):
        query = st.text_area(
            "What would you like to know about your database?",
            height=100,
            placeholder="Example: Which author was born first? | What were the total sales in 2023?"
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🔍 Get Answer")
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle query submission with enhanced visualization
    if submit_button and query:
        try:
            with st.spinner('🤔 Analyzing your question...'):
                # Create expander for showing thinking process
                with st.expander("🔍 View AI Thinking Process", expanded=False):
                    response = st.session_state.agent_executor.invoke(query)
                
                # Display the result in an enhanced format
                st.markdown("### 📊 Result")
                st.markdown('<div class="output-container">', unsafe_allow_html=True)
                st.write(response["output"])
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.markdown("""
                <div class="custom-card">
                    <h4>🔍 Troubleshooting Guide</h4>
                    <ul>
                        <li>Check if your database connection is active</li>
                        <li>Try rephrasing your question</li>
                        <li>Ensure your question is related to the available data</li>
                        <li>Verify that all required services are running</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <h4>🛠️ Powered by</h4>
        <p style='color: #666;'>
            Built with Streamlit, Langchain, and Ollama
        </p>
        <p style='color: #888; font-size: 0.8rem;'>
            Version 2.0 | Made with ❤️ for Data Enthusiasts
        </p>
    </div>
""", unsafe_allow_html=True)

# import streamlit as st
# import time
# from langchain_community.llms import Ollama
# from langchain_community.utilities import SQLDatabase
# from langchain_community.agent_toolkits import create_sql_agent
# from langchain.agents import AgentType

# # Configure page settings
# st.set_page_config(
#     page_title="SQL Query Assistant",
#     page_icon="🤖",
#     layout="wide"
# )

# # Add custom CSS
# st.markdown("""
#     <style>
#     .stApp {
#         max-width: 1200px;
#         margin: 0 auto;
#     }
#     .output-container {
#         background-color: #f0f2f6;
#         border-radius: 10px;
#         padding: 20px;
#         margin: 10px 0;
#     }
#     .query-box {
#         background-color: #ffffff;
#         border-radius: 10px;
#         padding: 20px;
#         margin: 10px 0;
#         border: 1px solid #e0e0e0;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'agent_executor' not in st.session_state:
#     st.session_state.agent_executor = None

# def initialize_agent():
#     try:
#         with st.spinner('Initializing SQL Agent...'):
#             # Initialize LLM
#             llm = Ollama(model="llama3")
            
#             # Initialize database connection
#             mysql_uri = 'mysql+mysqlconnector://root:Rajubay%40123@localhost:3306/mydb'
#             db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=3)
            
#             # Create SQL Agent
#             st.session_state.agent_executor = create_sql_agent(
#                 llm=llm,
#                 db=db,
#                 agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#                 verbose=True
#             )
#             return True
#     except Exception as e:
#         st.error(f"Error initializing agent: {str(e)}")
#         return False

# # Main UI
# st.title("🤖 SQL Query Assistant")
# st.markdown("""
#     This AI assistant helps you query your MySQL database using natural language.
#     Simply type your question, and the AI will generate and execute the appropriate SQL query.
# """)

# # Initialize button
# if st.session_state.agent_executor is None:
#     if st.button("Initialize SQL Agent"):
#         success = initialize_agent()
#         if success:
#             st.success("SQL Agent initialized successfully!")

# # Query input section
# if st.session_state.agent_executor is not None:
#     st.markdown("### Ask Your Question")
#     with st.form(key='query_form'):
#         query = st.text_area(
#             "Enter your question about the database:",
#             height=100,
#             placeholder="Example: Which author was born first?"
#         )
#         submit_button = st.form_submit_button("Get Answer")

#     # Handle query submission
#     if submit_button and query:
#         try:
#             with st.spinner('Analyzing your question...'):
#                 # Create expander for showing thinking process
#                 with st.expander("View thinking process", expanded=False):
#                     response = st.session_state.agent_executor.invoke(query)
                
#                 # Display the result in a nice format
#                 st.markdown("### 📊 Result")
#                 st.markdown('<div class="output-container">', unsafe_allow_html=True)
#                 st.write(response["output"])
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#             st.markdown("""
#                 ℹ️ If you're seeing this error, it might be due to:
#                 - Database connection issues
#                 - Invalid query format
#                 - Timeout in processing
#                 Please try rephrasing your question or check your database connection.
#             """)

# # Add footer
# st.markdown("---")
# st.markdown("""
#     <div style='text-align: center'>
#         <p>Built with Streamlit, Langchain, and Ollama</p>
#     </div>
# """, unsafe_allow_html=True)