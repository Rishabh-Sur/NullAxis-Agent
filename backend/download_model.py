from huggingface_hub import snapshot_download

# Download model and cache locally
model_path = snapshot_download(repo_id="facebook/bart-large-mnli")
print(f"Model downloaded to: {model_path}")
