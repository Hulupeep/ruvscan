/*!
RuvScan Sublinear Engine
TRUE O(log n) semantic comparison and clustering
*/

use tonic::transport::Server;
use tracing::{info, error};
use tracing_subscriber;

mod sublinear;
mod grpc_service;

use grpc_service::sublinear_proto::sublinear_service_server::SublinearServiceServer;
use grpc_service::SublinearServiceImpl;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .init();

    info!("🦀 RuvScan Sublinear Engine v0.5.0");
    info!("TRUE O(log n) Semantic Computation");

    let addr = "[::1]:50051".parse()?;
    let service = SublinearServiceImpl::default();

    info!("🚀 Starting gRPC server on {}", addr);

    Server::builder()
        .add_service(SublinearServiceServer::new(service))
        .serve(addr)
        .await?;

    info!("Server started successfully");

    Ok(())
}
