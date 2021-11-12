package main

import (
	// "fmt"

	"encoding/json"
	"log"

	// "net/http"
	// "github.com/gin-gonic/gin"
	"github.com/streadway/amqp"
)

// func main() {
// 	fmt.Println(query)
// 	router := gin.Default()
// 	router.GET("/api", func(c *gin.Context) {
// 		c.IndentedJSON(http.StatusOK, query)
// 	})
// 	router.Run(":7777")
// }

func main() {
	var body []byte // body to send
	decoded := config()
	body, _ = json.Marshal(decoded)
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	defer conn.Close()
	failHanler(err, "Failed to connect to RabbitMQ")
	ch, err := conn.Channel()
	defer ch.Close()
	failHanler(err, "Failed to open a channel")
	q, err := ch.QueueDeclare(
		"hello", // name of queue
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failHanler(err, "Failed to declare a queue")

	// body := "Hello World, It's Go!"
	err = ch.Publish(
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		})
	failHanler(err, "Failed to publish a message")
}

func failHanler(err error, msg string) {
	if err != nil {
		log.Fatal(err, msg)
	}
}
