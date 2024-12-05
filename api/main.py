import base64
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
app = FastAPI()



load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...), prompt: str = "What's in this image?"):
    try:
        # Read the uploaded file and encode to base64
        image_content = await file.read()
        base64_image = base64.b64encode(image_content).decode('utf-8')

        # Analyze image using OpenAI's vision model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{file.content_type.split('/')[-1]};base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        # Extract and return analysis
        analysis = response.choices[0].message.content
        return JSONResponse(content={"analysis": analysis})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Run server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)