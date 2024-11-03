# Ghost Agent

A powerful AI-assisted research and writing platform that puts humans in the loop. Ghost Agent combines modern AI technologies with human oversight to create a robust system for story development and research.

## 🌟 Features

- **AI-Powered Writing Assistant**: Leverages Google Gemini for sophisticated language understanding and generation
- **Interactive Frontend**: Built with Next.js and CopilotKit for seamless AI interactions
- **Real-time Research**: Integrates Perplexity for up-to-date news and information gathering
- **Human Oversight**: Uses Humanlayer for function calling approval, ensuring human control over AI actions
- **Advanced Monitoring**: Weights & Biases Weave integration for system observability and performance tracking

## 🚀 Tech Stack

### Frontend
- Next.js for a modern, responsive web interface
- CopilotKit for streamlined LLM interactions
- React for component-based UI development

### Backend
- Python with FastAPI for high-performance API endpoints
- Google Gemini AI for advanced language processing
- Perplexity API for real-time research capabilities
- Humanlayer for function call approval workflows
- W&B Weave for system monitoring and debugging

## Prerequisites

- Python 3.8-3.12
- Node.js 16.x or higher
- npm 8.x or higher

## 🛠️ Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:

`python -m venv venv`
`source venv/bin/activate`

2. Install Python dependencies:

`pip install -r requirements.txt`

3. Set up environment variables:

`cp .env.example .env`

Edit the `.env` file with your own values.

### Frontend Setup

1. Install Node.js dependencies:

`npm install`

2. Start the development server:

`npm run dev`

## 🚀 Running Locally

1. Start the backend server:

`python backend/app/main.py`

2. In a new terminal, start the frontend:

`npm run dev`

3. Access the application at `http://localhost:3000`

## 💡 Key Benefits

- **Enhanced Writing Process**: Combine AI capabilities with human creativity
- **Research Automation**: Streamline information gathering with Perplexity integration
- **Quality Control**: Human oversight ensures output quality and accuracy
- **Performance Monitoring**: Track system behavior and optimize performance
- **Scalable Architecture**: Built on modern, scalable technologies
