/*
RuvScan GitHub Scanner
Concurrent workers for fetching and analyzing GitHub repositories
*/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/google/go-github/v57/github"
	"golang.org/x/oauth2"
)

const (
	Version      = "0.5.0"
	MaxWorkers   = 10
	RateLimitPad = 100 // Keep 100 requests in reserve
)

// ScanConfig holds scanning configuration
type ScanConfig struct {
	SourceType string `json:"source_type"`
	SourceName string `json:"source_name"`
	Limit      int    `json:"limit"`
	Token      string `json:"token"`
	MCPEndpoint string `json:"mcp_endpoint"`
}

// RepoData holds repository information
type RepoData struct {
	Name        string   `json:"name"`
	Org         string   `json:"org"`
	FullName    string   `json:"full_name"`
	Description string   `json:"description"`
	Topics      []string `json:"topics"`
	README      string   `json:"readme"`
	Stars       int      `json:"stars"`
	Language    string   `json:"language"`
}

// Scanner manages concurrent GitHub scanning
type Scanner struct {
	client      *github.Client
	config      ScanConfig
	workers     int
	results     chan *RepoData
	errors      chan error
	wg          sync.WaitGroup
}

// NewScanner creates a new scanner instance
func NewScanner(config ScanConfig) *Scanner {
	ctx := context.Background()

	var tc *http.Client
	if config.Token != "" {
		ts := oauth2.StaticTokenSource(
			&oauth2.Token{AccessToken: config.Token},
		)
		tc = oauth2.NewClient(ctx, ts)
	}

	client := github.NewClient(tc)

	return &Scanner{
		client:  client,
		config:  config,
		workers: MaxWorkers,
		results: make(chan *RepoData, 100),
		errors:  make(chan error, 100),
	}
}

// ScanOrg scans all repos in a GitHub organization
func (s *Scanner) ScanOrg(ctx context.Context) error {
	log.Printf("Scanning organization: %s", s.config.SourceName)

	opts := &github.RepositoryListByOrgOptions{
		Type:        "public",
		ListOptions: github.ListOptions{PerPage: 100},
	}

	repoCount := 0
	for {
		repos, resp, err := s.client.Repositories.ListByOrg(ctx, s.config.SourceName, opts)
		if err != nil {
			return fmt.Errorf("error listing repos: %w", err)
		}

		// Process repos concurrently
		for _, repo := range repos {
			if repoCount >= s.config.Limit {
				return nil
			}

			s.wg.Add(1)
			go s.processRepo(ctx, repo)
			repoCount++
		}

		if resp.NextPage == 0 {
			break
		}
		opts.Page = resp.NextPage

		// Check rate limit
		if err := s.checkRateLimit(ctx); err != nil {
			return err
		}
	}

	return nil
}

// processRepo fetches and processes a single repository
func (s *Scanner) processRepo(ctx context.Context, repo *github.Repository) {
	defer s.wg.Done()

	// Fetch README
	readme, err := s.fetchREADME(ctx, repo)
	if err != nil {
		log.Printf("Warning: Could not fetch README for %s: %v", *repo.FullName, err)
		readme = ""
	}

	// Create repo data
	data := &RepoData{
		Name:        repo.GetName(),
		Org:         repo.GetOwner().GetLogin(),
		FullName:    repo.GetFullName(),
		Description: repo.GetDescription(),
		Topics:      repo.Topics,
		README:      readme,
		Stars:       repo.GetStargazersCount(),
		Language:    repo.GetLanguage(),
	}

	s.results <- data

	// Send to MCP server
	if err := s.sendToMCP(data); err != nil {
		s.errors <- fmt.Errorf("failed to send to MCP: %w", err)
	}
}

// fetchREADME retrieves repository README content
func (s *Scanner) fetchREADME(ctx context.Context, repo *github.Repository) (string, error) {
	readme, _, err := s.client.Repositories.GetReadme(
		ctx,
		repo.GetOwner().GetLogin(),
		repo.GetName(),
		nil,
	)
	if err != nil {
		return "", err
	}

	content, err := readme.GetContent()
	if err != nil {
		return "", err
	}

	return content, nil
}

// checkRateLimit checks GitHub API rate limit
func (s *Scanner) checkRateLimit(ctx context.Context) error {
	rate, _, err := s.client.RateLimits(ctx)
	if err != nil {
		return err
	}

	core := rate.GetCore()
	remaining := core.Remaining

	log.Printf("Rate limit: %d/%d remaining", remaining, core.Limit)

	if remaining < RateLimitPad {
		resetTime := core.Reset.Time
		sleepDuration := time.Until(resetTime)
		log.Printf("Rate limit low, sleeping until %v (%v)", resetTime, sleepDuration)
		time.Sleep(sleepDuration)
	}

	return nil
}

// sendToMCP sends repo data to Python MCP server
func (s *Scanner) sendToMCP(data *RepoData) error {
	if s.config.MCPEndpoint == "" {
		return nil // No endpoint configured
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}

	// TODO: Implement HTTP POST to MCP /ingest endpoint
	_ = jsonData

	return nil
}

// Run executes the scan
func (s *Scanner) Run() error {
	ctx := context.Background()

	// Start result processor
	go s.processResults()

	// Execute scan based on source type
	var err error
	switch s.config.SourceType {
	case "org":
		err = s.ScanOrg(ctx)
	case "user":
		// TODO: Implement user scanning
		err = fmt.Errorf("user scanning not yet implemented")
	case "topic":
		// TODO: Implement topic scanning
		err = fmt.Errorf("topic scanning not yet implemented")
	default:
		err = fmt.Errorf("unknown source type: %s", s.config.SourceType)
	}

	// Wait for all workers to complete
	s.wg.Wait()
	close(s.results)
	close(s.errors)

	return err
}

// processResults handles incoming results
func (s *Scanner) processResults() {
	for {
		select {
		case result, ok := <-s.results:
			if !ok {
				return
			}
			log.Printf("Processed: %s (%d stars)", result.FullName, result.Stars)

		case err, ok := <-s.errors:
			if !ok {
				return
			}
			log.Printf("Error: %v", err)
		}
	}
}

func main() {
	log.Printf("RuvScan GitHub Scanner v%s", Version)

	// Load config from environment or file
	config := ScanConfig{
		SourceType: os.Getenv("RUVSCAN_SOURCE_TYPE"),
		SourceName: os.Getenv("RUVSCAN_SOURCE_NAME"),
		Limit:      50, // Default limit
		Token:      os.Getenv("GITHUB_TOKEN"),
		MCPEndpoint: os.Getenv("RUVSCAN_MCP_ENDPOINT"),
	}

	if config.SourceType == "" || config.SourceName == "" {
		log.Fatal("RUVSCAN_SOURCE_TYPE and RUVSCAN_SOURCE_NAME must be set")
	}

	scanner := NewScanner(config)

	if err := scanner.Run(); err != nil {
		log.Fatalf("Scan failed: %v", err)
	}

	log.Println("Scan completed successfully")
}
