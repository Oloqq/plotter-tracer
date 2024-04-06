mod image_prep;
mod params;

use self::image_prep::SourceImage;
pub use self::params::Params;
use std::io::Write;
use structopt::StructOpt;

#[derive(StructOpt)]
struct Args {
    img_path: String,
    // output: String,
    #[structopt(short, long)]
    converted_img: Option<String>,
}

// fn find_workpoints() {}

// fn find_workpath() {}

// fn visualize_workpath() {}

// fn encode() {}

fn main() {
    env_logger::Builder::from_default_env()
        .format(|buf, record| writeln!(buf, "{}: {}", record.level(), record.args()))
        .init();
    // let args = Args::from_args();
    let args = Args {
        img_path: "snek.png".into(),
        // output: "snek.gcode".into(),
        converted_img: Some("snek_gray.png".into()),
    };

    log::info!("Image: {:?}", args.img_path);
    let img = SourceImage::load(args.img_path).unwrap();
    if let Some(path) = args.converted_img {
        img.save(path);
    }
}
