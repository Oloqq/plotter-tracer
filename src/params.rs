#[derive(Debug, Default, Clone, Copy)]
pub struct Params {
    source: SourceParams,
    machine: MachineParams,
    material: MaterialParams,
}

#[derive(Debug, Clone, Copy)]
pub struct SourceParams {
    pixel_to_um: u32,
    brush_um: u32,
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
        }
    }
}

impl SourceParams {
    fn workpoints_per_pixel(&self) -> u32 {
        assert!(
            self.pixel_to_um / self.brush_um == 1,
            "ppp < 1 needs interpolation"
        );
        1
    }
}
