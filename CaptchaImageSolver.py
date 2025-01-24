import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import base64
import time
import openai
from PIL import Image

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1"
    # base_url="https://api.openai.com/v1/chat/completions" # If you want to use ChatGPT API
)

request_delay = 1 # Delay in seconds between requests

class CaptchaImageSolver:
    def __init__(self):
        pass

    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def send_llm_request(self, prompt, image_path):
        B64_IMAGE = self.image_to_base64(image_path)
        completion = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # Specify the model you want to use
            messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"data:image/png;base64,{B64_IMAGE}"}
            ]
        )
        return completion

    def count_grids(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        
        # Determine the grid size by analyzing the image
        # Assuming the grid lines are black and 1 pixel wide
        horizontal_lines = []
        vertical_lines = []

        y_start = 165
        x_start = 20

        is_white_sequence = False
        for y in range(y_start, height - 130):
            if image.getpixel((x_start, y)) == (255, 255, 255):
                if not is_white_sequence:
                    horizontal_lines.append(y)
                    is_white_sequence = True
            else:
                is_white_sequence = False
                
        is_white_sequence = False
        for x in range(x_start, width - 10):
            if image.getpixel((x, y_start + 10)) == (255, 255, 255):
                if not is_white_sequence:
                    vertical_lines.append(x)
                    is_white_sequence = True
            else:
                is_white_sequence = False

        grid_size = min(len(horizontal_lines), len(vertical_lines)) + 1
        grid_width = width // grid_size if grid_size > 0 else width
        grid_height = height // grid_size if grid_size > 0 else height

        return grid_size, grid_width, grid_height

    def solve_captcha_image(self, image_path):
        grid_size, grid_width, grid_height = self.count_grids(image_path)

        prompt = f"""
        **Task: Solve Google reCAPTCHA v2 Image Grid**
        I will provide you with a Google reCAPTCHA v2 image grid. Your task is to help me solve it.
        - You will see a {grid_size}x{grid_size} grid of images.
        - First index is the row and second index is the column.
        - Grid indexes start from 0 and increase from left to right and top to bottom.
        - The top-left image is labeled as (0,0) and the bottom-right image is labeled as ({grid_size-1},{grid_size-1}).
        - Your goal is to identify the images that contain a part of the specific object, then provide their coordinates.
        - If you are not sure about an image, you can skip it.
        - If captcha is about selecting all images with a specific object, only search for the specific object itself. Not its shadow or reflection.
        - Do not consider the image in the title bar which is next to text : select all ... .
        - Do not consider the bottom bar which is next to text : verify.
        - If captcha is about selecting all squares with a specific object, provide the coordinates of all squares that contain the object and take object as center, then select all squares that contains connections with that object.
        **Instructions**:  
        - If multiple images contain specific objects, provide the coordinates of each image in the format (x1,y1), (x2,y2), ..., (xn,yn).
        - For example, if the images at (0,1) and (2,1) contain specific objects, your response should be: (0,1), (2,1).
        - Response just the coordinates in the format (x,y), (x,y), ..., (x,y).
        - If there are no images with the specific object, just respond with "no".

        """

        response = self.send_llm_request(prompt, image_path)

        try:
            if response.get("error"):
                print(response["error"])
                # Error: "The model is not available at the moment. Please try again later."
                time.sleep(request_delay)
                return self.solve_captcha_image(image_path)
        except:
            pass

        try:
            return response.choices[0].message["content"], grid_size
        except:
            return response, grid_size