from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from banorte_agent import root_agent


APP_NAME = "banorte_ai_assistant"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def execute_agent(
    message: str,
    user_id: str,
    session_id: str | None = None,
) -> tuple[str, str]:
    current_session_id = session_id or str(uuid4())

    existing_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=current_session_id,
    )

    if existing_session is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=current_session_id,
        )

    user_content = types.Content(
        role="user",
        parts=[
            types.Part(text=message),
        ],
    )

    final_response = "El agente no generó una respuesta."

    async for event in runner.run_async(
        user_id=user_id,
        session_id=current_session_id,
        new_message=user_content,
    ):
        if (
            event.is_final_response()
            and event.content
            and event.content.parts
        ):
            response_parts = [
                part.text
                for part in event.content.parts
                if getattr(part, "text", None)
            ]

            if response_parts:
                final_response = "\n".join(response_parts)

    return current_session_id, final_response

