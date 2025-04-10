# PICA

**Progressively Improving Computational Artist**  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?logo=gnu&logoColor=white)](/LICENSE)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat&logo=checkmarx)

Contributors:

[![Daniil Grydin](https://img.shields.io/badge/GitHub-daniilgrydin-57AC4D?logo=github)](https://github.com/daniilgrydin)
[![Zachary Prins](https://img.shields.io/badge/GitHub-okayokayzach-8C3C97?logo=github)](https://github.com/okayokayzach)

---

## Contents

- [About](#about)
- [Examples](#examples)
- [Installation](#installation)
- [Usage Guide](#usage-guide)

---

## About

**PICA (Progressively Improving Computational Artist)** is a Python-based visual art generator that creates textmode art using a genetic algorithm. Inspired by the aesthetics of PETSCII (Commodore 64's character set), PICA takes any input image, divides it into 8x8 pixel blocks, and evolves a population of representations to approximate the target using character tiles and colors.

This project was created as a final project for a university-level course in Applied Artificial Intelligence. The goal was to explore the use of genetic algorithms in discrete visual tasks and create a system capable of mimicking complex imagery through simple symbols and color palettes.

---

## Examples

| Original | 5,000 Generations | 50,000 Generations | Evolution Gif |
|:--------:|:-----------------:|:------------------:|:-------------:|
| ![](/examples/mario/original.png)[^1] | ![](/examples/mario/population_5226.png) | ![](/examples/mario/population_51588.png) | ![](/examples/mario/evolution.gif) |
| ![](/examples/night/original.png)[^2] | ![](/examples/night/population_5000.png) | ![](/examples/night/population_50000.png) | ![](/examples/night/evolution.gif) |
| ![](/examples/mona/original.png)[^3] | ![](/examples/mona/population_5000.png) | ![](/examples/mona/population_50000.png) | ![](/examples/mona/evolution.gif) |

[^1]: (altered) [Twilio.com](https://www.twilio.com/en-us/blog/making-super-mario-bros-even-more-difficult-for-science-html)
[^2]: (cropped) [Wikipeida](https://en.wikipedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg)
[^3]: (cropped) [Wikipedia](https://en.wikipedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg)

---

## Installation

### Verify Python Installation

Ensure Python 3.8+ is installed. You can verify with:

```bash
python --version
```

### Clone Repo

```bash
git clone https://github.com/daniilgrydin/pica.git
cd pica
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage Guide

1. Put your image into the `resources` folder
2. Run the main script:
```bash
python main.py
```
3. You’ll be prompted to enter the target image location:
```
input file name/location: resources/mona.png
```

> [!NOTE]
> Target images can be any resolution—they’ll be scaled down to 128x128.

4. Two windows will open:
   - The top six individuals from the population.
   - A comparison of the best individual to the target image.

5. In the terminal it will print you information about fitness of the best individual, number of the generation, FPS, and runtime.
```
Best Fitness: 281616082.0 [1] FPS 3.99 Time: 0.25
Best Fitness: 277604389.0 [2] FPS 6.21 Time: 0.41
...
```

6. Controls:
   - Press 'q' quit
   - Press s to save the current best image. (Note: May require multiple attempts.)

7. Upon quitting, final stats will be printed:
```
Best Fitness: 28078022.0 [19323] FPS 5.704176775864132 Time: 3627.7086412906647
Total time: 3627.7101442813873
Total generations: 19323
Average FPS: 5.326499286257991
Best fitness: 28078022.0
```
