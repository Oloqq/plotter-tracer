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

#[derive(Debug, Default, Clone, Copy)]
pub struct MachineParams {}

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
