# Captcha Recognition with CRNN (Minimal Data, High Accuracy)

This project demonstrates how to train a high-accuracy 4-letter CAPTCHA recognition model using a small amount of labeled data. With just **~500 human-labeled CAPTCHA images**, we build a lightweight CRNN model that achieves over **96% test accuracy**.

> ✅ Model trained without using digits – only lowercase English letters (`a`–`z`)

---

## 📂 Project Structure

```bash
.
├── captcha_crnn_training.ipynb      # Full training pipeline (CNN pretrain → CRNN with CTC)
├── single_char_img_generator.py     # Generate single-letter training images with augmentation
├── your_font.ttf                    # Font file for generating single-letter training images
├── captcha_labeling_tool.py         # Manual CAPTCHA labeling tool (Tkinter GUI)
├── single_char_images/              # Output folder for generated single-letter images (200 per letter)
├── single_char_test_images/         # Output folder for generated single-letter images (50 per letter)
├── unlabeled_captchas/              # Input folder for unlabeled CAPTCHAs (before manual labeling)
├── train_captchas/                  # Labeled CAPTCHA images (e.g., abcd.png)
└── test_captchas/                   # Labeled CAPTCHA images (e.g., abcd.png)
````

---

## 🛠️ Requirements

Install the necessary Python packages:

```bash
pip install torch torchvision pillow
```

To use the GUI labeling tool:

```bash
pip install tk
```

> Make sure to also have `SpicyRice-Regular.ttf` font file in the working directory, or update the font path according to your setup.

---

## 🔄 Step 1: Generate Single-Character Images

```bash
python single_char_img_generator.py --font SpicyRice-Regular.ttf --output single_char_images --num_samples 200
```

This will create 200 augmented images for each letter (`a` to `z`) in the `single_char_images/` directory.
Augmentations used:

* Affine transform (±15° rotation, random translation)
* Horizontal & vertical stretch (segment-wise scaling)
* Random erasing (to simulate occlusion)

---

## 🔖 Step 2: Manually Label CAPTCHA Images

1. Place your raw unlabeled CAPTCHA images in the `unlabeled_captchas/` folder. (Must be `.png` and named numerically like `1.png`, `2.png`...)

2. Run the labeling tool:

```bash
python captcha_labeling_tool.py --input unlabeled_captchas --output train_captchas 
```

This will open a simple GUI. For each image:

* Type the correct 4-letter answer (must be lowercase letters)
* Press `Enter` or click **Save**
* The tool will rename the image to `abcd.png` and move it to the output folder, skipping if that name already exists

---

## 🏋️‍♂️ Step 3: Train the CRNN Model

Open the notebook:

```bash
captcha_crnn_training.ipynb
```

The notebook includes:

* **Stage 1**: Train a `SimpleCNN` on the single-letter dataset
* **Stage 2**: Load the pretrained CNN weights into a CRNN (`CNN + BiLSTM + CTC`)
* **Train** on \~500 labeled CAPTCHA images
* Evaluate performance (test accuracy >96%)

> Model input size: `30x100` (for each letter image)
> Full CAPTCHA image: `120x100` (4 letters side by side)

---

## 🧾 Notes

* Uses CTC decoding for final predictions (argmax-based, no external language model)
* Label set includes 26 lowercase letters + 1 blank token (for CTC)
* No digits or uppercase characters

---

## 📈 Example Results

**Test Accuracy**: 96.97% (192/198 correct predictions)
Typical error types: missing/extra characters, slight misalignment.

Example Captchas (ground truth vs prediction):

```
Predict: jqa | GT: ljqa
Predict: rej | GT: reoj
Predict: nui | GT: nuji
```

---

## ⚖️ License

MIT License

---

## 🔗 Related

If you find this project helpful, feel free to ⭐ the repo and share your feedback!

Check out the [Medium article](https://medium.com/@jonathan-kao/high-accuracy-captcha-recognition-model-with-minimal-data-a-full-crnn-training-workflow-d07ce4e57b60) for a detailed explanation of the training strategy and data augmentation design.
