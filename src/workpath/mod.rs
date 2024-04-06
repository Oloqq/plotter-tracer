pub mod horizontal;

use crate::common::*;
use crate::WorkPoints;
use imageproc::drawing::draw_line_segment_mut;

pub enum Action {
    Up,
    Down,
    Move(usize, usize),
}
pub type Actions = Vec<Action>;

pub trait Navigator {
    fn navigate(&self, points: &WorkPoints) -> Actions;
}

pub struct WorkPath {
    actions: Actions,
    source_bounds: Bounds<u32>,
    tool_bounds: Bounds<u32>,
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
        let grid = true;

        let mut img = image::RgbImage::new(
            *self.source_bounds.right() * TILE_SIZE,
            *self.source_bounds.bottom() * TILE_SIZE,
        );

        img.save(img_path).unwrap();
    }
}
