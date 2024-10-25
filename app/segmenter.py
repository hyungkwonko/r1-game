import numpy as np
import torch
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

# Dictionary of models with paths and types
models = {
    "small": "app/models/sam_vit_b_01ec64.pth",
    "medium": "app/models/sam_vit_l_0b3195.pth",
    "large": "app/models/sam_vit_h_4b8939.pth",
}
model_types = {"small": "vit_b", "medium": "vit_l", "large": "vit_h"}


def load_model(model_size):
    """
    Loads the SAM model based on the selected size.
    """
    model_type = model_types[model_size]
    sam_checkpoint = models[model_size]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    return SamAutomaticMaskGenerator(sam)


def segment_image(image, model_size="small"):
    """
    Segments the given image using SAM and returns a PIL image with the segmentation overlay.

    Args:
        image (PIL.Image): Input image to be segmented.
        model_size (str): Model size to be used ("small", "medium", or "large").

    Returns:
        PIL.Image: Output image with segmentation overlays.
    """
    print("Segmentation is running with model size:", model_size)
    # Load the appropriate model based on user choice
    mask_generator = load_model(model_size)

    # Convert PIL image to RGB numpy array
    image_rgb = np.array(image.convert("RGB"))

    # Generate masks
    masks = mask_generator.generate(image_rgb)

    # Create a combined mask overlay with an alpha channel
    overlay = np.ones(
        (image_rgb.shape[0], image_rgb.shape[1], 4)
    )  # Initialize RGBA overlay
    overlay[:, :, 3] = 0  # Start with full transparency

    # Overlay each mask with a random color
    for mask_data in masks:
        mask = mask_data["segmentation"]
        color = np.concatenate(
            [np.random.rand(3), [0.7]]
        )  # Random color in RGBA format with 70% opacity
        overlay[mask] = color

    # Convert overlay to RGB image and return
    segmented_image = Image.fromarray((overlay[:, :, :3] * 255).astype(np.uint8))
    return segmented_image
