fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Compile proto files for gRPC
    tonic_build::configure()
        .build_server(true)
        .build_client(true)
        .out_dir("src/generated")
        .compile(
            &["proto/sublinear.proto"],
            &["proto"],
        )?;
    Ok(())
}
