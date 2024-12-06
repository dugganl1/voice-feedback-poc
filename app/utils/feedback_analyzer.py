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
            # Run the synchronous API call in a thread pool
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
                            "content": f"""Analyze the following user feedback on a website's user experience and provide a structured, actionable summary:
                        
                        Feedback: {transcript}
                        
                        Output structure:
                        1. **Executive Summary**: A concise 2-3 sentence overview summarizing the key takeaways from the feedback.
                        2. **Positive Aspects**: A list of specific positive comments categorized by themes (e.g., design, navigation, functionality).
                        3. **Areas for Improvement**: A prioritized list of issues or challenges, each clearly defined and grouped into high-level categories (e.g., usability, accessibility, content relevance).
                        4. **Recommendations**: Specific, actionable suggestions to address the identified issues, tied to the themes mentioned.
                        
                        The summary should be clear, professional, and actionable, with insights that are easy for a UX team to understand and implement.""",
                        }
                    ],
                ),
            )

            return {"summary": message.content, "success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}
