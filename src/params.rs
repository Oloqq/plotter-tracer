use crate::workpoints::Policy;

#[derive(Debug, Default, Clone, Copy)]
pub struct Params {
    pub source: SourceParams,
    pub machine: MachineParams,
    pub material: MaterialParams,
}

#[derive(Debug, Clone, Copy)]
pub struct SourceParams {
    pub pixel_to_um: u32,
    pub brush_um: u32,
    pub work_at: Policy,
}

#[derive(Debug, Clone, Copy)]
pub struct MachineParams {
    /// Highest Z at which the tool is engaged (first working layer).
    pub z_engaged: f32,
    /// Z-raise at disengagement.
    pub disengagement_offset: f32,

    /// Note that the tool will travel from home to destination in Y along X=0 regardless of this setting.
    pub allowed_x_min: f32,
    pub allowed_x_max: f32,
    /// Note that the tool will travel from home to destination in Y along X=0 regardless of this setting.
    pub allowed_y_min: f32,
    pub allowed_y_max: f32,

    /// Makes the work start at offset from allowed area.
    pub padding_x: f32,
    /// Makes the work start at offset from allowed area.
    pub padding_y: f32,

    /// The faster you move the easier a fire starts.
    pub speed_engaged: f32,
    pub speed_disengaged: f32,
    pub vertical_speed: f32,
}

#[derive(Debug, Default, Clone, Copy)]
pub struct MaterialParams {}

impl Default for SourceParams {
    fn default() -> Self {
        Self {
            pixel_to_um: 2400,
            brush_um: 2400,
            work_at: Policy::DarkerThan(10),
        }
    }
}

impl Default for MachineParams {
    fn default() -> Self {
        Self {
            z_engaged: 20.0,
            disengagement_offset: 3.0,
            allowed_x_min: 50.0,
            allowed_x_max: 100.0,
            allowed_y_min: 50.0,
            allowed_y_max: 100.0,
            speed_engaged: 70.0,
            speed_disengaged: 500.0,
            vertical_speed: 200.0,
            padding_x: 0.0,
            padding_y: 0.0,
        }
    }
}

impl SourceParams {
    #[allow(unused)]
    fn workpoints_per_pixel(&self) -> u32 {
        assert!(
            self.pixel_to_um / self.brush_um == 1,
            "ppp < 1 needs interpolation"
        );
        1
    }
}
