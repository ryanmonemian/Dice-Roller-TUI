# Dice Roller TUI (Python + curses)

A terminal-based dice roller built with **Python**.  
It uses `curses` for a text-based interface and `numpy` for random rolls. You roll five dice, hold or release them, and reset or quit directly from your terminal.

---

## Preview

![Dice Roller Preview](./preview.png)

---

## Setup Instructions

### 1. Create and activate an environment
```bash
conda create -n PPP python=3.11 -y
conda activate PPP
```

### 2. Install dependencies
```bash
conda install numpy -y
pip install windows-curses  # only needed on Windows
```

### 3. Navigate to your project folder
```bash
cd path/to/dice_roller
```

### 4. Run the program
```bash
python main.py
```

---

## Controls

| Action | Key / Mouse |
|:--------|:-------------|
| Roll all dice | `r` or click **Roll** |
| Reset | `t` or click **Reset** |
| Hold / Unhold a die | Press `1`–`5` or click a die |
| Quit | Press `q`, `Q`, or `ESC` |

---

## Requirements

- Python 3.8 or higher  
- numpy  
- windows-curses (Windows only)  
- Terminal that supports UTF-8 and mouse input

---

## Example Output

```
┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
│ - │   │ - │   │ - │   │ - │   │ - │
└───┘   └───┘   └───┘   └───┘   └───┘
  ◯      ◯      ◯      ◯      ◯

┌──────┐     ┌───────┐     ┌──────┐
│ Roll │     │ Reset │     │ Quit │
└──────┘     └───────┘     └──────┘

Rolls Remaining: 3
```

---

## How it Works

- The program builds a **TUI** using Python `curses`.  
- Each die is an instance of the **Die** class.  
- Dice rolling, holding, and redrawing are handled dynamically.  
- The app refreshes the display after every roll or click.  

---

## File Structure

| File | Description |
|:------|:-------------|
| `main.py` | Main program file |
| `Die` | Class for individual dice |
| `Dice` | Class for managing dice and rolls |
| `Button` | Class for on-screen buttons |

---

## Troubleshooting

| Issue | Fix |
|:-------|:----|
| `_curses` not found | Install `windows-curses` |
| Broken layout | Use UTF-8 terminal or resize to 80×25 |
| Mouse input not working | Use Anaconda PowerShell or Windows Terminal |

---

## License

MIT License

---
