use std::io::Write;
use std::path::PathBuf;
use structopt::StructOpt;

#[derive(StructOpt)]
struct Args {
    img: PathBuf,
}

fn main() {
    env_logger::Builder::from_default_env()
        .format(|buf, record| writeln!(buf, "{}: {}", record.level(), record.args()))
        .init();
    let args = Args::from_args();
    println!("Image: {:?}", args.img);
}
