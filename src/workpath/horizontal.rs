use super::{Actions, Navigator};
use crate::WorkPoints;

pub struct Horizontal {}

impl Navigator for Horizontal {
    fn navigate(&self, points: &WorkPoints) -> Actions {
        let _tool_bounds = points.tool_bounds();
        let _points = points.points();

        use super::Action::*;
        vec![Move(0, 0), Move(2, 0), Up, Move(4, 0), Down, Move(5, 0)]
    }
}
