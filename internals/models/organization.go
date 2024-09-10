package models

import (
	"database/sql/driver"
	"github.com/jackc/pgx/v5/pgtype"
	"gorm.io/gorm"
)

type organizationType string

const (
	ie  organizationType = "IE"
	llc organizationType = "LLC"
	jsc organizationType = "JSC"
)

func (ot *organizationType) Scan(value interface{}) error {
	*ot = organizationType(value.([]byte))
	return nil
}

func (ot organizationType) Value() (driver.Value, error) {
	return string(ot), nil
}

type Organization struct {
	gorm.Model
	ID               uint             `gorm:"primaryKey;auto_increment"`
	Name             string           `json:"name"`
	Description      string           `json:"description"`
	OrganizationType organizationType `gorm:"type:organization_type" json:"organization_type"`
	CreatedAt        pgtype.Timestamp `json:"created_at"`
	UpdatedAt        pgtype.Timestamp `json:"updated_at"`
}
