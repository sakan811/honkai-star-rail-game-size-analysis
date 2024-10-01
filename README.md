# Honkai Star Rail: Game Size Analysis
Display visualizations that illustrate the distribution of game sizes for Honkai Star Rail.

## Status
[![Python Script Test](https://github.com/sakan811/honkai-star-rail-game-size-analysis/actions/workflows/test-python.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-game-size-analysis/actions/workflows/test-python.yml)

[![CodeQL](https://github.com/sakan811/honkai-star-rail-game-size-analysis/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/honkai-star-rail-game-size-analysis/actions/workflows/codeql.yml)

## Visualizations
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMGEwMWU0MDMtMTQzOC00NzAyLTgyYWYtZjliNjIxN2RhZDQ4IiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)

[Instagram](https://www.instagram.com/p/DAlx2IxvK13/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

[Facebook](https://www.facebook.com/share/p/gxt2xzPMXwQztuCZ/)

## How to Use the Script
### Setup the Project
- Clone this repository: https://github.com/sakan811/honkai-star-rail-game-size-analysis.git
- Rename `.env.example` to `.env`
- Copy the absolute path of the Honkai Star Rail game directory
- Paste the path into the `GAME_DIR` variable in the `.env` file.

### Run the Script
* Run the Python script:
    ```bash
    python main.py
    ```
* The game size data is stored in an SQLite database
  > The database will be created automatically if it doesn’t already exist.