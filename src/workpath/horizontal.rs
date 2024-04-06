use super::{Actions, Navigator};
use crate::common::*;
use crate::WorkPoints;

pub struct Horizontal {}

impl Navigator for Horizontal {
    fn navigate(&self, points: &WorkPoints) -> Actions {
        let _tool_bounds = points.tool_bounds();
        let _points = points.points();

        use super::Action::*;
        vec![
            Move(V::new(0.0, 0.0)),
            Move(V::new(2.0, 4.0)),
            Up,
            Move(V::new(4.0, 0.0)),
            Down,
            Move(V::new(5.0, 6.0)),
        ]
    }
}
