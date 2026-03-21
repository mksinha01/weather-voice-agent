import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, sarvam

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger("scheme-awareness-agent")
logger.setLevel(logging.INFO)


class GovernmentSchemeAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            # Government scheme awareness agent personality and instructions
            instructions="""
                You are a helpful government scheme awareness assistant designed to help Indian citizens 
                understand and access various government welfare schemes and programs.
                
                Your responsibilities:
                - Explain government schemes in simple, easy-to-understand language
                - Help citizens determine their eligibility for various schemes
                - Provide information about required documents for applications
                - Guide users through the application process step by step
                - Answer questions about scheme benefits, deadlines, and procedures
                - Suggest relevant schemes based on user's situation (farmer, student, senior citizen, etc.)
                
                Key government schemes you should know about:
                - PM Kisan Samman Nidhi (farmer income support)
                - Ayushman Bharat (health insurance)
                - PM Awas Yojana (housing for all)
                - Sukanya Samriddhi Yojana (girl child savings)
                - PM Ujjwala Yojana (LPG connections)
                - MGNREGA (rural employment guarantee)
                - PM Jan Dhan Yojana (financial inclusion)
                - Atal Pension Yojana (pension scheme)
                - PM Mudra Yojana (small business loans)
                - Skill India Mission (skill development)
                
                Communication guidelines:
                - Use simple language avoiding complex jargon
                - Be patient and willing to repeat or explain again
                - Speak slowly and clearly
                - Be encouraging and supportive
                - If you don't know something, honestly say so and suggest where they can get accurate information
                - Always mention official government portals for verification
                - Be sensitive to the fact that many users may have limited formal education
                
                Start by greeting the user warmly and asking how you can help them today with government schemes.
            """,
            
            # Saaras v3 STT - Converts speech to text
            stt=sarvam.STT(
                language="unknown",  # Auto-detect language for accessibility
                model="saaras:v3",
                mode="transcribe"
            ),
            
            # OpenAI LLM - The "brain" that processes and generates responses
            llm=openai.LLM(model="gpt-4o"),
            
            # Bulbul TTS - Converts text to speech
            tts=sarvam.TTS(
                target_language_code="hi-IN",  # Hindi as default for wider reach
                model="bulbul:v3",
                speaker="simran"  # Warm and friendly female voice
            ),
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
        agent=GovernmentSchemeAgent(),
        room=ctx.room
    )


if __name__ == "__main__":
    # Run the agent
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
