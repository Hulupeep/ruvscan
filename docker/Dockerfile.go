# Go Scanner Dockerfile

# Build stage
FROM golang:1.21-alpine as builder

WORKDIR /build

# Copy go mod files
COPY src/go/go.mod src/go/go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY src/go/scanner ./scanner

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o scanner ./scanner

# Runtime stage
FROM alpine:latest

WORKDIR /app

# Install ca-certificates for HTTPS
RUN apk --no-cache add ca-certificates

# Copy binary from builder
COPY --from=builder /build/scanner /app/

# Run the scanner
CMD ["./scanner"]
