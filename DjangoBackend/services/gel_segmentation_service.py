import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import tempfile

from gelgenie.segmentation.evaluation import model_eval_load
from gelgenie.segmentation.evaluation.core_functions import segment_and_plot


class GelSegmentationService:

    _model = None

    def __init__(self, model_folder: str):
        exp_folder = Path(model_folder) / "universal_finetune"

        if GelSegmentationService._model is None:
            GelSegmentationService._model = model_eval_load(str(exp_folder), "590")

        self.model = GelSegmentationService._model
        self.model_name = "universal_finetune"


    def analyze(self, image, filename: str = "input.png"):
        with tempfile.TemporaryDirectory() as tmpdir:
            tempdir = Path(tmpdir)

            input_dir = tempdir / "input"
            output_dir = tempdir / "output"

            input_dir.mkdir()
            output_dir.mkdir()

            input_path = input_dir / filename

            image.save(input_path)

            segment_and_plot(
                models=[self.model],
                model_names=[self.model_name],
                input_folder=str(input_dir),
                output_folder=str(output_dir),
                multi_augment=False,
                run_classical_techniques=False
            )

            map_files = list(output_dir.rglob("*_map_only.png"))
            if map_files:
                return map_files[0].read_bytes()

            png_files = list(output_dir.rglob("*.png"))
            if not png_files:
                raise RuntimeError("GelGenie hat keine PNG-Ausgabe erzeugt.")

            return png_files[0].read_bytes()