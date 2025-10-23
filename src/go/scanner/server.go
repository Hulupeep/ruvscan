/*
HTTP server for scanner - waits for API trigger instead of auto-running
*/

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// ScanRequest represents an API request to trigger a scan
type ScanRequest struct {
	SourceType string `json:"source_type"`
	SourceName string `json:"source_name"`
	Limit      int    `json:"limit"`
}

// ScanResponse represents the API response
type ScanResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
	Scanned int    `json:"scanned"`
}

// ScannerServer wraps the scanner with HTTP endpoints
type ScannerServer struct {
	port  string
	token string
	mcpEndpoint string
}

// NewScannerServer creates a new scanner HTTP server
func NewScannerServer() *ScannerServer {
	port := os.Getenv("SCANNER_PORT")
	if port == "" {
		port = "8080"
	}

	return &ScannerServer{
		port:        port,
		token:       os.Getenv("GITHUB_TOKEN"),
		mcpEndpoint: os.Getenv("RUVSCAN_MCP_ENDPOINT"),
	}
}

// handleHealth returns service health status
func (s *ScannerServer) handleHealth(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"status":  "healthy",
		"version": Version,
		"service": "RuvScan GitHub Scanner",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// handleScan triggers a GitHub scan
func (s *ScannerServer) handleScan(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ScanRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("Invalid request: %v", err), http.StatusBadRequest)
		return
	}

	// Validate request
	if req.SourceType == "" || req.SourceName == "" {
		http.Error(w, "source_type and source_name are required", http.StatusBadRequest)
		return
	}

	if req.Limit == 0 {
		req.Limit = 50 // Default limit
	}

	// Create scanner config
	config := ScanConfig{
		SourceType:  req.SourceType,
		SourceName:  req.SourceName,
		Limit:       req.Limit,
		Token:       s.token,
		MCPEndpoint: s.mcpEndpoint,
	}

	// Run scan in background
	go func() {
		scanner := NewScanner(config)
		if err := scanner.Run(); err != nil {
			log.Printf("Scan error for %s/%s: %v", req.SourceType, req.SourceName, err)
		} else {
			log.Printf("Scan completed for %s/%s", req.SourceType, req.SourceName)
		}
	}()

	// Return immediate response
	response := ScanResponse{
		Status:  "started",
		Message: fmt.Sprintf("Scan initiated for %s: %s", req.SourceType, req.SourceName),
		Scanned: 0,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(response)
}

// handleStatus returns current scanner status
func (s *ScannerServer) handleStatus(w http.ResponseWriter, r *http.Request) {
	status := map[string]interface{}{
		"status":       "ready",
		"version":      Version,
		"github_token": s.token != "",
		"mcp_endpoint": s.mcpEndpoint,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

// Start begins the HTTP server
func (s *ScannerServer) Start() error {
	mux := http.NewServeMux()

	// Register endpoints
	mux.HandleFunc("/health", s.handleHealth)
	mux.HandleFunc("/scan", s.handleScan)
	mux.HandleFunc("/status", s.handleStatus)

	// Create server with timeouts
	server := &http.Server{
		Addr:         ":" + s.port,
		Handler:      mux,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Printf("Scanner HTTP server starting on port %s", s.port)
	log.Printf("Endpoints:")
	log.Printf("  GET  /health - Health check")
	log.Printf("  GET  /status - Scanner status")
	log.Printf("  POST /scan   - Trigger scan (body: {\"source_type\":\"org\",\"source_name\":\"owner\",\"limit\":50})")

	return server.ListenAndServe()
}

// RunServer starts the scanner as an HTTP service
func RunServer() error {
	server := NewScannerServer()
	return server.Start()
}
