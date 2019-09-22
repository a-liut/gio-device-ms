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
	"gio-device-ms/pkg/model"
	"gio-device-ms/pkg/repository"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func GetRoomById(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["roomId"]

	repo, _ := repository.NewRoomRepository()
	room, err := repo.Get(id)

	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if room == nil {
		errorHandler(w, http.StatusNotFound, "room not found")
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(room); err != nil {
		log.Println(err)
	}
}

func GetRooms(w http.ResponseWriter, _ *http.Request) {
	repo, _ := repository.NewRoomRepository()
	rooms, err := repo.GetAll()

	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(rooms); err != nil {
		log.Println(err)
	}
}

func CreateRoom(w http.ResponseWriter, r *http.Request) {
	var roomData model.Room

	err := json.NewDecoder(r.Body).Decode(&roomData)
	if err != nil {
		errorHandler(w, http.StatusBadRequest, "Invalid data")
		return
	}

	if _, err := roomData.Validate(); err != nil {
		errorHandler(w, http.StatusBadRequest, err.Error())
	}

	repo, _ := repository.NewRoomRepository()

	room, err := repo.GetByName(roomData.Name)
	if err != nil {
		errorHandler(w, http.StatusInternalServerError, err.Error())
		return
	}

	if room == nil {
		// Create a new room
		room, err = repo.Insert(&roomData)

		if err != nil {
			errorHandler(w, http.StatusInternalServerError, err.Error())
			return
		}
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(room); err != nil {
		log.Println(err)
	}
}
