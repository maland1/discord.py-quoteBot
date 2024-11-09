package bot

import (
	"fmt"
	"strings"
	"time"

	"github.com/bwmarrin/discordgo"
	"github.com/jasonlvhit/gocron"
	"github.com/maland1/malenia-bot/config"
)

// BotID is id for bot
var BotID string
var goBot *discordgo.Session

func userWelcome(s *discordgo.Session, u *discordgo.GuildMemberAdd) {
	addNewUser(u.User)
	return
}

func profileEmbed(s *discordgo.Session, m *discordgo.MessageCreate) {
	exp, mexp := findExp(m)
	pos := findPos(m, exp)
	mpos := findMonthlyPos(m, mexp)

	mE := new(discordgo.MessageEmbed)
	mE.Color = 9693630
	mE.Description = fmt.Sprintf("Chat exp = %v\nChat rank = %v\nAvg Msg Length = %v\nAML rank = %v", exp, pos)

	author := new(discordgo.MessageEmbedAuthor)
	author.Name = fmt.Sprintf("%s's profile", m.Author.Username)
	author.IconURL = m.Author.AvatarURL("128")
	mE.Author = author

	footer := new(discordgo.MessageEmbedFooter)
	member, _ := s.GuildMember(QuantexID, m.Author.ID)
	// Was timestamp, is now time.Time
	time, _ := member.JoinedAt.Parse()
	footer.Text = fmt.Sprintf("Joined on %v", time.Format("02/01/2006 15:04"))
	mE.Footer = footer

	f2 := new(discordgo.MessageEmbedField)
	f2.Inline = true
	f2.Name = "Monthly"
	f2.Value = fmt.Sprintf("Chat exp = %v\nChat rank = %v", mexp, mpos)
	mE.Fields = append(mE.Fields, f2)

	_, err3 := s.ChannelMessageSendEmbed(BotCommandsChannel, mE)
	if err3 != nil {
		fmt.Println(err3.Error())
	}
}

func messageHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Author.ID == BotID {
		return
	}
	addExp(m)

	if strings.HasPrefix(m.Content, "!lolstats") {
		m.Content = m.Content[10:]
		commandLeagueStats(s, m)
	} else if m.ChannelID == BotCommandsChannel {
		if strings.HasPrefix(m.Content, config.BotPrefix) {
			switch m.Content {
			case "!help":
				_, _ = s.ChannelMessageSend(BotCommandsChannel, "```Command list: cointoss, top, topMonth, me```")
			case "!cointoss":
				commandCointoss(s, m)
			case "!top":
				printLeaderboard(s, m)
			case "!topmonth":
				printMonthlyLeaderboard(s, m)
			case "!me":
				profileEmbed(s, m)
			default:
				_, _ = s.ChannelMessageSend(BotCommandsChannel, "```Invalid command, !help for the command list```")
			}
		}
	}

}

func task(s *discordgo.Session) {
	t := time.Now()
	if t.Weekday() == 1 {
		updateUserNames(s)
	}
	if t.Day() == 1 {
		getMonthlyExp(s)
		clearMonthlyExp()
	}
}

// Start is bot keep awake function
func Start() {
	goBot, err := discordgo.New("Bot " + config.Token)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	u, err := goBot.User("@me")
	if err != nil {
		fmt.Println(err.Error())
	}

	BotID = u.ID
	goBot.AddHandler(userWelcome)
	goBot.AddHandler(messageHandler)
	goBot.AddHandler(voiceHandler)

	err = goBot.Open()
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	fmt.Println("Bot is running!")
	gocron.Every(1).Day().At("00:00").Do(task, goBot)
	<-gocron.Start()
}
