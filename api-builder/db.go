package main

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Tabler interface {
	TableName() string
}

type Experiment struct {
	ID      int64
	Name    string   `gorm:"default:newTestInsert"`
	Samples []Sample `gorm:"foreignKey:Exp_id"`
}

type Sample struct {
	ID       int64
	Activity float64
	Exp_id   int64
}

func config(id int64) map[string]interface{} {
	dsn := "host=irt-t.ru user=postgres password=postgres dbname=Detectors port=1111 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("connection failed")
	}
	// exper := ExperimentConstructor(id)
	sample := SampleConstructor()
	allSamples := AllSampleConstructor()
	fmt.Printf("Type of struct slice is %T\n", &allSamples)
	sample.TableName()
	samplesAll := db.Where(&[]Sample{{Exp_id: id}}).Find(&allSamples)
	fmt.Println(samplesAll.Error)
	filteredQuery := queryFormatting(allSamples)
	return filteredQuery

}

func queryFormatting(sp []Sample) map[string]interface{} {

	var sliceID []int64
	var sliceAct []float64
	for _, v := range sp {
		sliceID = append(sliceID, v.ID)
		sliceAct = append(sliceAct, v.Activity)
	}
	mapping := map[string]interface{}{
		"ID":       sliceID,
		"Activity": sliceAct,
	}
	fmt.Println(mapping)
	return mapping
}

func (*Experiment) TableName() string {
	return "experiment"
}

func ExperimentConstructor(id int64) *Experiment {
	return &Experiment{ID: id}
	// return &Experiment{Name: name}
}

func (*Sample) TableName() string {
	return "sample"
}

func SampleConstructor() *Sample {
	return &Sample{}
}

func AllSampleConstructor() []Sample {
	return []Sample{}
}
