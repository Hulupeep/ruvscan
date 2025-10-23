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

    // For openblas-static, we need to explicitly link the static library
    // The openblas-src crate builds it but we need to tell the linker where it is
    if let Ok(openblas_path) = std::env::var("DEP_OPENBLAS_SRC") {
        println!("cargo:rustc-link-search=native={}", openblas_path);
        println!("cargo:rustc-link-lib=static=openblas");
        println!("cargo:rustc-link-lib=dylib=gfortran");
    } else {
        // Fallback to system OpenBLAS if available
        println!("cargo:rustc-link-search=native=/usr/lib/x86_64-linux-gnu");
        println!("cargo:rustc-link-lib=static=openblas");
        println!("cargo:rustc-link-lib=dylib=gfortran");
    }

    Ok(())
}
