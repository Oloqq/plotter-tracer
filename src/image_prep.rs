use std::error::Error;

use image::GrayImage;

pub fn load_image(img_path: String) -> Result<GrayImage, Box<dyn Error>> {
    println!("{}", img_path);
    let img = image::open(img_path)?;
    // img.resize()

    let grayimg = img.to_luma8();
    // let newimg = image::ImageBuffer::new(100, 100);
    // println!("{:?}", img.color());

    // for (x, y, pixel) in grayimg.enumerate_pixels() {
    //     // println!("{x}, {y}, {pixel:?}");
    // }
    Ok(grayimg)
}
