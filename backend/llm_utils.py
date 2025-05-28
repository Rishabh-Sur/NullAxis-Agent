from llama_cpp import Llama

llm = Llama(model_path="backend/models/response_generator.gguf", n_ctx=2048)

def query_llm(prompt: str) -> str:
    response = llm(
        prompt=f"[INST] {prompt} [/INST]",
        stop=["</s>"],
        temperature=0.0,
        max_tokens=256,
    )
    return response["choices"][0]["text"].strip()
