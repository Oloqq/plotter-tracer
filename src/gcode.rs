use crate::machining_context::MachiningContext as Ctx;
use crate::workpath::Action;
use crate::workpath::WorkPath;
use crate::Params;

struct Engaged {}

struct Neutral {}

impl Engaged {
    fn ping<I>(self, actions: I) -> I
    where
        I: Iterator<Item = Action>,
    {
        actions
    }
}

impl Neutral {
    fn advance(self, mut actions: impl Iterator<Item = Action>) {
        while let Some(action) = actions.next() {
            match action {
                Action::Retreat => actions = Engaged {}.ping(actions),
                Action::Engage => todo!(),
                Action::Move(_) => todo!(),
                Action::Note(_) => todo!(),
            }
        }
    }
}

struct Tool {}

pub fn gcode(actions: &WorkPath, params: &Params) -> String {
    // let ctx = Ctx::from_params(&params.machine).unwrap();
    // header(&ctx)

    let mut actions = actions.actions().iter().cloned().peekable();
    let first = actions.peek().unwrap();
    match first {
        Action::Retreat => panic!(),
        Action::Engage => panic!(),
        _ => (),
    };
    Neutral {}.advance(actions);

    todo!()
}

fn header(ctx: &Ctx) -> String {
    let now = chrono::offset::Local::now();
    let vertical_force = 0.0;
    let high = ctx.z_neutral;
    format!(
        "; Rustracer {now}
M140 S0 ; Bed temperature
M104 S0 ; Hotend temperature
M105 ; Report temperatures
M107 ; No fan
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90 ; Set all axes to absolute
G0 F{vertical_force} Z{high} ; Lift the pen
"
    )
}
