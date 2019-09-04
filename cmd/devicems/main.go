/*
 * Devices service
 *
 * Microservice for managing Giò Plants devices
 *
 * API version: 1.0.0
 * Contact: andrea.liut@gmail.com
 * Generated by: Swagger Codegen (https://github.com/swagger-api/swagger-codegen.git)
 */

package main

import (
	"flag"
	"fmt"
	"gio-device-ms/pkg/api"
	"log"
	"net/http"
)

func main() {
	port := flag.Int("port", 8080, "port to be used")

	flag.Parse()

	log.Printf("Server started on port %d", *port)

	router := api.NewRouter()

	p := fmt.Sprintf(":%d", *port)

	log.Fatal(http.ListenAndServe(p, router))
}
