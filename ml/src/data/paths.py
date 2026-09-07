from pathlib import Path
from pydantic_settings import BaseSettings

class DataPaths(BaseSettings):
    """Configuration class resolving all data paths dynamically."""
    
    # Base directories
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"
    
    # Lifecycle directories
    raw_dir: Path = data_dir / "raw"
    interim_dir: Path = data_dir / "interim"
    processed_dir: Path = data_dir / "processed"
    features_dir: Path = data_dir / "features"
    selected_dir: Path = data_dir / "selected"
    splits_dir: Path = data_dir / "splits"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure all directories exist
        for path_field in [self.raw_dir, self.interim_dir, self.processed_dir, 
                           self.features_dir, self.selected_dir, self.splits_dir]:
            path_field.mkdir(parents=True, exist_ok=True)

# Usage: paths = DataPaths()
# print(paths.raw_dir / "cicids-2017")
