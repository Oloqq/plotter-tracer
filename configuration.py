# class PlotterConfiguration:

class PlotterConfiguration():
    input_path: str = None
    tile_size: float = 0.25,
    z_high: float = 19,
    z_low: float = 13,
    x = [50, 220],
    y = [30, 220],
    horizontal_move_force: int = 500,
    vertical_move_force: int = 200

    def validate(self) -> bool:
        raise NotImplementedError