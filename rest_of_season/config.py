from pathlib import Path

# --------------------------------------------------
# Season configuration
# --------------------------------------------------

SEASON = 2026
CURRENT_WEEK = 8

N_SIMULATIONS = 50_000
RANDOM_SEED = 2026

# --------------------------------------------------
# Project paths
# --------------------------------------------------

ROS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROS_ROOT.parent

NOTEBOOK_DIR = ROS_ROOT / "notebooks"

OUTPUT_ROOT = ROS_ROOT / "outputs"

CURRENT_OUTPUT_DIR = (
    OUTPUT_ROOT / f"week_{CURRENT_WEEK:02d}"
)

PREVIOUS_OUTPUT_DIR = (
    OUTPUT_ROOT / f"week_{CURRENT_WEEK - 1:02d}"
)

# --------------------------------------------------
# Create current output directory
# --------------------------------------------------

CURRENT_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Season: {SEASON}")
print(f"Projection week: {CURRENT_WEEK}")
print(f"Simulations: {N_SIMULATIONS:,}")
print(f"Output directory: {CURRENT_OUTPUT_DIR}")