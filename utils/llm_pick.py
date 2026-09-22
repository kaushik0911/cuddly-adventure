from langchain_ollama import OllamaLLM

def pick_llm(level: str="low") -> OllamaLLM:
    """
    Picks the appropriate LLM based on the provided level.

    Args:
        level (str): The level of the LLM to pick. Can be "low", "intermediate", or "advanced".

    Returns:
        OllamaLLM: The selected LLM instance.
    """
    llm_mapping = {
        "low": "llama3.2:latest",
        "intermediate": "llama3.2:latest",
        "advanced": "llama3.2:latest"
    }

    llm = OllamaLLM(model=llm_mapping.get(level, "low"), temperature=0)  # Create an instance of the selected LLM with specified parameters

    return llm  # Return the selected LLM instance if level is recognized, otherwise return BasicLLM

if __name__ == "__main__":
    # Example usage
    selected_llm = pick_llm("intermediate")
    print(f"Selected LLM: {selected_llm.model}")
    print(selected_llm.invoke("What is the capital of Austria?"))  # Example invocation of the selected LLM