/*
 * Devices Microservice
 *
 * Microservice for managing Giò Plants devices
 *
 * API version: 1.0.0
 * Contact: andrea.liut@gmail.com
 * Generated by: Swagger Codegen (https://github.com/swagger-api/swagger-codegen.git)
 */
package api

import (
	"encoding/json"
	"fmt"
	"gio-device-ms/pkg/model"
	"gio-device-ms/pkg/repository"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
)

func GetDeviceById(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["deviceId"]
	roomId := vars["roomId"]

	repo, _ := repository.NewDeviceRepository()
	device, _ := repo.Get(id)

	if device == nil || device.Room != roomId {
		errorHandler(w, http.StatusNotFound, "device not found")
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(device); err != nil {
		log.Println(err)
	}
}

func GetDevices(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	roomId := vars["roomId"]

	roomRepo, err := repository.NewRoomRepository()
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	room, err := roomRepo.Get(roomId)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if room == nil {
		errorHandler(w, http.StatusNotFound, "room not found")
		return
	}

	repo, _ := repository.NewDeviceRepository()
	devices, err := repo.GetAll(roomId)

	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(devices); err != nil {
		log.Println(err)
	}
}

func CreateDevice(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	roomId := vars["roomId"]

	var d model.Device

	err := json.NewDecoder(r.Body).Decode(&d)
	if err != nil {
		errorHandler(w, http.StatusBadRequest, "Invalid data")
		return
	}

	d.Room = roomId

	if _, err := d.Validate(); err != nil {
		errorHandler(w, http.StatusBadRequest, err.Error())
		return
	}

	// Check room
	roomRepo, _ := repository.NewRoomRepository()
	room, err := roomRepo.Get(d.Room)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if room == nil {
		errorHandler(w, http.StatusBadRequest, "room not found")
		return
	}

	repo, _ := repository.NewDeviceRepository()

	// Check if the device has been already registered
	device, err := repo.GetByMAC(d.Mac)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if device == nil {
		// Create a new device
		device, err = repo.Insert(&d)
		if err != nil {
			errorHandler(w, http.StatusInternalServerError, err.Error())
			return
		}
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(device); err != nil {
		log.Println(err)
	}
}

func GetAllDeviceReadings(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["deviceId"]
	roomId := vars["roomId"]

	// Query parameters
	lim := r.URL.Query().Get("limit")
	limit, err := strconv.Atoi(lim)
	if err != nil {
		limit = -1 // Take all readings
	}

	name := r.URL.Query().Get("name")

	repo, _ := repository.NewDeviceRepository()

	device, err := repo.Get(id)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if device == nil || device.Room != roomId {
		errorHandler(w, http.StatusNotFound, "device not found")
		return
	}

	readings, err := repo.GetReadings(id, limit, name)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(readings); err != nil {
		log.Println(err)
	}
}

func CreateDeviceReadings(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["deviceId"]
	roomId := vars["roomId"]

	var reading model.Reading
	err := json.NewDecoder(r.Body).Decode(&reading)
	if err != nil {
		errorHandler(w, http.StatusBadRequest, "Invalid data")
		return
	}

	repo, _ := repository.NewDeviceRepository()

	device, err := repo.Get(id)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if device == nil || device.Room != roomId {
		errorHandler(w, http.StatusNotFound, "device not found")
		return
	}

	res, err := repo.InsertReading(device, &reading)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(res); err != nil {
		log.Println(err)
	}
}

func getActionData(r *http.Request) *model.ActionData {
	var actionData model.ActionData
	err := json.NewDecoder(r.Body).Decode(&actionData)
	if err != nil {
		return nil
	}

	return &actionData
}

func TriggerDeviceAction(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["deviceId"]
	roomId := vars["roomId"]
	actionName := vars["actionName"]

	log.Printf("TriggerDeviceAction called: %s", actionName)

	actionData := getActionData(r)
	if actionData == nil {
		log.Printf("WARNING: no data passed for action %s", actionName)
	}

	repo, _ := repository.NewDeviceRepository()
	device, _ := repo.Get(id)

	if device == nil || device.Room != roomId {
		errorHandler(w, http.StatusNotFound, "device not found")
		return
	}

	errors, oneSuccessful := device.TriggerAction(actionName, actionData)

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	code := http.StatusOK

	m := "Action performed"
	if !oneSuccessful {
		code = http.StatusBadRequest
		m = "Cannot perform action %s: ["

		errorStrings := make([]string, len(errors))
		for i, err := range errors {
			errorStrings[i] = err.Error()
		}

		m = fmt.Sprintf("%s%s]", m, strings.Join(errorStrings, ","))
	}

	res := model.ApiResponse{
		Code:    code,
		Message: m,
	}

	w.WriteHeader(code)
	if err := json.NewEncoder(w).Encode(res); err != nil {
		log.Println(err)
	}
}
