from huggingface_hub import hf_hub_download

repo = "mattaq/GelGenie-Universal-FineTune-May-2024"
base = "DjangoBackend/gel_models/universal_finetune"

hf_hub_download(
    repo_id=repo,
    filename="config.toml",
    local_dir=base
)

hf_hub_download(
    repo_id=repo,
    filename="checkpoints/checkpoint_epoch_590.pth",
    local_dir=base
)