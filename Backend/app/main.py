from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Dict
from pydantic import BaseModel
import requests
load_dotenv()  # Load environment variables
import json
# from shapely.geometry import Polygon
from models import init_db
from models import ChatHistory, SessionLocal
init_db()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Polygon(BaseModel):
    vertices: List[Dict[str, float]]
class RequestBody(BaseModel):
    chatId: int
    prompt: str
    vertices: list
def call_chat_gpt_api(chatId, prompt, polygon_area):
        # Attempt to convert polygon_area to a float if it's a string, then check if it's greater than 0
        try:
            # Convert to float, this will not change the value if it's already a float
            polygon_area_float = float(polygon_area)
            # Check if the converted float is greater than 0
            if polygon_area_float > 0:
                area_message = f"By the way, the area of your current polygon is {polygon_area_float} square units."
            else:
                # Handle case where polygon_area is a float but not greater than 0
                area_message = "The area of your polygon cannot be calculated as the drawn shape is not valid. Please ensure you have drawn a closed polygon with at least 3 points."
        except ValueError:
            # Handle case where polygon_area cannot be converted to float, implying it's an invalid string
            area_message = "The area of your polygon cannot be calculated as the drawn shape is not valid or the area has not been provided correctly. Please ensure you have drawn a closed polygon with at least 3 points."

        # System prompt to OpenAI GPT, incorporating the polygon area
        # Adjust the prompt according to the validity of the polygon area
        system_prompt = f"""
        Welcome to the Polygon Drawing Tool!

        Getting Started:
        - Start Drawing: Click on the 'Start Drawing' button to begin creating your polygon. You'll enter drawing mode, allowing you to click on the canvas to place vertices.
        - Placing Points: Click anywhere on the canvas to place the corners (vertices) of your polygon. You need to place at least 3 points to form a valid polygon.
        - Finishing Your Polygon: After placing at least 3 points, close the polygon by clicking on the first point again or press the 'Finish Drawing' button. Your polygon will automatically close and display on the canvas.
        - Reset Drawing: If you want to start over at any point, simply click the 'Reset' button. This will clear the canvas and allow you to begin a new polygon.

        Using the Chatbot:
        - Ask Questions: If you have any questions about how to use the tool, encounter issues, or need information about the polygon you've drawn, feel free to ask our chatbot for help. Simply type your question into the chatbox and press enter.
        - Examples of Questions: Feel free to ask questions like "How do I start a new polygon?" or "What can I do if my polygon doesn't look right?"

        Please note:
        - The chatbot is designed to answer questions related to the interface or the polygon drawing process only. Questions outside these topics, such as unrelated general knowledge or personal inquiries, cannot be addressed by the chatbot.
        - If the area of your polygon appears as not valid or if you encounter any error messages regarding the polygon area, please do not attempt to calculate it manually or ask the chatbot for mathematical explanations. Instead, ensure your polygon is correctly drawn and try again.

        Tips:
        - Make sure to click carefully to place your points accurately.
        - You can always ask the chatbot for tips on creating better polygons or for clarification on any of the tool's features.

        Feedback:
        - Your experience is important to us. If you have suggestions on how to improve this tool or the chatbot, please let us know through the feedback option.

        Thank you for using our Polygon Drawing Tool. Happy drawing!

        {polygon_area}

        Please type your question below:
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Fetch the last five Q&A pairs and append them to the messages
        last_five_qa_pairs = get_last_five_chats(chatId)
        for pair in last_five_qa_pairs:
            messages.append({"role": "user", "content": pair.prompt})  
            messages.append({"role": "assistant", "content": pair.completion})  
        
        
        messages.append({
            "role": "user",
            "content": prompt
        })

        # Adding the user's question to the prompt
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json',
        }

        payload = {
            'model': 'gpt-3.5-turbo-16k',
            'messages': messages,
            'temperature': 0.7,  
            'max_tokens': 150  
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=50)
        response_json = response.json()
        completion_content = response_json['choices'][0]['message']['content']
        save_chat_history(chatId, prompt, completion_content)
        return response_json

def save_chat_history(chatId, prompt, completion):
    db = SessionLocal()
    chat_history = ChatHistory(chatId=chatId, prompt=prompt, completion=completion)
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)
    db.close()
    return chat_history

def get_last_five_chats(chatId):
    db = SessionLocal()
    last_three_chats = db.query(ChatHistory).filter(ChatHistory.chatId == chatId).order_by(ChatHistory.id.asc()).limit(5).all()
    db.close()
    return last_three_chats
def get_chat(chatId):
    db = SessionLocal()
    last_three_chats = db.query(ChatHistory).filter(ChatHistory.chatId == chatId).order_by(ChatHistory.id.desc()).limit(50).all()
    db.close()
    return last_three_chats
def calculate_polygon_area_from_list(points_list):
    """
    Calculates the area of a polygon given a list of dictionaries representing the points
    using the shoelace formula.
    
    Parameters:
    - points_list (list of dicts): A list of dictionaries with 'x' and 'y' as keys representing points of the polygon.
    
    Returns:
    - float: The area of the polygon.
    """
    
    if len(points_list) < 3:
        return "The points provided are not enough to form a valid polygon."

    # Convert list of dictionaries to list of tuples for easier manipulation
    points = [(point["x"], point["y"]) for point in points_list]

    # Apply the shoelace formula
    sum1 = sum(x * points[(i + 1) % len(points)][1] for i, (x, y) in enumerate(points))
    sum2 = sum(y * points[(i + 1) % len(points)][0] for i, (x, y) in enumerate(points))
    area = abs(sum1 - sum2) / 2.0

    return f"The area of the polygon is {area} square units."


@app.post("/completion/")
async def calculate_area(body: RequestBody):
    
    chatId = body.chatId
    prompt = body.prompt
    vertices = body.vertices
    polygon_area= calculate_polygon_area_from_list(vertices)
    return call_chat_gpt_api(chatId, prompt, polygon_area)
@app.get("/chat-history/{chatId}")
async def get_chat_history(chatId: int):
    chats = get_chat(chatId)
    return chats