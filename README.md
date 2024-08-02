# commercetoolsAgent

This basic example is a Python-based conversational AI agent that interfaces with the commercetools GraphQL API. It uses LangChain for agent functionality and Gradio for the user interface.

## Features

- Interact with Commercetools GraphQL API
- Conversational AI powered by OpenAI's GPT-4
- Memory-enabled chat interface
- Gradio-based web UI for easy interaction

## Prerequisites

- Python 3.7+
- commercetools account and API credentials
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/commercetools-agent.git
   cd llm_to_ctp
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   CTP_API_URL=your_commercetools_api_url
   CTP_AUTH_URL=your_commercetools_auth_url
   CTP_CLIENT_ID=your_client_id
   CTP_CLIENT_SECRET=your_client_secret
   CTP_PROJECT_KEY=your_project_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

To start the CommercetoolsAgent with the Gradio interface:

```python
python main.py
```

This will launch a web interface where you can interact with the agent.

## Class Overview

### CommercetoolsAgent

The main class that sets up the LangChain agent, tools, and Gradio interface.

#### Methods:

- `__init__()`: Initializes the agent, tools, and GraphQL client.
- `_setup_tools()`: Sets up the tools for the agent.
- `_setup_gql_client()`: Initializes the GraphQL client.
- `_get_access_token()`: Retrieves the access token for Commercetools API.
- `_query_commercetools()`: Executes GraphQL queries on the Commercetools API.
- `chat()`: Processes user input and returns the agent's response.
- `launch_gradio_interface()`: Launches the Gradio web interface.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.