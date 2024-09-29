package config

import (
	"encoding/json"
	"fmt"
	"os"
)

var (
	Token     string
	BotPrefix string
	GiphyKey  string
	RiotKey   string

	config *configStruct
)

type configStruct struct {
	Token     string `json:"Token"`
	BotPrefix string `json:"BotPrefix"`
	GiphyKey  string `json:"GiphyAPIKey"`
	RiotKey   string `json:"RiotKey"`
}

func ReadConfig() error {
	fmt.Println("Reading from config file...")

	file, err := os.ReadFile("./config/config.json")

	if err != nil {
		fmt.Println(err.Error())
		return err
	}

	err = json.Unmarshal(file, &config)

	if err != nil {
		fmt.Println(err.Error())
		return err
	}

	Token = config.Token
	BotPrefix = config.BotPrefix
	GiphyKey = config.GiphyKey
	RiotKey = config.RiotKey

	return nil
}
