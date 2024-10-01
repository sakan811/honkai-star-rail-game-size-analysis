# Honkai Star Rail: Game Size Analysis
Display visualizations that illustrate the distribution of game sizes for Honkai Star Rail.

## Status


## Visualizations
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMGEwMWU0MDMtMTQzOC00NzAyLTgyYWYtZjliNjIxN2RhZDQ4IiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)

[Instagram]()

[Facebook]()

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