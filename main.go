package main

import (
	"fmt"

	"github.com/maland1/malenia-bot/bot"
	"github.com/maland1/malenia-bot/config"
)

func main() {
	err := config.ReadConfig()
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	bot.Start()

	<-make(chan struct{})
	return
}
