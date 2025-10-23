use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Compile proto files for gRPC
    let out_dir = PathBuf::from(std::env::var("OUT_DIR")?);

    tonic_build::configure()
        .build_server(true)
        .build_client(true)
        .out_dir(&out_dir)
        .compile(
            &["proto/sublinear.proto"],
            &["proto"],
        )?;

    println!("cargo:rerun-if-changed=proto/sublinear.proto");
    Ok(())
}
