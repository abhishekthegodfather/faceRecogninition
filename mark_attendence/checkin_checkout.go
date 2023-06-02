package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-sql-driver/mysql"
)

func attendenceDBConnector() *sql.DB {
	var db *sql.DB
	config := mysql.Config{
		User:   "root",
		Passwd: "cubastion",
		Net:    "tcp",
		Addr:   "127.0.0.1:3306",
		DBName: "attendencedB",
		Params: map[string]string{
			"allowNativePasswords": "true",
		},
	}

	var err error
	db, err = sql.Open("mysql", config.FormatDSN())

	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()

	if pingErr != nil {
		log.Fatal(pingErr)
	}

	fmt.Println("Connected to Attendence DB")
	return db
}

func biometricDBConnector() *sql.DB {
	var db *sql.DB
	config := mysql.Config{
		User:   "root",
		Passwd: "cubastion",
		Net:    "tcp",
		Addr:   "127.0.0.1:3306",
		DBName: "demoBiometricDB",
		Params: map[string]string{
			"allowNativePasswords": "true",
		},
	}

	var err error
	db, err = sql.Open("mysql", config.FormatDSN())

	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()

	if pingErr != nil {
		log.Fatal(pingErr)
	}

	fmt.Println("Connected to Biometric DB")
	return db
}

func markAttendence(c *gin.Context) {
	var json struct {
		EmpCode string `json:"emp_code"`
	}
	err := c.ShouldBindJSON(&json)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Employee code is missing"})
		return
	}

	var empCodeExists bool
	var db *sql.DB = biometricDBConnector()
	fmt.Println(json.EmpCode)
	err = db.QueryRow("SELECT EXISTS(SELECT emp_code FROM devbiometricDB WHERE emp_code = ?)", json.EmpCode).Scan(&empCodeExists)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query database"})
		return
	} else {
		fmt.Println("Suceessfully Query in BiometricDB")
	}

	if !empCodeExists {
		c.JSON(http.StatusNotFound, gin.H{"error": "Employee not found"})
		return
	}

	var checkInTime sql.NullString
	var adb = attendenceDBConnector()
	defer adb.Close()

	err = adb.QueryRow("SELECT check_in FROM attendenceDB WHERE emp_code = ? ORDER BY id DESC LIMIT 1", json.EmpCode).Scan(&checkInTime)
	if err != nil && err != sql.ErrNoRows {
		fmt.Println("Failed to query database")
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query database"})
		return
	}

	currentDateTime := time.Now().Format("2006-01-02 15:04:05")

	if err == sql.ErrNoRows || !checkInTime.Valid || checkInTime.String[:10] != currentDateTime[:10] {
		// Check-in
		_, err = adb.Exec("INSERT INTO attendenceDB (emp_code, check_in, check_out, attendance_date) VALUES (?, ?, NULL, ?)", json.EmpCode, currentDateTime, currentDateTime[:10])
		if err != nil {
			fmt.Println("Failed to update attendance")
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update attendance"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Checked in successfully"})
	} else {
		// Check-out
		_, err = adb.Exec("UPDATE attendenceDB SET check_out = ? WHERE emp_code = ? AND attendance_date = ?", currentDateTime, json.EmpCode, currentDateTime[:10])
		if err != nil {
			fmt.Println("Failed to update attendance")
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update attendance"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Checked out successfully"})
	}
}

func setupPostAttendence() {
	var err error
	router := gin.Default()
	router.PUT("/attendance", markAttendence)
	err = router.Run(":8000")
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	setupPostAttendence()
}
