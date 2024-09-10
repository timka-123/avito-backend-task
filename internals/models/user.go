package models

import (
	"github.com/jackc/pgx/v5/pgtype"
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	ID        int `gorm:"primaryKey;auto_increment" json:"id"`
	Username  string
	FirstName string           `json:"first_name"`
	LastName  string           `json:"last_name"`
	CreatedAt pgtype.Timestamp `json:"created_at"`
	UpdatedAt pgtype.Timestamp `json:"updated_at"`
}
