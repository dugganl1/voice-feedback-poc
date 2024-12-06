import asyncio
import os
from functools import partial

from anthropic import Anthropic


class FeedbackAnalyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def analyze(self, transcript: str) -> dict:
        """
        Analyze transcribed feedback and generate a structured summary.
        """
        try:
            # Debug prints
            print("Received transcript:", transcript)
            print("Transcript type:", type(transcript))

            loop = asyncio.get_event_loop()
            message = await loop.run_in_executor(
                None,
                partial(
                    self.client.messages.create,
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    system="You are a UX feedback analyst specializing in creating structured, actionable insights from user feedback. Use the pyramid principle to organize the information hierarchically, starting with an executive summary followed by well-categorized details. Ensure the analysis is MECE (Mutually Exclusive, Collectively Exhaustive).",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""Analyze this website feedback and provide a sharp, actionable summary:

                            Feedback: "{transcript}"

                            Please provide:
                            1. **Key Points** (3 max, ordered by importance):
                            • [Bullet points capturing the core message]

                            2. **Recommended Actions** (3 max, ordered by impact):
                            • [Specific, actionable next steps]

                            Be direct and prioritize the most impactful insights. Avoid any unnecessary explanation or context.""",
                        }
                    ],
                ),
            )

            # Debug print
            print("Claude Response:", message.content)

            analysis_text = (
                message.content[0].text
                if isinstance(message.content, list)
                else message.content
            )

            return {"summary": analysis_text, "success": True}

        except Exception as e:
            print("Analysis Error:", str(e))
            return {"success": False, "error": str(e)}
