import instructor
import PIL.Image
import google.generativeai as genai
from openai import OpenAI
from pydantic import BaseModel, Field, HttpUrl, ValidationError
import json
from typing import List, Optional, Dict
import asyncio
import pandas as pd
import yfinance as yf
from app.core.config import settings

# --- Pydantic Models ---
class TextResponse(BaseModel):
    primary_response: str = Field(...)
    image_url: Optional[HttpUrl] = Field(None)
    reference_links: Optional[List[HttpUrl]] = Field(None)
    visualization_spec: Optional[Dict] = Field(None)

class VisionResponse(BaseModel):
    image_description: str = Field(...)
    user_query_answer: str = Field(...)
    identified_objects: List[str] = Field(...)

class FinancialResponse(BaseModel):
    primary_response: str = Field(...)
    visualization_spec: Optional[Dict] = Field(None)

# --- Specialized Agents ---
class FinancialAgent:
    ENTITY_TO_SYMBOL = {"nifty 50": "^NSEI", "nifty50": "^NSEI", "sensex": "^BSESN"}
    
    def _extract_symbol(self, query: str) -> Optional[str]:
        for entity, symbol in self.ENTITY_TO_SYMBOL.items():
            if entity in query.lower(): return symbol
        return None
        
    async def run(self, query: str, system_prompt: str) -> FinancialResponse:
        print("--> FinancialAgent: Running...")
        symbol = self._extract_symbol(query)
        if not symbol: return FinancialResponse(primary_response="I can fetch stock chart data for Nifty 50 and Sensex.")
        
        try:
            ticker = yf.Ticker(symbol)
            hist = await asyncio.to_thread(ticker.history, period="1mo")
            if hist.empty: raise ValueError("No data found for symbol.")

            hist.reset_index(inplace=True)
            chart_values = hist.apply(lambda row: {'date': row['Date'].strftime('%Y-%m-%d'), 'price': row['Close']}, axis=1).tolist()
            latest_price = chart_values[-1]['price']
            
            vega_lite_spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "description": f"Stock price of {symbol}",
                "data": { "values": chart_values }, "mark": "line",
                "encoding": {"x": {"field": "date", "type": "temporal"}, "y": {"field": "price", "type": "quantitative"}}
            }
            
            natural_response = f"Using real-time data from Yahoo Finance, here is the recent performance for {symbol}. The latest closing value was approximately {latest_price:.2f}."
            return FinancialResponse(primary_response=natural_response, visualization_spec=vega_lite_spec)
        except Exception as e:
            return FinancialResponse(primary_response=f"An error occurred while fetching financial data: {e}")


# --- The Main Orchestrator ---
class MetaAgent:
    def __init__(self):
        self.groq_client = instructor.patch(OpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.GROQ_API_KEY), mode=instructor.Mode.JSON)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.financial_agent = FinancialAgent()

    async def _run_text_agent(self, user_query: str, system_prompt: str) -> TextResponse:
        print("--> TextAgent: Running...")
        try:
            response = await asyncio.to_thread(self.groq_client.chat.completions.create, model="llama3-70b-8192", response_model=TextResponse, messages=[{"role": "system", "content": f"You are a world-class data visualization expert and research assistant. **Your most powerful skill is generating Vega-Lite JSON specifications.** When a user asks for a 'chart', 'graph', 'plot', 'diagram', or any other data visualization, you MUST generate a valid Vega-Lite spec in the 'visualization_spec' field. - You can create bar charts, pie charts, scatter plots, etc. - ALWAYS provide a primary text response to accompany the visualization. - User Persona: {system_prompt}"}, {"role": "user", "content": user_query}])
            return response
        except Exception as e:
            return TextResponse(primary_response=f"Sorry, an error occurred: {e}", visualization_spec=None)

    async def run_vision_agent(self, user_query: str, image: PIL.Image.Image, system_prompt: str) -> VisionResponse:
        print("--> VisionAgent: Running...")
        try:
            full_prompt = f"""
            You are an expert multi-modal AI assistant. Analyze the user's image and their query.
            - User's Persona: {system_prompt}
            - User's Query: "{user_query}"
            - **If the user asks to 'ocr', 'read', or 'extract text'**, perform OCR and list the extracted text in the 'user_query_answer' field.
            - **For all other queries**, describe the image and answer the question.
            - You MUST respond with a JSON object that strictly follows this schema: 
            {{"image_description": "A detailed description of the image content.", "user_query_answer": "The specific answer to the user's query, containing the analysis or extracted text.", "identified_objects": ["A list of key objects or concepts identified."]}}
            """
            prompt_parts = [full_prompt, image]
            
            response = await self.vision_model.generate_content_async(
                prompt_parts,
                generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
            )
            
            structured_response = VisionResponse.model_validate_json(response.text)
            print("<-- VisionAgent: Successfully received and parsed response.")
            return structured_response
            
        except Exception as e:
            print(f"<-- VisionAgent: CRITICAL ERROR -> {e}")
            # --- THIS IS THE DEFINITIVE FIX ---
            # ALWAYS return a valid VisionResponse object, even on a catastrophic failure.
            # This prevents the backend from ever returning None and crashing.
            return VisionResponse(
                image_description="A critical error occurred while analyzing the image.",
                user_query_answer=f"I was unable to process this request. The specific error was: {str(e)}",
                identified_objects=["Error"]
            )

    async def run(self, user_query: str, system_prompt: str):
        print(f"MetaAgent: Received query '{user_query}'. Classifying intent...")
        financial_symbols = ['nifty50', 'sensex', 'nifty 50']
        if any(symbol in user_query.lower() for symbol in financial_symbols):
            return await self.financial_agent.run(user_query, system_prompt)
        else:
            return await self._run_text_agent(user_query, system_prompt)

meta_agent_instance = MetaAgent()