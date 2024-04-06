use image::GrayImage;

use crate::Params;

#[derive(Debug, Clone, Copy)]
pub enum Policy {
    DarkerThan(u8),
    #[allow(unused)]
    BrighterThan(u8),
}

impl Policy {
    pub fn is_worked(&self, val: u8) -> bool {
        use Policy::*;
        match self {
            DarkerThan(x) => val < *x,
            BrighterThan(x) => val > *x,
        }
    }
}

pub struct WorkPoints {
    points: Vec<Vec<bool>>,
}

impl WorkPoints {
    pub fn from_image(img: &GrayImage, params: &Params) -> Self {
        let (width, height) = img.dimensions();
        let mut points: Vec<Vec<bool>> = vec![vec![false; height as usize]; width as usize];
        let policy = params.source.work_at;

        for (x, y, pixel) in img.enumerate_pixels() {
            points[x as usize][y as usize] = policy.is_worked(pixel.0[0])
        }

        Self { points }
    }

    pub fn save(&self, img_path: String) {
        let mut img: GrayImage =
            image::ImageBuffer::new(self.points.len() as u32, self.points[0].len() as u32);
        for (x, y, pixel) in img.enumerate_pixels_mut() {
            let pixval = if self.points[x as usize][y as usize] {
                0
            } else {
                255
            };
            *pixel = image::Luma([pixval]);
        }
        img.save(img_path).unwrap();
    }
}
