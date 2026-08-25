# Setting Up Your Environment

This section walks you through setting up your working environment: choosing a code editor, creating a virtual environment, and organising your project files.

If you already have everything set up, feel free to skip this section.

> **Recommended Python version: 3.13.** The course materials are pinned to Python `>=3.12,<3.14` (see `pyproject.toml`), and everything – notebooks, library versions, compatibility – is tested on 3.13.

## Tools

In this course we work in **Visual Studio Code (VS Code)** with the **Jupyter** extension. This lets you run `.ipynb` notebooks directly inside the editor – no separate browser application needed.

**Jupyter Notebook** is an interactive environment for creating documents that combine code, text, images, and output. Code runs in individual cells, making it easy to work with data step by step.

**Visual Studio Code (VS Code)** is a lightweight yet powerful code editor from Microsoft. With the Jupyter extension installed, it supports notebooks natively.

## What is a Kernel?

Before diving into installation, it helps to understand how Jupyter works.

A **kernel** is a background process that executes the code in your notebook. When you press `Shift + Enter`, the code from the current cell is sent to the kernel, the kernel runs it, and the result is sent back to the notebook.

The kernel is tied to a specific Python virtual environment. This means it is important to select the correct environment when you open a notebook – otherwise the libraries you need may not be available.

If the kernel stops responding, code will not run. You can restart it at any time via `Ctrl+Shift+P → Jupyter: Restart Kernel`.

---

## 1. Installing the Required Tools

### 1.1. Install VS Code

1. Download it from the official website: [https://code.visualstudio.com](https://code.visualstudio.com).
2. Run the installer and follow the on-screen instructions.

### 1.2. Install uv

`uv` is a modern, extremely fast package and virtual environment manager for Python. It can download and install Python versions on its own, create isolated environments, and manage dependencies.

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal and verify it works:

```bash
uv --version
```

### 1.3. Install Python 3.13 via uv

Rather than downloading Python manually from python.org, let `uv` handle it:

```bash
uv python install 3.13
```

Confirm the version is available:

```bash
uv python list
```

### 1.4. Install the Jupyter and Python Extensions in VS Code

1. Open VS Code.
2. Go to the **Extensions** tab (`Ctrl+Shift+X`).
3. Search for **Jupyter** (publisher: Microsoft) and install it.
4. Search for **Python** (publisher: Microsoft) and install it.

---

## 2. Setting Up a Working Directory and Creating a Notebook

We recommend keeping all course projects and exercises in a single dedicated folder.

### 2.1. Create an empty folder anywhere on your computer.

### 2.2. Open it in VS Code

Go to **File → Open Folder**, or drag the folder into the VS Code window.

### 2.3. Create a Jupyter Notebook

In the **Explorer** panel, click the **New File** icon and enter a filename with the `.ipynb` extension.

### 2.4. Open the file you just created.

---

## 3. Setting Up a Virtual Environment with uv

`uv` creates environments quickly and with the correct Python version from the start.

### 3.1. Initialise the project

Open the terminal in VS Code (**Terminal → New Terminal**) and run:

```bash
uv init
```

This creates `pyproject.toml` and `.python-version`, which describe the project and pin the Python version. The virtual environment itself (a `.venv` folder) appears the first time you run `uv add`, `uv sync`, or `uv run`.

### 3.2. Check the Python version in the environment

```bash
uv run python --version
```

If the version is not 3.13, pin it explicitly:

```bash
uv python pin 3.13
```

Then recreate the environment:

```bash
uv sync
```

### 3.3. Activate the environment manually (if needed)

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

> Once activated, VS Code should pick up the environment automatically when you open a notebook. If it does not, select it manually via **Select Kernel** in the top-right corner of the editor.

---

## 4. Installing Libraries

There are two situations here, and they need different commands.

### 4.1. You cloned the course repository

This is the short route, and it is worth taking if you already use git. Cloning brings the whole course down at once – the notebooks, the `data/` folder, and the pinned dependency files – so it replaces both the project folder of section 2 and the data download of section 5:

```bash
git clone https://github.com/bella-mir/geoPythonEn.git
cd geoPythonEn
```

The repository already contains `pyproject.toml` and `uv.lock` with the exact versions everything was tested with. One command installs all of them:

```bash
uv sync
```

Open that folder in VS Code and the notebooks run where they sit: their `../../data/...` paths are already correct, because the layout around them is the one they were written for.

### 4.2. You are working in your own project folder

Add the libraries the course uses:

```bash
uv add geopandas shapely osmnx folium mapclassify rasterio rasterstats networkx pandas numpy matplotlib requests polyline
```

`uv` installs the packages, writes them into `pyproject.toml`, and creates a `uv.lock` file pinning the exact versions of every dependency, including transitive ones.

To run notebooks you also need a Jupyter kernel. VS Code offers to install `ipykernel` the first time you run a cell; you can also add it yourself:

```bash
uv add ipykernel
```

### 4.3. Alternative – using pip

> Use this approach only if `uv` is unavailable for some reason.

First, make sure Python is installed (3.12 or 3.13 – download from [python.org](https://www.python.org/downloads) and **check the box** `Add Python to PATH` during installation). Then create a virtual environment:

```bash
python -m venv myenv

source myenv/bin/activate   # Linux / macOS
myenv\Scripts\activate       # Windows
```

Once the environment is active, install the dependencies:

```bash
pip install geopandas shapely osmnx folium mapclassify rasterio rasterstats networkx pandas numpy matplotlib requests polyline ipykernel
```

If you cloned the repository, you can instead install the pinned versions from the exported file:

```bash
pip install -r requirements.txt
```

---

## 5. Getting the Course Data

The notebooks work on prepared datasets – Vienna's districts and buildings, U-Bahn stations, a population raster – kept in a `data/` folder. Every file and where it came from is listed in [Course Modules](syllabus.md).

**[Download data.zip](https://github.com/bella-mir/geoPythonEn/releases/latest/download/data.zip)** (about 28 MB), unpack it, and put the `data` folder into your project, next to your notebook. That link always serves the data of the most recent release, so it does not go stale.

Or do the same from a notebook cell:

```python
import urllib.request, shutil, os

url = "https://github.com/bella-mir/geoPythonEn/releases/latest/download/data.zip"
urllib.request.urlretrieve(url, "data.zip")
shutil.unpack_archive("data.zip")

os.remove("data.zip")
```

Your project folder should now look like this:

```
my-course-folder/
├── data/
│   ├── austria/
│   ├── leopoldstadt/
│   └── vienna/
├── notebook.ipynb
└── pyproject.toml
```

**Where the folder sits matters.** The notebooks published in this book live two levels deep, in `notebooks/module_1/` and so on, so they reach the data as `../../data/vienna/vienna_metro.geojson`. In your own project, with `data/` sitting next to your notebook, drop the `../../`:

```python
gdf = gpd.read_file("data/vienna/vienna_metro.geojson")
```

When a read fails with `FileNotFoundError`, this is nearly always the reason: the path was written for a different folder layout. The file is there; the notebook is looking somewhere else.

---

## 6. Basic Features

### 6.1. Running Cells

- **Run a cell**: `Shift + Enter`.
- **Add a code cell**: click `+ Code` in the toolbar, or press `Esc` to leave the cell and then `B` (below) / `A` (above).
- **Turn a cell into text** (Markdown): press `Esc`, then `M`; `Y` turns it back into a code cell.

---

## 7. Additional Tips

- Useful shortcuts:
  - `Ctrl + /` – comment or uncomment code.
  - `Alt + Up/Down` – move a cell up or down (press `Esc` first; inside a cell the same shortcut moves the current line).
- If the kernel stops responding:
  - Restart it via `Ctrl+Shift+P → Jupyter: Restart Kernel`.
- Documentation:
  - [Jupyter in VS Code](https://code.visualstudio.com/docs/python/jupyter-support)
  - [uv documentation](https://docs.astral.sh/uv/)

**You're all set!** You can now work with Jupyter Notebooks in VS Code.
