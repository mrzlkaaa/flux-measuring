package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	config()
	router := gin.Default()
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  200,
			"message": "Welcome To API",
		})
	})
	router.Run(":4747")
}
