import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider



def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Get Configuration Settings
        load_dotenv()
        endpoint = os.getenv("MODEL_ENDPOINT")
        model_deployment = os.getenv("MODEL_NAME")
        api_version = os.getenv("MODEL_API_VERSION")
        file_path = Path(__file__).parent / "speech.wav"
        
        print(f"Endpoint: {endpoint}")
        print(f"Deployment: {model_deployment}")
        print(f"API Version: {api_version}")
        
        # Play the speech file
        playsound(file_path)
        
        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider = token_provider,
            api_version=api_version
        )


        
        # Call model to transcribe audio file
        audio_file = open(file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model=model_deployment,
            file=audio_file,
            response_format="text"
        )

        print(transcription)




    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()