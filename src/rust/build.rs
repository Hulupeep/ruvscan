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

    // Link against OpenBLAS for linear algebra operations
    // ndarray-linalg with openblas-system feature handles this automatically
    // but we ensure the linker can find it
    println!("cargo:rustc-link-search=native=/usr/lib/x86_64-linux-gnu");
    println!("cargo:rustc-link-lib=dylib=openblas");
    println!("cargo:rustc-link-lib=dylib=gfortran");

    Ok(())
}
