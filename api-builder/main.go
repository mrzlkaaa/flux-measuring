package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	// This handler will match /user/john but will not match /user/ or /user
	router.GET("/user/:name", func(c *gin.Context) {
		name := c.Param("name")
		c.String(http.StatusOK, "Hello %s", name)
	})

	// However, this one will match /user/john/ and also /user/john/send
	// If no other routers match /user/john, it will redirect to /user/john/
	router.GET("/user/:name/*action", func(c *gin.Context) {
		name := c.Param("name")
		action := c.Param("action")
		message := name + " is " + action
		c.String(http.StatusOK, message)
	})

	// For each matched request Context will hold the route definition
	// router.POST("/user/:name/*action", func(c *gin.Context) {
	// 	c.FullPath() == "/user/:name/*action" // true
	// })

	// This handler will add a new router for /user/groups.
	// Exact routes are resolved before param routes, regardless of the order they were defined.
	// Routes starting with /user/groups are never interpreted as /user/:name/... routes
	// router.GET("/user/groups", func(c *gin.Context) {
	// 	c.String(http.StatusOK, "The available groups are [...]", name)
	// })

	router.Run(":8080")
}

// // album represents data about a record album.
// type album struct {
// 	ID     string  `json:"id"`
// 	Title  string  `json:"title"`
// 	Artist string  `json:"artist"`
// 	Price  float64 `json:"price"`
// }

// var albums = []album{
// 	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
// 	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
// 	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
// }

// func main() {
// 	http.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
// 		fmt.Fprintf(w, "Hello, %q", r.URL.Path)
// 	})
// 	fmt.Println("Hello!")
// 	router := gin.Default()
// 	router.LoadHTMLFiles("templates/home.html")
// 	router.GET("/", func(c *gin.Context) {
// 		c.HTML(http.StatusOK, "home.html", gin.H{
// 			"title": "Hello from Go",
// 		})
// 	})
// 	router.POST("/", func(c *gin.Context) {
// 		area := c.PostForm("Area")
// 		fmt.Println(area)
// 	})
// 	// router.GET("/", getAlbums)
// 	router.Run("localhost:8080")
// }

// func getAlbums(c *gin.Context) {
// 	c.IndentedJSON(http.StatusOK, albums)
// }
