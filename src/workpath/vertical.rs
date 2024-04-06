use super::Action::{self, *};
use super::{Actions, Navigator};
use crate::common::*;
use crate::WorkPoints;

pub struct Vertical {}

impl Navigator for Vertical {
    fn navigate(&self, points: &WorkPoints) -> Actions {
        let _tool_bounds = points.tool_bounds();
        let points = points.points();

        let mut engaged = false;
        let mut actions = vec![];
        for (x, col) in points.iter().enumerate() {
            actions.push(Note(format!("Column {x}")));
            let iter = col.iter().enumerate();
            if x % 2 == 0 {
                for (y, pixel) in iter {
                    actions.append(&mut action_match(*pixel, engaged, x, y));
                    engaged = *pixel;
                }
            } else {
                for (y, pixel) in iter.rev() {
                    actions.append(&mut action_match(*pixel, engaged, x, y));
                    engaged = *pixel;
                }
            };
        }

        actions
    }
}

fn action_match(pixel: bool, engaged: bool, x: usize, y: usize) -> Vec<Action> {
    match (pixel, engaged) {
        (true, true) => vec![Move(pos(x, y))],
        (true, false) => vec![Move(pos(x, y)), Engage],
        (false, true) => vec![Retreat, Move(pos(x, y))],
        (false, false) => vec![],
    }
}

fn pos(x: usize, y: usize) -> V {
    V::new(x as f32, y as f32)
}
