package routes

import (
	"avito-backend-task/internals/handlers"
	"github.com/gofiber/fiber/v3"
)

func SetupRoutes(router fiber.Router) {
	router.Get("/", handlers.PingHandler)
}
