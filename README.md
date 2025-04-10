# PICA

**Progressively Improving Computational Artist**  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?logo=gnu&logoColor=white)](/LICENSE)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat&logo=checkmarx)

Contributors:

[![Daniil Grydin](https://img.shields.io/badge/GitHub-daniilgrydin-57AC4D?logo=github)](https://github.com/daniilgrydin)
[![Zachary Prins](https://img.shields.io/badge/GitHub-okayokayzach-8C3C97?logo=github)](https://github.com/okayokayzach)

---

## 📦 Contents

- [About](#-about)
- [Examples](#%EF%B8%8F-examples)
- [Installation](#%EF%B8%8F-installation)
- [Usage Guide](#-usage-guide)

---

## 🧠 About

**PICA** is a genetic algorithm that transforms images into textmode art using the Commodore 64 character set (PETSCII). Each generated image is composed of 8×8 pixel tiles where the algorithm selects the optimal character, foreground, and background color to match a target image.

The system:
- Uses a population-based evolutionary strategy.
- Supports crossover and mutation operations.
- Visually evolves and previews the image in real time.
- Saves progress frames for creating evolution GIFs.

---

## 🖼️ Examples

| Original | 5,000 Generations | 50,000 Generations | Evolution Gif |
|:--------:|:-----------------:|:------------------:|:-------------:|
| ![](/examples/mario/original.png)[^1] | ![](/examples/mario/population_5226.png) | ![](/examples/mario/population_51588.png) | ![](/examples/mario/evolution.gif) |
| ![](/examples/night/original.png)[^2] | ![](/examples/night/population_5000.png) | ![](/examples/night/population_50000.png) | ![](/examples/night/evolution.gif) |
| ![](/examples/mona/original.png)[^3] | ![](/examples/mona/population_5000.png) | ![](/examples/mona/population_50000.png) | ![](/examples/mona/evolution.gif) |

[^1]: (altered) [Twilio.com](https://www.twilio.com/en-us/blog/making-super-mario-bros-even-more-difficult-for-science-html)
[^2]: (cropped) [Wikipeida](https://en.wikipedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg)
[^3]: (cropped) [Wikipedia](https://en.wikipedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg)

---

## ⚙️ Installation

### 1. Clone Repo

```bash
git clone https://github.com/daniilgrydin/pica.git
cd pica
```

### 2. Install Dependencies

Ensure you're using Python 3.10+, then:

```bash
pip install -r requirements.txt
```

## 🚀 Usage Guide

1. Put your image into the `input` folder
2. Run the main script:
```bash
python main.py
```
3. You’ll be prompted to enter the target image location:
```
input file name/location: input/mona.png
```

> [!NOTE]
> Target images can be any resolution—they’ll be scaled down to 128x128.

4. Two windows will appear:
   - **Population**: showing the top 6 candidates
   - **Best Chromosome**: comparing the current best individual to the target

5. In the terminal it will print you information about fitness of the best individual, number of the generation, FPS, and runtime.
```
Best Fitness: 281616082.0 [1] FPS 3.99 Time: 0.25
Best Fitness: 277604389.0 [2] FPS 6.21 Time: 0.41
...
```

6. Controls:
   - Press `q` quit
   - Press `s` to save the best chromosome image (name includes generation, fitness, and timestamp)

> [!NOTE]
> Every few hundred generations, a snapshot is saved to gif/ for creating a timelapse or evolution animation.

---

Built with 🧋
