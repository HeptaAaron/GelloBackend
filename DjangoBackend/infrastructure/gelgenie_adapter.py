# DjangoBackend/infrastructure/gelgenie_adapter.py

from gelgenie.segmentation.evaluation import model_eval_load


def test_gelgenie_import():
    print("GelGenie import works")


def load_test_model(model_folder: str, epoch: str):
    """
    Minimal model loader to verify Torch + GelGenie pipeline.
    """
    print("Loading model...")
    model = model_eval_load(model_folder, epoch)
    print("Model loaded")
    return model
