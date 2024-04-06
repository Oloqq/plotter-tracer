use crate::params::MachineParams;
use crate::workpath::Action;

pub struct MachiningContext {
    pub min_x: f32,
    pub max_x: f32,
    pub min_y: f32,
    pub max_y: f32,
    pub z_engaged: f32,
    pub z_neutral: f32,
    pub speed_engaged: f32,
    pub speed_disengaged: f32,
    pub z_speed: f32,
}

impl MachiningContext {
    pub fn from_params(params: &MachineParams) -> Result<Self, String> {
        let min_x = params.allowed_x_min + params.padding_x;
        let max_x = params.allowed_x_max;
        assert!(min_x < max_x && min_x >= 0.0);
        let min_y = params.allowed_y_min + params.padding_y;
        let max_y = params.allowed_y_max;
        assert!(min_y < max_y && min_y >= 0.0);
        let z_engaged = params.z_engaged;
        let z_neutral = params.z_engaged + params.disengagement_offset;
        assert!(z_engaged < z_neutral && z_engaged >= 0.0);
        assert!(z_neutral - z_engaged >= 1.0);
        let speed_engaged = params.speed_engaged;
        let speed_disengaged = params.speed_disengaged;
        assert!(speed_engaged < speed_disengaged);
        let z_speed = params.vertical_speed;
        assert!(z_speed < speed_disengaged);

        Ok(Self {
            min_x,
            max_x,
            min_y,
            max_y,
            z_engaged,
            z_neutral,
            speed_engaged,
            speed_disengaged,
            z_speed,
        })
    }
}
