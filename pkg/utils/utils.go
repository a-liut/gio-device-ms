package utils

import (
	"bytes"
	"net/http"
)

func DoPost(u string, bodyData *bytes.Buffer) (*http.Response, error) {
	if bodyData != nil {
		return http.Post(u, "application/json", bodyData)
	}

	return http.Post(u, "application/json", nil)
}
