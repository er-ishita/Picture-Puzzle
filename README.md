# 🧩 Hand Gesture Picture Puzzle

An interactive **computer vision puzzle game** built with **OpenCV, NumPy,Mediapipe and hand tracking**.  
The program captures a picture using hand gestures, divides it into a **3×3 puzzle**, shuffles the pieces, and lets you **solve the puzzle using your hands**.

No mouse. No keyboard. Just your hands and a camera.

---

## 🚀 Features

- 📸 Capture a picture using **two-hand pinch gesture**
- 🧩 Automatically converts the image into a **3×3 puzzle**
- 🔀 Randomly shuffles puzzle tiles
- ✋ Swap puzzle pieces using **hand gestures**
- ⏱ Displays **time taken to solve the puzzle**
- 🔄 Reset puzzle anytime

---

## 🛠 Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **MediaPipe (via custom handTrackingModule)**

---

## 📂 Project Structure

```
Picture-Puzzle/
│
├── main.py
├── handTrackingModule.py
├── start.png
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/er-ishita/Picture-Puzzle
cd hand-gesture-puzzle
```

### 2️⃣ Install dependencies

```bash
pip install opencv-python numpy mediapipe
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🎮 How to Play

### Step 1: Capture Image
1. Show **both hands** to the camera.
2. Create a **rectangle using both thumbs**.
3. Perform a **pinch gesture** (thumb + index finger on both hands).
4. The selected region will be captured.

### Step 2: Puzzle Starts
- The captured image is split into **9 tiles**.
- Tiles are **randomly shuffled**.

### Step 3: Swap Pieces
1. Place your **thumbs over two puzzle tiles**.
2. Perform a **pinch gesture with both hands**.
3. The tiles will **swap positions**.

### Step 4: Solve
Rearrange tiles until the original image is restored.

When solved:

```
Yayy, you solved it in: X seconds
```

---

## 🎛 Controls

| Key | Action |
|----|------|
| `q` | Quit the program |
| `r` | Reset puzzle |

---

## 🧠 How It Works

### 1️⃣ Hand Tracking
`handTrackingModule` detects hand landmarks using **MediaPipe**.

Important landmarks:
- **Thumb tip → 4**
- **Index finger tip → 8**

Pinch gesture detection:

```python
d = math.hypot(tx - fx, ty - fy)
if d < 20:
    # pinch detected
```

---

### 2️⃣ Puzzle Creation

Captured image is divided into **9 equal sections**:

```
[ a11 | a12 | a13 ]
[ a21 | a22 | a23 ]
[ a31 | a32 | a33 ]
```

Then shuffled using:

```python
np.random.shuffle(puzzle)
```

---

### 3️⃣ Tile Swapping

Tile positions are calculated based on thumb coordinates:

```python
row = getValues(y, hl1, hl2)
col = getValues(x, vl1, vl2)
```

Tiles are swapped inside the puzzle grid.

---

### 4️⃣ Puzzle Completion Check

The puzzle is solved when the shuffled tiles match the original order.

```python
return all(flat[i] is original[i] for i in range(9))
```

---

## 🖼 Example Gameplay Flow

1️⃣ Capture picture  
2️⃣ Puzzle shuffles  
3️⃣ Swap tiles with gestures  
4️⃣ Rebuild the image  
5️⃣ 🎉 Puzzle solved

---

Built using **Computer Vision + Hand Gesture Interaction** to create a fun interactive puzzle experience.

---

⭐ If you like this project, consider giving it a star!