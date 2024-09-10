package main

import (
	"avito-backend-task/internals/routes"
	"github.com/gofiber/fiber/v3"
	"log"
)

func SetupRoutes(app *fiber.App) {
	api := app.Group("/api")

	pingGroup := api.Group("/ping")
	routes.SetupRoutes(pingGroup)
}

func main() {
	app := fiber.New()

	SetupRoutes(app)
	log.Fatal(app.Listen(":8080"))
}
