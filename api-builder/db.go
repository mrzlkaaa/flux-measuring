package main

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Tabler interface {
	TableName() string
}

type gormtest struct {
	ID   uint
	Name string `gorm:"default:newTestInsert"`
	Age  int64  `gorm:"default:22"`
}

type Experiment struct {
	ID      uint
	Name    string   `gorm:"default:newTestInsert"`
	Samples []Sample `gorm:"foreignKey:Exp_id"`
}

type Sample struct {
	ID       uint
	Activity float64
	Exp_id   uint
}

func config() *[]Sample {
	dsn := "host=irt-t.ru user=postgres password=postgres dbname=Detectors port=1111 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("connection failed")
	}
	exper := ExperimentConstructor()
	sample := SampleConstructor()
	allSamples := AllSampleConstructor()
	exper.TableName()
	sample.TableName()
	// experFirst := db.First(exper)
	// sampleFirst := db.First(sample)
	samplesAll := db.Find(allSamples)
	fmt.Println(samplesAll.Error)
	// fmt.Println(exper.Name, experFirst.Error)
	// fmt.Println(sample.Activity, sampleFirst.RowsAffected)
	return allSamples

}

func (*Experiment) TableName() string {
	return "experiment"
}

func ExperimentConstructor() *Experiment {
	return &Experiment{}
}

func (*Sample) TableName() string {
	return "sample"
}

func SampleConstructor() *Sample {
	return &Sample{}
}

func AllSampleConstructor() *[]Sample {
	return &[]Sample{}
}
