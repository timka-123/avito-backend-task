package database

import (
	"avito-backend-task/config"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func Connect() {
	var err error
	DB, err = gorm.Open(postgres.Open(config.Config("POSTGRES_JDBC_URL")))
	if err != nil {
		panic("Error while connecting to db")
	}
}
