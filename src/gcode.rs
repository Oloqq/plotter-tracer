use crate::{machining_context::MachiningContext as Ctx, workpath::WorkPath, Params};

struct Engaged {}

struct Neutral {}

pub fn gcode(actions: &WorkPath, params: &Params) -> String {
    let _actions = actions.actions().iter();
    let ctx = Ctx::from_params(&params.machine).unwrap();
    header(&ctx)
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
