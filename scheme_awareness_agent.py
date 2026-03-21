import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, RoomInputOptions
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
                - Use simple Hindi or regional language the user is comfortable with
                - Be patient and willing to repeat or explain again
                - Speak slowly and clearly
                - Be encouraging and supportive
                - If you don't know something, say so and suggest official portals
                - Always mention official government portals for verification
                
                Start by greeting the user warmly in Hindi and asking how you can help them.
            """,

            # ✅ FIX 1: Saaras v3 STT - auto language detection
            stt=sarvam.STT(
                language="unknown",
                model="saaras:v3",
                mode="transcribe",
            ),

            # OpenAI LLM brain
            llm=openai.LLM(model="gpt-4o"),

            # ✅ FIX 2: Added encoding="wav" to fix MP3/WAV mismatch error
            tts=sarvam.TTS(
                target_language_code="hi-IN",
                model="bulbul:v3",
                speaker="simran",
                encoding="wav",        # 👈 KEY FIX — forces WAV output
                sample_rate=22050,     # 👈 standard sample rate
            ),
        )

    async def on_enter(self):
        """Called when user joins - agent starts the conversation"""
        await self.session.generate_reply()  # ✅ FIX 3: added await


async def entrypoint(ctx: JobContext):
    """Main entry point"""
    logger.info(f"User connected to room: {ctx.room.name}")

    # ✅ FIX 4: wait for participant before starting session
    await ctx.connect()

    session = AgentSession()

    await session.start(
        agent=GovernmentSchemeAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(),   # 👈 required in newer versions
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))