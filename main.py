import os
from dotenv import load_dotenv

from hsr_size_analyzer.hsr_size_analyzer import get_file_distribution
from hsr_size_analyzer.sqlite import save_to_db

# Load environment variables from .env file
load_dotenv()


game_directory = os.getenv("GAME_DIR")
df = get_file_distribution(game_directory)
save_to_db(df)