import matplotlib

matplotlib.use("Agg")

import base64
import io
import string
import tempfile
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from torch.utils.data import DataLoader

from gelgenie.segmentation.evaluation import model_eval_load
from gelgenie.segmentation.evaluation.core_functions import (
    model_predict_and_process,
    save_segmentation_map,
)
from gelgenie.segmentation.data_handling.dataloaders import ImageDataset

LANE_GROUPING_TOLERANCE = 0.05


class GelSegmentationService:
    _model = None

    def __init__(self, model_folder: str):
        model_path = Path(model_folder) / "universal_finetune"

        if GelSegmentationService._model is None:
            GelSegmentationService._model = model_eval_load(str(model_path), "590")

        self.model = GelSegmentationService._model
        self.model_name = "universal_finetune"

    def analyze(self, original_image, grayscale_image, filename="input.png"):
        with tempfile.TemporaryDirectory() as temp_root:
            temp_root = Path(temp_root)

            input_directory = temp_root / "input"
            output_directory = temp_root / "output"
            input_directory.mkdir()
            output_directory.mkdir()

            grayscale_image.save(input_directory / filename)

            padded_batch = self._load_image_as_batch(input_directory)
            segmentation_mask = self._run_inference(padded_batch)

            band_labels, band_count = ndi.label(segmentation_mask.argmax(axis=0))
            lane_count = self._count_lanes(band_labels, band_count)

            segmentation_rgba = self._create_segmentation_image(
                output_directory, filename, segmentation_mask
            )

            return {
                "image": self._to_base64_png(original_image),
                "processed_image": self._to_base64_png(segmentation_rgba),
                "lane_count": lane_count,
                "table_data": self._build_empty_table(lane_count),
                "note": None,
            }

    def _load_image_as_batch(self, input_directory):
        dataset = ImageDataset(
            str(input_directory), 1,
            padding=False, individual_padding=True,
            minmax_norm=False, percentile_norm=False,
        )
        dataloader = DataLoader(dataset, shuffle=False, batch_size=1, num_workers=0)
        return next(iter(dataloader))

    def _run_inference(self, padded_batch):
        original_height = int(padded_batch["image_height"][0])
        original_width = int(padded_batch["image_width"][0])
        padded_height, padded_width = padded_batch["image"].shape[2], padded_batch["image"].shape[3]

        pad_top = (padded_height - original_height) // 2
        pad_left = (padded_width - original_width) // 2
        pad_bottom = padded_height - original_height - pad_top
        pad_right = padded_width - original_width - pad_left

        _, segmentation_mask = model_predict_and_process(self.model, padded_batch["image"])
        unpadded_mask = segmentation_mask[:, pad_top:-pad_bottom, pad_left:-pad_right]

        return unpadded_mask

    def _create_segmentation_image(self, output_directory, filename, segmentation_mask):
        (output_directory / self.model_name).mkdir()
        image_stem = Path(filename).stem
        return save_segmentation_map(
            str(output_directory), self.model_name, image_stem, segmentation_mask
        )

    def _count_lanes(self, band_labels, band_count):
        if band_count == 0:
            return 0

        band_center_x_positions = sorted(
            np.mean(np.where(band_labels == band_index)[1])
            for band_index in range(1, band_count + 1)
        )

        image_width = band_labels.shape[1]
        grouping_tolerance = image_width * LANE_GROUPING_TOLERANCE

        lanes = []
        current_lane_centers = [band_center_x_positions[0]]

        for center_x in band_center_x_positions[1:]:
            if center_x - np.mean(current_lane_centers) < grouping_tolerance:
                current_lane_centers.append(center_x)
            else:
                lanes.append(current_lane_centers)
                current_lane_centers = [center_x]

        lanes.append(current_lane_centers)
        return len(lanes)

    @staticmethod
    def _build_empty_table(lane_count):
        lane_labels = list(string.ascii_uppercase)
        return [
            {"lane": lane_labels[i], "probe": "", "volume": None}
            for i in range(min(lane_count, len(lane_labels)))
        ]

    @staticmethod
    def _to_base64_png(image):
        png_buffer = io.BytesIO()
        image.save(png_buffer, format="PNG")
        return base64.b64encode(png_buffer.getvalue()).decode("utf-8")
