import os

huggingface_config = {
    # Only required for private models from Huggingface (e.g. LLaMA models)
    "TOKEN": os.environ.get("HF_TOKEN", None)
}

openai_config = {
    "API_KEY": os.environ.get("OPENAI_API_KEY", None)
}