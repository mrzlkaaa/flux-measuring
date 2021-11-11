package DataBase

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func config() {
	dsn := "host=irt-t.ru user=postgres password=postgres dbname=sample port=1111 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	fmt.Println(db, err)
}
