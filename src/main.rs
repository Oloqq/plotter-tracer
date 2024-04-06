mod common;
mod image_prep;
mod params;
mod workpath;
mod workpoints;

use crate::{workpath::WorkPath, workpoints::WorkPoints};

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
    #[structopt(short, long)]
    workpoints_img: Option<String>,
    #[structopt(short, long)]
    workpath_img: Option<String>,
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
        workpoints_img: Some("snek_workpoints.png".into()),
        workpath_img: Some("snek_workpath.png".into()),
    };

    let params = Params::default();

    log::info!("Image: {:?}", args.img_path);
    let img = SourceImage::load(args.img_path).unwrap();
    if let Some(path) = args.converted_img {
        img.save(path);
    }

    let wpo = WorkPoints::from_image(&img.into(), &params);
    if let Some(path) = args.workpoints_img {
        wpo.save(path);
    }

    let navi = workpath::horizontal::Horizontal {};
    let wpa = WorkPath::with_navigator(wpo, navi);
    if let Some(path) = args.workpath_img {
        wpa.save(path);
    }
}
