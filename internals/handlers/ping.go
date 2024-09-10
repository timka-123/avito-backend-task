package handlers

import "github.com/gofiber/fiber/v3"

func PingHandler(c fiber.Ctx) error {
	return c.SendString("ok")
}
