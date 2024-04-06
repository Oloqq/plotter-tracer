use std::error::Error;

use image::GrayImage;

pub struct SourceImage {
    img: GrayImage,
}

impl SourceImage {
    pub fn load(img_path: String) -> Result<Self, Box<dyn Error>> {
        let img = image::open(img_path)?;
        let grayimg = img.to_luma8();
        Ok(Self { img: grayimg })
    }

    pub fn save(&self, img_path: String) {
        self.img.save(img_path).unwrap();
    }
}

impl Into<GrayImage> for SourceImage {
    fn into(self) -> GrayImage {
        self.img
    }
}
