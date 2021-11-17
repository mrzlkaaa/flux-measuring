package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func handler(c *gin.Context) {
	param := c.Param("id")
	converted, _ := strconv.ParseInt(param, 10, 64)
	fmt.Println(converted)
	queryResponse := config(converted)
	c.IndentedJSON(http.StatusOK, queryResponse)
}

func main() {
	router := gin.Default()
	router.Use(cors.Default())
	router.GET("/api/experiment/:id", handler)
	router.Run(":8080")
}
