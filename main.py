import os
from typing import List, Dict, Any
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import gradio as gr
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


load_dotenv()

class CommercetoolsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.tools = self._setup_tools()
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        self.gql_client = self._setup_gql_client()

    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="CommercetoolsGraphQL",
                func=self._query_commercetools,
                description="Use this tool to query the commercetools GraphQL API for customer information."
            )
        ]

    def _setup_gql_client(self) -> Client:
        transport = RequestsHTTPTransport(
            url=os.getenv('CTP_API_URL'),
            headers={
                'Authorization': f"Bearer {self._get_access_token()}",
                'Content-Type': 'application/json'
            },
            verify=True,
            retries=3,
        )
        return Client(transport=transport, fetch_schema_from_transport=True)

    def _get_access_token(self) -> str:
        auth_url = os.getenv('CTP_AUTH_URL')
        client_id = os.getenv('CTP_CLIENT_ID')
        client_secret = os.getenv('CTP_CLIENT_SECRET')
        
        data = {
            'grant_type': 'client_credentials',
            'scope': f'manage_project:{os.getenv("CTP_PROJECT_KEY")}'
        }
        
        response = requests.post(
            auth_url,
            auth=HTTPBasicAuth(client_id, client_secret),
            data=data
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to get access token. Status code: {response.status_code}, Response: {response.text}")

    def _query_commercetools(self, query: str) -> Dict[str, Any]:
        gql_query = gql(query)
        result = self.gql_client.execute(gql_query)
        return result

    def chat(self, user_input: str) -> str:
        response = self.agent.run(user_input)
        return response

    def launch_gradio_interface(self):
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot(avatar_images=["images/user.png", "images/ct.png"])
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            def user(user_message, history):
                return "", history + [[user_message, None]]

            def bot(history):
                bot_message = self.chat(history[-1][0])
                history[-1][1] = bot_message
                return history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )
            clear.click(lambda: None, None, chatbot, queue=False)

        demo.launch()

if __name__ == "__main__":
    agent = CommercetoolsAgent()
    agent.launch_gradio_interface()