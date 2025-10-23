/*!
RuvScan Sublinear Engine
TRUE O(log n) semantic comparison and clustering
*/

use tonic::transport::Server;
use tracing::{info};
use tracing_subscriber;
use std::net::SocketAddr;
use std::io::Write;

mod sublinear;
mod grpc_service;

use grpc_service::sublinear_proto::sublinear_service_server::SublinearServiceServer;
use grpc_service::SublinearServiceImpl;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Test 1: Can we even execute?
    std::io::stderr().write_all(b"=== RUST ENGINE STARTING ===\n").ok();
    std::io::stderr().flush().ok();

    // Test 2: Can we use println?
    println!("stdout: Rust engine initializing");
    std::io::stdout().flush().ok();

    // Test 3: eprintln with explicit flush
    eprintln!("stderr: DEBUG - Entered main function");
    std::io::stderr().flush().ok();

    // Initialize tracing with explicit error handling
    eprintln!("stderr: DEBUG - Initializing tracing...");
    std::io::stderr().flush().ok();

    match tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .try_init() {
        Ok(_) => {
            eprintln!("stderr: DEBUG - Tracing initialized successfully");
            std::io::stderr().flush().ok();
        },
        Err(e) => {
            eprintln!("stderr: WARNING - Tracing init failed: {}", e);
            std::io::stderr().flush().ok();
        }
    }

    info!("🦀 RuvScan Sublinear Engine v0.5.0");
    info!("TRUE O(log n) Semantic Computation");

    eprintln!("stderr: DEBUG - Creating tokio runtime...");
    std::io::stderr().flush().ok();

    let runtime = match tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build() {
        Ok(rt) => {
            eprintln!("stderr: DEBUG - Tokio runtime created successfully");
            std::io::stderr().flush().ok();
            rt
        },
        Err(e) => {
            eprintln!("stderr: FATAL - Failed to create Tokio runtime: {}", e);
            std::io::stderr().flush().ok();
            return Err(Box::new(e));
        }
    };

    eprintln!("stderr: DEBUG - Blocking on async server...");
    std::io::stderr().flush().ok();

    let result = runtime.block_on(async {
        eprintln!("stderr: DEBUG - Inside async block");
        std::io::stderr().flush().ok();

        let addr = match "0.0.0.0:50051".parse() {
            Ok(a) => {
                eprintln!("stderr: DEBUG - Address parsed: {}", a);
                std::io::stderr().flush().ok();
                a
            },
            Err(e) => {
                eprintln!("stderr: FATAL - Failed to parse address: {}", e);
                std::io::stderr().flush().ok();
                return Err(Box::new(e) as Box<dyn std::error::Error>);
            }
        };

        eprintln!("stderr: DEBUG - Creating service...");
        std::io::stderr().flush().ok();
        let service = SublinearServiceImpl::default();

        eprintln!("stderr: DEBUG - Service created");
        std::io::stderr().flush().ok();

        info!("🚀 Starting gRPC server on {}", addr);
        eprintln!("stderr: DEBUG - Building gRPC server...");
        std::io::stderr().flush().ok();

        let server_result = Server::builder()
            .add_service(SublinearServiceServer::new(service))
            .serve(addr)
            .await;

        match server_result {
            Ok(_) => {
                eprintln!("stderr: INFO - Server completed successfully");
                std::io::stderr().flush().ok();
                Ok(())
            },
            Err(e) => {
                eprintln!("stderr: ERROR - Server error: {}", e);
                std::io::stderr().flush().ok();
                Err(Box::new(e) as Box<dyn std::error::Error>)
            }
        }
    });

    eprintln!("stderr: DEBUG - Async block returned");
    std::io::stderr().flush().ok();

    match result {
        Ok(_) => {
            eprintln!("stderr: INFO - Server stopped normally");
            std::io::stderr().flush().ok();
        },
        Err(e) => {
            eprintln!("stderr: ERROR - Server failed: {}", e);
            std::io::stderr().flush().ok();
            return Err(e);
        }
    }

    Ok(())
}
