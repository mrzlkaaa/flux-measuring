package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/streadway/amqp"
)

func response() {
	// conn, err := amqp.Dial("amqp://guest:guest@rabbit:5672/")
	amqpServer := os.Getenv("AMQP_SERVER_URL")
	conn, err := amqp.Dial(amqpServer)
	defer conn.Close()
	failHanler(err, "Failed to connect to RabbitMQ")
	ch, err := conn.Channel()
	defer ch.Close()
	failHanler(err, "Failed to open a channel")
	q, err := ch.QueueDeclare(
		"rpc", // name of queue
		false, // durable
		false, // delete when unused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	failHanler(err, "Failed to declare a queue")
	err = ch.Qos(
		1,     // prefetch count
		0,     // prefetch size
		false, // global
	)
	failHanler(err, "Failed to set QoS")
	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failHanler(err, "Failed to register a consumer")

	forever := make(chan bool)
	go func() {
		for d := range msgs {
			// n, err := strconv.Atoi(string(d.Body))
			id, err := strconv.ParseInt(string(d.Body), 10, 64)
			failHanler(err, "Failed to convert body to integer")
			fmt.Println(id)
			queryResponse := config(id)
			response, _ := json.Marshal(queryResponse)

			err = ch.Publish(
				"",        // exchange
				d.ReplyTo, // routing key
				false,     // mandatory
				false,     // immediate
				amqp.Publishing{
					ContentType:   "text/plain",
					CorrelationId: d.CorrelationId,
					Body:          response,
				})
			failHanler(err, "Failed to publish a message")

			d.Ack(false)
		}
	}()
	log.Printf(" [*] Awaiting RPC requests")
	<-forever
}

func fib(n int) int {
	if n == 0 {
		return 0
	} else if n == 1 {
		return 1
	} else {
		return fib(n-1) + fib(n-2)
	}
}

func failHanler(err error, msg string) {
	if err != nil {
		log.Fatal(err, msg)
	}
}
