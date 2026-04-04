from pathlib import Path

from huggingface_hub import hf_hub_download

repo = "mattaq/GelGenie-Universal-FineTune-May-2024"
project_root = Path(__file__).resolve().parent.parent
model_directory = str(project_root / "gel_models" / "universal_finetune")

hf_hub_download(
    repo_id=repo,
    filename="config.toml",
    local_dir=model_directory,
)

hf_hub_download(
    repo_id=repo,
    filename="checkpoints/checkpoint_epoch_590.pth",
    local_dir=model_directory,
)