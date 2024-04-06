pub mod horizontal;

use crate::common::*;
use crate::WorkPoints;
use image::Pixel;
use image::Rgb;
use image::Rgba;
use imageproc::drawing::draw_filled_rect_mut;
use imageproc::drawing::draw_line_segment_mut;
use imageproc::drawing::Canvas;
use imageproc::rect::Rect;

pub enum Action {
    Up,
    Down,
    Move(V),
}
pub type Actions = Vec<Action>;

pub trait Navigator {
    fn navigate(&self, points: &WorkPoints) -> Actions;
}

type Tile = u32;
pub struct WorkPath {
    actions: Actions,
    source_bounds: Bounds<Tile>,
    tool_bounds: Bounds<Tile>,
}

impl WorkPath {
    pub fn with_navigator(points: WorkPoints, navigator: impl Navigator) -> Self {
        Self {
            actions: navigator.navigate(&points),
            source_bounds: *points.source_bounds(),
            tool_bounds: *points.tool_bounds(),
        }
    }

    pub fn save(&self, img_path: String) {
        const TILE_SIZE: u32 = 8;
        const TILE: f32 = TILE_SIZE as f32;
        let color_bg = Rgba([87, 87, 87, 255]);
        let grid = true;
        let color_grid = Rgba([0, 0, 0, 255]);
        let color_engaged = Rgba([128, 255, 255, 180]);
        let color_disengaged = Rgba([255, 255, 128, 100]);

        let w: Tile = *self.source_bounds.right();
        let h: Tile = *self.source_bounds.bottom();
        let mut img = image::RgbaImage::new(w * TILE_SIZE, h * TILE_SIZE);

        draw_filled_rect_mut(
            &mut img,
            Rect::at(0, 0).of_size(w * TILE_SIZE, h * TILE_SIZE),
            color_bg,
        );

        if grid {
            draw_grid(&mut img, w, h, TILE, color_grid);
        }

        let mut pos = V::new(0.0, 0.0);
        let mut engaged = false;
        for action in &self.actions {
            match action {
                Action::Up => engaged = false,
                Action::Down => engaged = true,
                Action::Move(target) => {
                    let color = if engaged {
                        color_engaged
                    } else {
                        color_disengaged
                    };
                    draw_line_segment_mut(
                        &mut img,
                        (pos.x * TILE, pos.y * TILE),
                        (target.x * TILE, target.y * TILE),
                        color,
                    );
                    pos = *target;
                }
            }
        }

        img.save(img_path).unwrap();
    }
}

fn draw_grid<P>(
    img: &mut impl Canvas<Pixel = P>,
    width_in_tiles: Tile,
    height_in_tiles: Tile,
    tile_size: f32,
    color: P,
) where
    P: Pixel,
{
    for x in 0..width_in_tiles {
        let x = x as f32;
        draw_line_segment_mut(
            img,
            (x * tile_size, 0.0),
            (x * tile_size, height_in_tiles as f32 * tile_size),
            color,
        )
    }
    for y in 0..height_in_tiles {
        let y = y as f32;
        draw_line_segment_mut(
            img,
            (0.0, y * tile_size),
            (width_in_tiles as f32 * tile_size, y * tile_size),
            color,
        )
    }
}
