/*!
RuvScan Sublinear Engine
TRUE O(log n) semantic comparison and clustering
*/

use tonic::transport::Server;
use tracing::{info};
use tracing_subscriber;
use std::net::SocketAddr;

mod sublinear;
mod grpc_service;

use grpc_service::sublinear_proto::sublinear_service_server::SublinearServiceServer;
use grpc_service::SublinearServiceImpl;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // VERY FIRST THING - Debug output to stderr (bypasses all logging)
    eprintln!("=== RUST ENGINE STARTING ===");
    eprintln!("DEBUG: Entered main function");

    // Initialize tracing
    eprintln!("DEBUG: Initializing tracing...");
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .init();
    eprintln!("DEBUG: Tracing initialized");

    info!("🦀 RuvScan Sublinear Engine v0.5.0");
    info!("TRUE O(log n) Semantic Computation");

    eprintln!("DEBUG: Creating tokio runtime...");
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .expect("Failed to create Tokio runtime");
    eprintln!("DEBUG: Tokio runtime created successfully");

    runtime.block_on(async {
        eprintln!("DEBUG: Inside async block");
        eprintln!("DEBUG: Parsing address...");
        let addr = "0.0.0.0:50051".parse()
            .expect("Failed to parse server address");
        eprintln!("DEBUG: Address parsed: {}", addr);

        eprintln!("DEBUG: Creating service...");
        let service = SublinearServiceImpl::default();
        eprintln!("DEBUG: Service created");

        info!("🚀 Starting gRPC server on {}", addr);
        eprintln!("DEBUG: Building gRPC server...");

        Server::builder()
            .add_service(SublinearServiceServer::new(service))
            .serve(addr)
            .await
            .map_err(|e| {
                eprintln!("❌ Server error: {}", e);
                e
            })
    })?;

    info!("✅ Server started successfully");
    eprintln!("DEBUG: Server stopped");
    Ok(())
}
