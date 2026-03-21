import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, sarvam

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger("collection-agent")
logger.setLevel(logging.INFO)


class CollectionAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            # Collection agent personality and instructions
            instructions="""
                You are a professional and empathetic collection agent working for ABC Bank.
                
                Customer Account Details:
                - Bank Name: ABC Bank
                - EMI Amount: ₹5,000
                - Due Date: 15th January 2025
                - Loan Type: Personal Loan
                - Account Status: Payment Overdue
                
                Your responsibilities:
                - Remind customers about their pending EMI payment of ₹5,000 which was due on 15th January
                - Provide information about payment due dates, amounts, and available payment methods
                - Help customers understand their payment options and any applicable late fees
                - Guide customers through the payment process if they want to pay immediately
                - Address customer concerns about their account with empathy
                - Offer payment plans or extensions when appropriate (mention that you can connect them with a specialist)
                
                Payment Methods to mention:
                - UPI payment to ABC Bank
                - Net Banking
                - ABC Bank mobile app
                - Visit nearest ABC Bank branch
                
                Communication guidelines:
                - Always maintain a professional yet friendly tone
                - Be empathetic to customer's financial situations
                - Never be aggressive, threatening, or use inappropriate language
                - If a customer is upset, remain calm and understanding
                - Speak clearly and concisely
                - Confirm important details like EMI amount (₹5,000) and due date (15th January)
                - If customer requests to speak to a human, acknowledge and offer to transfer
                
                Start by greeting the customer, introducing yourself as calling from ABC Bank, 
                and politely remind them about their pending EMI of ₹5,000.
            """,
            
            # Saaras v3 STT - Converts speech to text
            stt=sarvam.STT(
                language="unknown",  # Auto-detect language
                model="saaras:v3",
                mode="transcribe"
            ),
            
            # OpenAI LLM - The "brain" that processes and generates responses
            llm=openai.LLM(model="gpt-4o"),
            
            # Bulbul TTS - Converts text to speech
            tts = sarvam.TTS(
                 target_language_code="en-IN",
                 model="bulbul:v3",
                 speaker="ishita",
                 pace=0.9,            # Slightly slower for better understanding
                 speech_sample_rate=24000  # 8000, 16000, 22050, 24000 Hz (default). v3 REST API also supports 32000, 44100, 48000 Hz
                    )
,
        )
    
    async def on_enter(self):
        """Called when user joins - agent starts the conversation"""
        self.session.generate_reply()


async def entrypoint(ctx: JobContext):
    """Main entry point - LiveKit calls this when a user connects"""
    logger.info(f"User connected to room: {ctx.room.name}")
    
    # Create and start the agent session
    session = AgentSession()
    await session.start(
        agent=CollectionAgent(),
        room=ctx.room
    )


if __name__ == "__main__":
    # Run the agent
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
