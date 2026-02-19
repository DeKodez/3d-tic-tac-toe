"""UI constants — colors, dimensions, layout positions, and labels."""

# --- Colors (R, G, B) ---
BG_COLOR = (30, 30, 30)
GRID_COLOR = (200, 200, 200)
X_COLOR = (70, 130, 230)
O_COLOR = (230, 70, 70)
CELL_HOVER = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)

ARROW_BG = (60, 60, 60)
ARROW_HOVER = (80, 80, 80)
ARROW_ICON = (180, 180, 180)

LOCKED_OVERLAY = (0, 0, 0, 100)
LOCKED_LABEL_COLOR = (180, 180, 180)

STATUS_BG = (40, 40, 40)

CUBE_EDGE_COLOR = (150, 150, 150)
CUBE_EDGE_BACK_COLOR = (80, 80, 80)

# --- Window ---
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 620

# --- Grid ---
CELL_SIZE = 120
GRID_LINE_WIDTH = 3
GRID_WIDTH = CELL_SIZE * 3
GRID_HEIGHT = CELL_SIZE * 3
GRID_ORIGIN_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_ORIGIN_Y = 100

# --- Marks ---
MARK_PADDING = 25
MARK_LINE_WIDTH = 4

# --- Arrow Buttons ---
ARROW_SIZE = 36
ARROW_PADDING = 8

ARROW_UP = (
    GRID_ORIGIN_X + GRID_WIDTH // 2 - ARROW_SIZE // 2,
    GRID_ORIGIN_Y - ARROW_SIZE - 10,
)
ARROW_DOWN = (
    GRID_ORIGIN_X + GRID_WIDTH // 2 - ARROW_SIZE // 2,
    GRID_ORIGIN_Y + GRID_HEIGHT + 10,
)
ARROW_LEFT = (
    GRID_ORIGIN_X - ARROW_SIZE - 10,
    GRID_ORIGIN_Y + GRID_HEIGHT // 2 - ARROW_SIZE // 2,
)
ARROW_RIGHT = (
    GRID_ORIGIN_X + GRID_WIDTH + 10,
    GRID_ORIGIN_Y + GRID_HEIGHT // 2 - ARROW_SIZE // 2,
)

ARROWS = {
    "up": ARROW_UP,
    "down": ARROW_DOWN,
    "left": ARROW_LEFT,
    "right": ARROW_RIGHT,
}

# --- Mini Cube Legend ---
CUBE_LEGEND_CX = 65
CUBE_LEGEND_CY = 42
CUBE_LEGEND_R = 22

# --- Face label ---
FACE_LABEL_Y = 20

# --- Status bar ---
STATUS_BAR_Y = GRID_ORIGIN_Y + GRID_HEIGHT + ARROW_SIZE + 24
STATUS_BAR_HEIGHT = 40

# --- Face definitions ---
FACE_LABELS = ["Top", "Front", "Left", "Bottom", "Back", "Right"]
NUM_FACES = 6
DEFAULT_FACE = 1  # Start on Front

# Navigation adjacency: face_index -> {direction: next_face_index}
# Horizontal ring: Front -> Right -> Back -> Left -> Front
# Vertical ring:   Front -> Top -> Back -> Bottom -> Front
FACE_ADJACENCY = {
    0: {"left": 2, "right": 5, "up": 4, "down": 1},   # Top
    1: {"left": 2, "right": 5, "up": 0, "down": 3},   # Front
    2: {"left": 4, "right": 1, "up": 0, "down": 3},   # Left
    3: {"left": 2, "right": 5, "up": 1, "down": 4},   # Bottom
    4: {"left": 5, "right": 2, "up": 3, "down": 0},   # Back
    5: {"left": 1, "right": 4, "up": 0, "down": 3},   # Right
}

# --- Fonts ---
FONT_SIZE_STATUS = 22
FONT_SIZE_FACE_LABEL = 28
FONT_SIZE_CUBE_LABEL = 14
FONT_SIZE_LOCKED_LABEL = 32
FONT_SIZE_GAME_OVER = 36
FONT_SIZE_GAME_OVER_SUB = 20
