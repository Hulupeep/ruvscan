// Build script for compiling Protocol Buffers

fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .build_server(true)
        .build_client(false)
        .compile(&["proto/sublinear.proto"], &["proto"])?;

    Ok(())
}
