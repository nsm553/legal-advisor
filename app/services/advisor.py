import os
import json
from flask import Flask, current_app, jsonify, request, render_template, Blueprint 
from ollama import Client
from app.common import assistant, user, system

ad = Blueprint("advisor", __name__)

DEFAULT_MODEL = "llama3.2:latest"
DEFAULT_URL = "http://localhost:11434"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 0

# @current_app.route("/", methods=["GET"])
ad.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@ad.route("/advisor", methods=["POST"])
def get_advisor():
    """
    Get an advisor based on the provided URL and model.
    [POST] /advisor
    
    Request Body:
        "message" (str): The message to get the advisor for.
        "model" (str): The model to use. Defaults to DEFAULT_MODEL.
        "url" (str): The URL to get the advisor for. Defaults to DEFAULT_URL.
        "temperature" (float): The temperature to use. Defaults to DEFAULT_TEMPERATURE.
        "max_tokens" (int): The max tokens to use. Defaults to DEFAULT_MAX_TOKENS.
    
    Response:
        Streams the response.
    """
    input_data = request.get_json()
    print(f"Input data: {input_data}",  input_data)

    try:
        model = input_data.get("model", DEFAULT_MODEL)
        url = input_data.get("url", DEFAULT_URL)
        temperature = input_data.get(
            "temperature", DEFAULT_TEMPERATURE
        )
        max_tokens = input_data.get(
            "max_tokens", DEFAULT_MAX_TOKENS
        )        
        if "message" not in input_data:
            return jsonify(error="Missing required parameter: message"), 400
                
        # Validate "temperature" if provided
        #
        if temperature:
            try:
                temperature = float(input["temperature"])
                assert temperature >= 0.0
            except Exception:
                return (
                    jsonify({"error": "temperature must be a float superior or equal to 0.0."}),
                    400,
                )

        message = str(input_data.get("message"))
        
        if not message:
            return jsonify(error="Missing required parameter: message"), 400

        messages = [
            assistant("You are a legal advisor. Provide an opinion on the following message."),
            user(message)
        ]

        # client = Client(model=model, url=url)
        # stream = client.chat.stream(messages, temperature=temperature, max_tokens=max_tokens)
        # def generate():
        #     for chunk in stream:
        #         yield chunk["message"]["content"] or ""
        # return response(generate(), mimetype="text/event-stream")
        
        ollama_client = Client(
            # host=os.environ[url]
            host=url
        )

        response = ollama_client.chat(
            model=model.replace("ollama/", ""),
            options={"temperature": temperature},
            format="json",
            messages=messages,
        )

        output = response["message"]["content"]
    
        output = json.loads(output)

    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(output), 200