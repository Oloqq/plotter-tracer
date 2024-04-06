use crate::common::*;
use crate::Params;
use image::GrayImage;

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
    source_bounds: Bounds<u32>,
    tool_bounds: Bounds<u32>,
}

impl WorkPoints {
    pub fn points(&self) -> &Vec<Vec<bool>> {
        &self.points
    }

    pub fn tool_bounds(&self) -> &Bounds<u32> {
        &self.tool_bounds
    }

    pub fn source_bounds(&self) -> &Bounds<u32> {
        &self.source_bounds
    }

    pub fn from_image(img: &GrayImage, params: &Params) -> Self {
        const UNWORKED: bool = false;
        const WORKED: bool = true;

        let (width, height) = img.dimensions();
        let mut points: Vec<Vec<bool>> = vec![vec![UNWORKED; height as usize]; width as usize];
        let policy = params.source.work_at;

        let mut leftmost = u32::MAX;
        let mut rightmost = u32::MIN;
        let mut topmost = u32::MAX;
        let mut bottommost = u32::MIN;

        for (x, y, pixel) in img.enumerate_pixels() {
            if policy.is_worked(pixel.0[0]) == WORKED {
                points[x as usize][y as usize] = WORKED;
                if x < leftmost {
                    leftmost = x;
                }
                if x > rightmost {
                    rightmost = x;
                }
                if y < topmost {
                    topmost = y;
                }
                if y > bottommost {
                    bottommost = y;
                }
            }
        }

        Self {
            points,
            source_bounds: Bounds::new(0, width, 0, height),
            tool_bounds: Bounds::new(leftmost, rightmost, topmost, bottommost),
        }
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
