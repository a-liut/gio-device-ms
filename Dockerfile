FROM golang:alpine AS builder

# Install git for fetching dependencies
RUN apk update && apk add --no-cache git

WORKDIR /devicems

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

# Build the binary.
RUN go build -o /go/bin/devicems cmd/devicems/main.go

## Build lighter image
FROM alpine:latest

# Copy our static executable.
COPY --from=builder /go/bin/devicems /devicems

EXPOSE 8080

# Run the binary.
ENTRYPOINT /devicems