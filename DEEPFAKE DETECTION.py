# ============================================================
# PROJECT: DEEPFAKE DETECTION
# Platform: Google Colab
# Language: Python
# Author: Deepfake Detection Project
# Description: Multi-model ensemble system to detect AI-generated
#              or manipulated face images/videos using CNNs,
#              Frequency Analysis, and Texture Analysis.
# ============================================================

# ============================================================
# CELL 1: INSTALL DEPENDENCIES
# ============================================================
# Run this cell first in Google Colab

"""
!pip install -q torch torchvision
!pip install -q opencv-python-headless
!pip install -q facenet-pytorch
!pip install -q timm
!pip install -q scikit-image
!pip install -q matplotlib seaborn
!pip install -q Pillow
!pip install -q tqdm
!pip install -q albumentations
"""

# ============================================================
# CELL 2: IMPORTS
# ============================================================

import os
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from PIL import Image
from tqdm import tqdm
from skimage.feature import local_binary_pattern
from facenet_pytorch import MTCNN
import timm
import warnings

warnings.filterwarnings("ignore")

# Check device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {DEVICE}")
if torch.cuda.is_available():
    print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")

# ============================================================
# CELL 3: CONFIGURATION
# ============================================================

class Config:
    """Central configuration for the Deepfake Detection project."""

    # Image settings
    IMAGE_SIZE     = 224           # Input size for CNN models
    FACE_MARGIN    = 40            # Pixels to expand around detected face
    MIN_FACE_SIZE  = 80            # Minimum face size to analyze (pixels)

    # Model settings
    CNN_MODEL_NAME = "efficientnet_b3"  # timm model name
    CNN_CONFIDENCE_THRESHOLD = 0.5      # >= this → FAKE

    # Frequency analysis
    FFT_THRESHOLD  = 0.15          # High-frequency energy threshold

    # LBP texture analysis
    LBP_RADIUS     = 3
    LBP_N_POINTS   = 24
    LBP_THRESHOLD  = 0.35          # Uniformity threshold

    # Ensemble weights (must sum to 1.0)
    WEIGHT_CNN       = 0.60
    WEIGHT_FFT       = 0.20
    WEIGHT_TEXTURE   = 0.20

    # Grad-CAM layer name
    GRADCAM_LAYER    = "blocks"     # Target layer for EfficientNet

    # Output
    SAVE_RESULTS   = True
    OUTPUT_DIR     = "deepfake_results"


cfg = Config()
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
print("[INFO] Configuration loaded.")

# ============================================================
# CELL 4: FACE DETECTOR
# ============================================================

class FaceDetector:
    """
    Detects and crops faces from images using MTCNN (Multi-task CNN).
    Falls back to full-image analysis if no face is found.
    """

    def __init__(self, device=DEVICE):
        self.detector = MTCNN(
            keep_all=True,
            device=device,
            min_face_size=cfg.MIN_FACE_SIZE,
            thresholds=[0.6, 0.7, 0.7]
        )
        print("[INFO] Face detector (MTCNN) initialized.")

    def detect_faces(self, image: np.ndarray):
        """
        Returns list of cropped face arrays from an image.

        Args:
            image: BGR numpy array (OpenCV format)
        Returns:
            List of face crops (numpy arrays in RGB)
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        boxes, probs = self.detector.detect(pil_image)

        faces = []
        face_boxes = []

        if boxes is not None:
            h, w = image.shape[:2]
            for box, prob in zip(boxes, probs):
                if prob < 0.85:
                    continue
                x1, y1, x2, y2 = [int(v) for v in box]
                # Add margin
                x1 = max(0, x1 - cfg.FACE_MARGIN)
                y1 = max(0, y1 - cfg.FACE_MARGIN)
                x2 = min(w, x2 + cfg.FACE_MARGIN)
                y2 = min(h, y2 + cfg.FACE_MARGIN)

                face_crop = rgb_image[y1:y2, x1:x2]
                if face_crop.size > 0:
                    faces.append(face_crop)
                    face_boxes.append((x1, y1, x2, y2))

        if not faces:
            # Fallback: analyze entire image
            faces = [rgb_image]
            face_boxes = [(0, 0, image.shape[1], image.shape[0])]
            print("[WARNING] No face detected — analyzing full image.")

        return faces, face_boxes


# ============================================================
# CELL 5: CNN DEEPFAKE DETECTOR (EfficientNet)
# ============================================================

class CNNDeepfakeDetector(nn.Module):
    """
    EfficientNet-B3 based binary classifier.
    Output: probability of being FAKE (0 = Real, 1 = Fake).
    """

    def __init__(self, model_name=cfg.CNN_MODEL_NAME, pretrained=True):
        super(CNNDeepfakeDetector, self).__init__()
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,      # Remove classification head
            global_pool="avg"
        )
        in_features = self.backbone.num_features
        self.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        features = self.backbone(x)
        return self.classifier(features)

    def predict(self, image_tensor: torch.Tensor) -> float:
        """Returns fake probability for a single image tensor."""
        self.eval()
        with torch.no_grad():
            image_tensor = image_tensor.unsqueeze(0).to(DEVICE)
            prob = self.forward(image_tensor).item()
        return prob


def get_cnn_transform():
    """Returns image preprocessing transforms for CNN inference."""
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((cfg.IMAGE_SIZE, cfg.IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


# ============================================================
# CELL 6: FREQUENCY ANALYSIS (FFT)
# ============================================================

class FrequencyAnalyzer:
    """
    Analyzes frequency domain artifacts in images.
    Deepfakes often leave characteristic high-frequency patterns
    in the Fourier spectrum due to GAN upsampling artifacts.
    """

    def analyze(self, face_image: np.ndarray) -> dict:
        """
        Args:
            face_image: RGB numpy array
        Returns:
            dict with 'fake_score' (0-1) and 'spectrum' (visualizable FFT)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY).astype(np.float32)

        # Apply FFT
        f_transform = np.fft.fft2(gray)
        f_shifted   = np.fft.fftshift(f_transform)
        magnitude   = np.abs(f_shifted)
        log_spectrum = np.log1p(magnitude)

        # Normalize
        spectrum_norm = log_spectrum / (log_spectrum.max() + 1e-8)

        # Measure high-frequency energy (outer ring of spectrum)
        h, w = spectrum_norm.shape
        cy, cx = h // 2, w // 2
        radius_inner = int(min(h, w) * 0.1)   # Inner 10% = low freq
        radius_outer = int(min(h, w) * 0.45)  # Up to 45% = high freq

        Y, X = np.ogrid[:h, :w]
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)

        inner_mask  = dist < radius_inner
        outer_mask  = (dist >= radius_inner) & (dist <= radius_outer)

        low_freq_energy  = spectrum_norm[inner_mask].mean()
        high_freq_energy = spectrum_norm[outer_mask].mean()

        # Ratio: deepfakes tend to have elevated high-freq artifacts
        ratio = high_freq_energy / (low_freq_energy + 1e-8)

        # Normalize to 0-1 fake score
        fake_score = float(np.clip(ratio / (cfg.FFT_THRESHOLD * 10), 0, 1))

        return {
            "fake_score": fake_score,
            "spectrum":   spectrum_norm,
            "hf_energy":  float(high_freq_energy),
            "lf_energy":  float(low_freq_energy),
            "ratio":      float(ratio)
        }


# ============================================================
# CELL 7: TEXTURE ANALYSIS (LBP)
# ============================================================

class TextureAnalyzer:
    """
    Analyzes texture consistency using Local Binary Patterns (LBP).
    Deepfakes often show unnatural texture smoothness or
    inconsistency compared to real facial textures.
    """

    def analyze(self, face_image: np.ndarray) -> dict:
        """
        Args:
            face_image: RGB numpy array
        Returns:
            dict with 'fake_score' (0-1) and 'lbp_map'
        """
        gray = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
        gray_resized = cv2.resize(gray, (cfg.IMAGE_SIZE, cfg.IMAGE_SIZE))

        # Compute LBP
        lbp = local_binary_pattern(
            gray_resized,
            P=cfg.LBP_N_POINTS,
            R=cfg.LBP_RADIUS,
            method="uniform"
        )

        # Compute LBP histogram
        n_bins = cfg.LBP_N_POINTS + 2
        hist, _ = np.histogram(lbp.ravel(), bins=n_bins,
                               range=(0, n_bins), density=True)

        # Uniformity measure — real faces have more varied textures
        uniformity = np.sum(hist ** 2)  # High = uniform = potentially fake

        # Variance of LBP values — low variance = too smooth = fake signal
        lbp_variance = np.var(lbp)
        variance_score = float(np.clip(1.0 - (lbp_variance / 500.0), 0, 1))

        # Combined fake score
        fake_score = float(np.clip(
            0.5 * uniformity / cfg.LBP_THRESHOLD +
            0.5 * variance_score, 0, 1
        ))

        return {
            "fake_score":    fake_score,
            "lbp_map":       lbp,
            "uniformity":    float(uniformity),
            "lbp_variance":  float(lbp_variance)
        }


# ============================================================
# CELL 8: GRAD-CAM VISUALIZATION
# ============================================================

class GradCAM:
    """
    Generates Gradient-weighted Class Activation Maps to highlight
    which regions influenced the CNN's prediction.
    """

    def __init__(self, model: nn.Module, target_layer_name: str):
        self.model = model
        self.gradients = None
        self.activations = None
        self._hook_layer(target_layer_name)

    def _hook_layer(self, layer_name: str):
        """Attach forward and backward hooks."""
        for name, module in self.model.named_modules():
            if layer_name in name:
                module.register_forward_hook(self._save_activation)
                module.register_backward_hook(self._save_gradient)
                print(f"[INFO] Grad-CAM hooked to layer: {name}")
                return
        print(f"[WARNING] Layer '{layer_name}' not found. Grad-CAM disabled.")

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, image_tensor: torch.Tensor) -> np.ndarray:
        """
        Args:
            image_tensor: preprocessed tensor (C, H, W)
        Returns:
            heatmap as numpy array (H, W), values 0-1
        """
        self.model.eval()
        img_batch = image_tensor.unsqueeze(0).to(DEVICE)
        img_batch.requires_grad_(True)

        output = self.model(img_batch)
        self.model.zero_grad()
        output.backward()

        if self.gradients is None or self.activations is None:
            return np.zeros((cfg.IMAGE_SIZE, cfg.IMAGE_SIZE))

        # Pool gradients over spatial dimensions
        pooled_grads = torch.mean(self.gradients, dim=[0, 2, 3])

        # Weight activations by pooled gradients
        activations = self.activations[0]
        for i in range(activations.shape[0]):
            activations[i, :, :] *= pooled_grads[i]

        heatmap = activations.mean(dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0)  # ReLU
        heatmap /= (heatmap.max() + 1e-8)

        # Resize to original image size
        heatmap = cv2.resize(heatmap, (cfg.IMAGE_SIZE, cfg.IMAGE_SIZE))
        return heatmap


# ============================================================
# CELL 9: ENSEMBLE PREDICTOR
# ============================================================

class DeepfakeEnsemble:
    """
    Combines CNN, Frequency, and Texture analyzers via weighted voting
    to produce a final Fake/Real prediction with confidence score.
    """

    def __init__(self):
        print("[INFO] Initializing CNN model...")
        self.cnn_model    = CNNDeepfakeDetector().to(DEVICE)
        self.transform    = get_cnn_transform()
        self.fft_analyzer = FrequencyAnalyzer()
        self.lbp_analyzer = TextureAnalyzer()
        self.gradcam      = GradCAM(self.cnn_model, cfg.GRADCAM_LAYER)
        print("[INFO] All analyzers ready.")

    def load_weights(self, checkpoint_path: str):
        """Load pretrained CNN weights from a .pth file."""
        if os.path.exists(checkpoint_path):
            state_dict = torch.load(checkpoint_path, map_location=DEVICE)
            self.cnn_model.load_state_dict(state_dict)
            self.cnn_model.eval()
            print(f"[INFO] Loaded weights from {checkpoint_path}")
        else:
            print(f"[WARNING] No checkpoint at {checkpoint_path}. Using random weights.")
            print("[WARNING] Results will be unreliable. Please train or provide weights.")

    def predict_face(self, face_image: np.ndarray) -> dict:
        """
        Run full ensemble analysis on a single face crop.

        Args:
            face_image: RGB numpy array of a face
        Returns:
            dict with all analysis results and final prediction
        """
        # --- CNN Analysis ---
        img_tensor = self.transform(face_image)
        cnn_score  = self.cnn_model.predict(img_tensor)

        # Grad-CAM
        heatmap = self.gradcam.generate(img_tensor)

        # --- Frequency Analysis ---
        fft_result = self.fft_analyzer.analyze(face_image)

        # --- Texture Analysis ---
        lbp_result = self.lbp_analyzer.analyze(face_image)

        # --- Ensemble Voting ---
        final_score = (
            cfg.WEIGHT_CNN     * cnn_score          +
            cfg.WEIGHT_FFT     * fft_result["fake_score"] +
            cfg.WEIGHT_TEXTURE * lbp_result["fake_score"]
        )

        prediction = "FAKE" if final_score >= cfg.CNN_CONFIDENCE_THRESHOLD else "REAL"

        return {
            "prediction":    prediction,
            "confidence":    final_score,
            "cnn_score":     cnn_score,
            "fft_score":     fft_result["fake_score"],
            "texture_score": lbp_result["fake_score"],
            "heatmap":       heatmap,
            "spectrum":      fft_result["spectrum"],
            "lbp_map":       lbp_result["lbp_map"]
        }

    def analyze_image(self, image_path: str) -> dict:
        """
        Full pipeline: load image → detect faces → predict each face.

        Args:
            image_path: path to .jpg/.png image
        Returns:
            dict with results per detected face
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        detector    = FaceDetector()
        faces, boxes = detector.detect_faces(image)

        results = []
        for idx, (face, box) in enumerate(zip(faces, boxes)):
            print(f"[INFO] Analyzing face {idx+1}/{len(faces)}...")
            result = self.predict_face(face)
            result["face_box"]  = box
            result["face_image"] = face
            results.append(result)

        return {
            "image_path":   image_path,
            "original_image": image,
            "num_faces":    len(faces),
            "faces":        results
        }


# ============================================================
# CELL 10: VISUALIZATION
# ============================================================

def visualize_results(analysis_result: dict, save_path: str = None):
    """
    Creates a comprehensive visualization of deepfake analysis.
    Shows: original image with bounding boxes, face crops,
    Grad-CAM heatmaps, FFT spectrum, and LBP maps.
    """
    faces   = analysis_result["faces"]
    n_faces = len(faces)

    if n_faces == 0:
        print("[WARNING] No faces to visualize.")
        return

    fig = plt.figure(figsize=(18, 5 * n_faces))
    fig.patch.set_facecolor("#0f0f1a")

    for face_idx, result in enumerate(faces):
        row_offset = face_idx * 5

        # --- Column 1: Original face crop ---
        ax1 = fig.add_subplot(n_faces, 5, row_offset + 1)
        ax1.imshow(result["face_image"])
        ax1.set_title(
            f"Face {face_idx+1}\n{result['prediction']} ({result['confidence']:.1%})",
            color="white", fontsize=11, fontweight="bold"
        )
        color = "#ff4d4d" if result["prediction"] == "FAKE" else "#4dff88"
        for spine in ax1.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(3)
        ax1.tick_params(colors="white")
        ax1.set_facecolor("#0f0f1a")

        # --- Column 2: Grad-CAM Heatmap ---
        ax2 = fig.add_subplot(n_faces, 5, row_offset + 2)
        face_resized = cv2.resize(result["face_image"],
                                  (cfg.IMAGE_SIZE, cfg.IMAGE_SIZE))
        heatmap_colored = cv2.applyColorMap(
            (result["heatmap"] * 255).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        heatmap_rgb = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        overlay = cv2.addWeighted(face_resized, 0.55, heatmap_rgb, 0.45, 0)
        ax2.imshow(overlay)
        ax2.set_title(
            f"Grad-CAM\nCNN: {result['cnn_score']:.1%}",
            color="white", fontsize=10
        )
        ax2.axis("off")
        ax2.set_facecolor("#0f0f1a")

        # --- Column 3: FFT Spectrum ---
        ax3 = fig.add_subplot(n_faces, 5, row_offset + 3)
        ax3.imshow(result["spectrum"], cmap="inferno", origin="lower")
        ax3.set_title(
            f"FFT Spectrum\nScore: {result['fft_score']:.1%}",
            color="white", fontsize=10
        )
        ax3.axis("off")
        ax3.set_facecolor("#0f0f1a")

        # --- Column 4: LBP Texture Map ---
        ax4 = fig.add_subplot(n_faces, 5, row_offset + 4)
        ax4.imshow(result["lbp_map"], cmap="viridis")
        ax4.set_title(
            f"LBP Texture\nScore: {result['texture_score']:.1%}",
            color="white", fontsize=10
        )
        ax4.axis("off")
        ax4.set_facecolor("#0f0f1a")

        # --- Column 5: Score Bar Chart ---
        ax5 = fig.add_subplot(n_faces, 5, row_offset + 5)
        ax5.set_facecolor("#1a1a2e")
        scores  = [result["cnn_score"], result["fft_score"],
                   result["texture_score"], result["confidence"]]
        labels  = ["CNN", "FFT", "LBP", "Final"]
        colors  = ["#6C63FF", "#00D4FF", "#FFD700",
                   "#ff4d4d" if result["prediction"] == "FAKE" else "#4dff88"]
        bars = ax5.barh(labels, scores, color=colors, height=0.5, alpha=0.9)
        ax5.set_xlim(0, 1)
        ax5.axvline(0.5, color="white", linestyle="--", alpha=0.4, linewidth=1)
        ax5.set_xlabel("Fake Probability", color="white", fontsize=9)
        ax5.set_title("Score Breakdown", color="white", fontsize=10)
        ax5.tick_params(colors="white")
        for spine in ax5.spines.values():
            spine.set_edgecolor("#333355")
        for bar, score in zip(bars, scores):
            ax5.text(min(score + 0.02, 0.92), bar.get_y() + bar.get_height() / 2,
                     f"{score:.0%}", va="center", color="white", fontsize=9)

    plt.suptitle(
        f"Deepfake Detection — {analysis_result['image_path']}",
        color="white", fontsize=14, fontweight="bold", y=1.01
    )
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor="#0f0f1a")
        print(f"[INFO] Visualization saved to: {save_path}")

    plt.show()


# ============================================================
# CELL 11: VIDEO ANALYSIS
# ============================================================

def analyze_video(video_path: str,
                  ensemble: DeepfakeEnsemble,
                  sample_fps: int = 2,
                  max_frames: int = 30) -> dict:
    """
    Analyzes a video by sampling frames and running the ensemble
    detector on each detected face.

    Args:
        video_path:  path to .mp4 / .avi video
        ensemble:    initialized DeepfakeEnsemble
        sample_fps:  frames to analyze per second
        max_frames:  maximum number of frames to process
    Returns:
        dict with frame-level and video-level predictions
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps        = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step       = max(1, int(fps / sample_fps))

    print(f"[INFO] Video: {total_frames} frames @ {fps:.1f} FPS")
    print(f"[INFO] Sampling every {step} frames (≈{sample_fps} FPS)")

    detector  = FaceDetector()
    frame_results = []
    frame_idx = 0
    processed = 0

    pbar = tqdm(total=min(max_frames, total_frames // step))
    while cap.isOpened() and processed < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step == 0:
            faces, _ = detector.detect_faces(frame)
            if faces:
                result = ensemble.predict_face(faces[0])
                frame_results.append({
                    "frame":      frame_idx,
                    "prediction": result["prediction"],
                    "confidence": result["confidence"]
                })
                processed += 1
                pbar.update(1)

        frame_idx += 1

    cap.release()
    pbar.close()

    if not frame_results:
        return {"video_path": video_path, "error": "No faces found in video."}

    fake_scores = [r["confidence"] for r in frame_results]
    avg_score   = np.mean(fake_scores)
    fake_frames = sum(1 for r in frame_results if r["prediction"] == "FAKE")
    fake_ratio  = fake_frames / len(frame_results)

    final_prediction = "FAKE" if avg_score >= cfg.CNN_CONFIDENCE_THRESHOLD else "REAL"

    print(f"\n{'='*50}")
    print(f"VIDEO ANALYSIS RESULT: {final_prediction}")
    print(f"  Avg. Fake Score  : {avg_score:.1%}")
    print(f"  Fake Frames      : {fake_frames}/{len(frame_results)} ({fake_ratio:.0%})")
    print(f"{'='*50}\n")

    # Plot timeline
    fig, ax = plt.subplots(figsize=(12, 3))
    frames_list = [r["frame"] for r in frame_results]
    ax.plot(frames_list, fake_scores, color="#6C63FF", linewidth=1.5)
    ax.fill_between(frames_list, fake_scores, alpha=0.2, color="#6C63FF")
    ax.axhline(0.5, color="red", linestyle="--", alpha=0.6, label="Decision boundary")
    ax.set_xlabel("Frame Number")
    ax.set_ylabel("Fake Probability")
    ax.set_title(f"Video Deepfake Score Timeline — {final_prediction} ({avg_score:.1%})")
    ax.set_ylim(0, 1)
    ax.legend()
    plt.tight_layout()
    plt.show()

    return {
        "video_path":      video_path,
        "final_prediction": final_prediction,
        "avg_score":       avg_score,
        "fake_ratio":      fake_ratio,
        "frame_results":   frame_results
    }


# ============================================================
# CELL 12: TRAINING PIPELINE
# ============================================================

def train_cnn_model(train_loader,
                    val_loader,
                    num_epochs: int = 10,
                    learning_rate: float = 1e-4,
                    save_path: str = "deepfake_model.pth"):
    """
    Trains the CNN deepfake detector on a labeled dataset.

    Dataset expected format:
        train/
            real/  ← real face images
            fake/  ← fake/deepfake images
        val/
            real/
            fake/

    Args:
        train_loader: DataLoader for training set
        val_loader:   DataLoader for validation set
        num_epochs:   number of training epochs
        learning_rate: Adam optimizer LR
        save_path:    where to save the best model
    """
    model = CNNDeepfakeDetector().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,
                                  weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=num_epochs
    )
    criterion = nn.BCELoss()

    best_val_acc = 0.0
    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    print(f"[TRAIN] Starting training for {num_epochs} epochs...")

    for epoch in range(num_epochs):
        # ---- Training Phase ----
        model.train()
        train_losses = []
        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
            images = images.to(DEVICE)
            labels = labels.float().unsqueeze(1).to(DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        # ---- Validation Phase ----
        model.eval()
        val_losses = []
        correct = total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(DEVICE)
                labels = labels.float().unsqueeze(1).to(DEVICE)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_losses.append(loss.item())
                preds = (outputs >= 0.5).float()
                correct += (preds == labels).sum().item()
                total   += labels.size(0)

        scheduler.step()
        train_loss_avg = np.mean(train_losses)
        val_loss_avg   = np.mean(val_losses)
        val_acc        = correct / total

        history["train_loss"].append(train_loss_avg)
        history["val_loss"].append(val_loss_avg)
        history["val_acc"].append(val_acc)

        print(f"[Epoch {epoch+1:02d}] "
              f"Train Loss: {train_loss_avg:.4f} | "
              f"Val Loss: {val_loss_avg:.4f} | "
              f"Val Acc: {val_acc:.2%}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), save_path)
            print(f"  → Best model saved (Val Acc: {val_acc:.2%})")

    print(f"\n[TRAIN] Training complete. Best Val Acc: {best_val_acc:.2%}")

    # Plot training history
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    epochs_range = range(1, num_epochs + 1)

    axes[0].plot(epochs_range, history["train_loss"], label="Train Loss", color="#6C63FF")
    axes[0].plot(epochs_range, history["val_loss"],   label="Val Loss",   color="#FF6584")
    axes[0].set_title("Loss Curve")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("BCE Loss")
    axes[0].legend()

    axes[1].plot(epochs_range, history["val_acc"], label="Val Accuracy", color="#4dff88")
    axes[1].axhline(0.9, color="red", linestyle="--", alpha=0.5, label="90% target")
    axes[1].set_title("Validation Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f"{cfg.OUTPUT_DIR}/training_history.png", dpi=120, bbox_inches="tight")
    plt.show()

    return model, history


# ============================================================
# CELL 13: DATASET PREPARATION HELPER
# ============================================================

from torch.utils.data import Dataset, DataLoader

class DeepfakeDataset(Dataset):
    """
    PyTorch Dataset for deepfake detection.

    Folder structure:
        root_dir/
            real/  → label 0
            fake/  → label 1
    """

    EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    def __init__(self, root_dir: str, transform=None):
        self.transform = transform or get_cnn_transform()
        self.samples   = []

        for label, subfolder in enumerate(["real", "fake"]):
            folder_path = os.path.join(root_dir, subfolder)
            if not os.path.isdir(folder_path):
                print(f"[WARNING] Missing folder: {folder_path}")
                continue
            for fname in os.listdir(folder_path):
                if os.path.splitext(fname)[1].lower() in self.EXTENSIONS:
                    self.samples.append((
                        os.path.join(folder_path, fname),
                        label
                    ))

        print(f"[INFO] Dataset loaded: {len(self.samples)} samples "
              f"(real + fake) from {root_dir}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        tensor = self.transform(image)
        return tensor, label


def create_dataloaders(train_dir: str,
                       val_dir: str,
                       batch_size: int = 32,
                       num_workers: int = 2):
    """
    Creates training and validation DataLoaders.

    Args:
        train_dir:   path to training data root
        val_dir:     path to validation data root
        batch_size:  images per batch
        num_workers: parallel data loading workers
    """
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((cfg.IMAGE_SIZE + 32, cfg.IMAGE_SIZE + 32)),
        transforms.RandomCrop(cfg.IMAGE_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    train_ds = DeepfakeDataset(train_dir, transform=train_transform)
    val_ds   = DeepfakeDataset(val_dir)

    train_loader = DataLoader(train_ds, batch_size=batch_size,
                              shuffle=True, num_workers=num_workers)
    val_loader   = DataLoader(val_ds, batch_size=batch_size,
                              shuffle=False, num_workers=num_workers)

    print(f"[INFO] Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")
    return train_loader, val_loader


# ============================================================
# CELL 14: DEMO — RUN INFERENCE
# ============================================================

def run_demo(image_path: str, weights_path: str = None):
    """
    Quick demo function to analyze a single image.

    Usage in Colab:
        from google.colab import files
        uploaded = files.upload()
        image_path = list(uploaded.keys())[0]
        run_demo(image_path)
    """
    print("\n" + "="*55)
    print("  DEEPFAKE DETECTION SYSTEM — INFERENCE DEMO")
    print("="*55)

    # Initialize ensemble
    ensemble = DeepfakeEnsemble()

    # Load pretrained weights if provided
    if weights_path:
        ensemble.load_weights(weights_path)

    # Analyze image
    print(f"\n[INFO] Analyzing: {image_path}")
    analysis = ensemble.analyze_image(image_path)

    # Print summary
    print(f"\n{'─'*40}")
    print(f"  Faces detected : {analysis['num_faces']}")
    for i, face in enumerate(analysis["faces"]):
        verdict = face["prediction"]
        conf    = face["confidence"]
        icon    = "⚠ FAKE" if verdict == "FAKE" else "✓ REAL"
        print(f"  Face {i+1}         : {icon} ({conf:.1%} fake probability)")
        print(f"    CNN score    : {face['cnn_score']:.1%}")
        print(f"    FFT score    : {face['fft_score']:.1%}")
        print(f"    Texture score: {face['texture_score']:.1%}")
    print(f"{'─'*40}\n")

    # Visualize
    save_path = os.path.join(cfg.OUTPUT_DIR,
                             f"result_{os.path.basename(image_path)}.png")
    visualize_results(analysis, save_path=save_path if cfg.SAVE_RESULTS else None)

    return analysis


# ============================================================
# CELL 15: MAIN ENTRY POINT
# ============================================================

# if __name__ == "__main__":
#     print("""
# ╔══════════════════════════════════════════════╗
# ║        DEEPFAKE DETECTION PROJECT            ║
# ║  Platform : Google Colab                     ║
# ║  Language : Python                           ║
# ║  Models   : EfficientNet-B3 + FFT + LBP      ║
# ╚══════════════════════════════════════════════╝

# HOW TO USE:
# -----------
# 1. INFERENCE ON A SINGLE IMAGE:
#    analysis = run_demo("your_image.jpg")

# 2. INFERENCE ON A VIDEO:
#    ensemble = DeepfakeEnsemble()
#    result = analyze_video("your_video.mp4", ensemble)

# 3. TRAIN YOUR OWN MODEL:
#    train_loader, val_loader = create_dataloaders(
#        train_dir="data/train",
#        val_dir="data/val"
#    )
#    model, history = train_cnn_model(
#        train_loader, val_loader, num_epochs=15
#    )

# 4. USE A PRETRAINED MODEL:
#    ensemble = DeepfakeEnsemble()
#    ensemble.load_weights("deepfake_model.pth")
#    analysis = ensemble.analyze_image("test.jpg")

# RECOMMENDED DATASETS:
# ---------------------
# - FaceForensics++ (ff++): https://github.com/ondyari/FaceForensics
# - DFDC (Deepfake Detection Challenge)
# - CelebDF-v2
# - WildDeepfake

# COLAB TIPS:
# -----------
# - Runtime → Change runtime type → GPU (T4)
# - Use Google Drive to persist model weights
# - !gdown <id> to download datasets from Drive
# """)