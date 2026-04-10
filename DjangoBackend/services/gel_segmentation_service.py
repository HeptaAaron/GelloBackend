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
MINIMUM_BAND_AREA = 50


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
            grayscale_array = self._extract_grayscale_array(padded_batch)
            segmentation_mask = self._run_inference(padded_batch)

            band_labels, band_count = ndi.label(segmentation_mask.argmax(axis=0))
            lanes = self._group_bands_into_lanes(band_labels, band_count)
            lane_count = len(lanes)

            analysis_note = self._generate_analysis_note(
                lanes, band_labels, grayscale_array
            )

            segmentation_rgba = self._create_segmentation_image(
                output_directory, filename, segmentation_mask
            )

            return {
                "image": self._to_base64_png(original_image),
                "processed_image": self._to_base64_png(segmentation_rgba),
                "lane_count": lane_count,
                "table_data": self._build_empty_table(lane_count),
                "note": analysis_note,
            }

    def _load_image_as_batch(self, input_directory):
        dataset = ImageDataset(
            str(input_directory), 1,
            padding=False, individual_padding=True,
            minmax_norm=False, percentile_norm=False,
        )
        dataloader = DataLoader(dataset, shuffle=False, batch_size=1, num_workers=0)
        return next(iter(dataloader))

    def _extract_grayscale_array(self, padded_batch):
        original_height = int(padded_batch["image_height"][0])
        original_width = int(padded_batch["image_width"][0])
        padded_height, padded_width = padded_batch["image"].shape[2], padded_batch["image"].shape[3]

        pad_top = (padded_height - original_height) // 2
        pad_left = (padded_width - original_width) // 2
        pad_bottom = padded_height - original_height - pad_top
        pad_right = padded_width - original_width - pad_left

        full_array = padded_batch["image"].detach().squeeze().cpu().numpy()
        return full_array[pad_top:-pad_bottom, pad_left:-pad_right]

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

    def _group_bands_into_lanes(self, band_labels, band_count):
        if band_count == 0:
            return []

        band_center_x_positions = []
        for band_index in range(1, band_count + 1):
            coords = np.where(band_labels == band_index)
            if len(coords[0]) < MINIMUM_BAND_AREA:
                continue
            band_center_x_positions.append((band_index, np.mean(coords[1])))

        if not band_center_x_positions:
            return []

        band_center_x_positions.sort(key=lambda entry: entry[1])

        image_width = band_labels.shape[1]
        grouping_tolerance = image_width * LANE_GROUPING_TOLERANCE

        lanes = []
        current_lane = [band_center_x_positions[0]]

        for entry in band_center_x_positions[1:]:
            current_mean = np.mean([e[1] for e in current_lane])
            if entry[1] - current_mean < grouping_tolerance:
                current_lane.append(entry)
            else:
                lanes.append(current_lane)
                current_lane = [entry]

        lanes.append(current_lane)
        return lanes

    def _generate_analysis_note(self, lanes, band_labels, grayscale_array):
        if not lanes:
            return "No bands detected."

        image_height = band_labels.shape[0]
        lane_labels = list(string.ascii_uppercase)
        lines = []

        for lane_index, lane_bands in enumerate(lanes):
            if lane_index >= len(lane_labels):
                break

            label = lane_labels[lane_index]
            band_count = len(lane_bands)

            strongest_intensity = 0
            strongest_position_percent = 0

            for band_index, _ in lane_bands:
                band_pixels = np.where(band_labels == band_index)
                band_y_center = np.mean(band_pixels[0])
                position_percent = round(band_y_center / image_height * 100)

                pixel_intensities = grayscale_array[band_pixels]
                integrated_intensity = np.sum(255 - pixel_intensities)

                if integrated_intensity > strongest_intensity:
                    strongest_intensity = integrated_intensity
                    strongest_position_percent = position_percent

            if band_count == 1:
                lines.append(
                    f"Lane {label}: {band_count} band detected, "
                    f"at position {strongest_position_percent}%."
                )
            else:
                lines.append(
                    f"Lane {label}: {band_count} bands detected, "
                    f"strongest at position {strongest_position_percent}%."
                )

        return "\n".join(lines)

    @staticmethod
    def _build_empty_table(lane_count):
        lane_labels = list(string.ascii_uppercase)
        return [
            {"lane": lane_labels[i], "sample": "", "volume": None}
            for i in range(min(lane_count, len(lane_labels)))
        ]

    @staticmethod
    def _to_base64_png(image):
        png_buffer = io.BytesIO()
        image.save(png_buffer, format="PNG")
        return base64.b64encode(png_buffer.getvalue()).decode("utf-8")