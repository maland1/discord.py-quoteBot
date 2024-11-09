package bot

import (
	"database/sql"
	"fmt"
	"strconv"

	"github.com/bwmarrin/discordgo"
)

type user struct {
	user_id    string
	discord_id string
	name       string
	birthday   string
	exp        int
	mexp       int
}

// DB is open SQLite database
var DB sql.DB = openDB()

func openDB() sql.DB {
	DB, err := sql.Open("sqlite3", "./database.db")
	if err != nil {
		fmt.Println(err.Error())
	}
	return *DB
}

func fillDB(ml []*discordgo.Member) {
	for i := 0; i < len(ml); i++ {
		sqlStmt, err := DB.Prepare("INSERT INTO users (discord_id, name, birthday) values (?, ?, ?);")
		if err != nil {
			fmt.Println(err.Error())
		}
		sqlStmt.Exec(ml[i].User.ID, ml[i].User.Username)
	}
}

func addNewUser(u *discordgo.User) {
	sqlStmt, err := DB.Prepare("INSERT INTO users (discord_id, name, birthday) values (?, ?, ?);")
	if err != nil {
		fmt.Println(err.Error())
	}
	sqlStmt.Exec(u.ID, u.Username)
}

func addExp(m *discordgo.MessageCreate) {
	u := new(user)
	err := DB.QueryRow("SELECT * FROM users WHERE discord_id = ?;", m.Author.ID).Scan(&u.user_id, &u.name, &u.exp)
	if err != nil {
		fmt.Println(err.Error())
	}
	sqlStmt, err := DB.Prepare("UPDATE users SET exp = ?, mexp = ?, WHERE discord_id = ?;")
	if err != nil {
		fmt.Println(err.Error())
	}
	u.exp = u.exp + 10
	u.mexp = u.mexp + 10

	sqlStmt.Exec(u.exp, u.mexp, m.Author.ID)
}

func printLeaderboard(s *discordgo.Session, m *discordgo.MessageCreate) {
	u := new(user)

	text := ""
	rows, _ := DB.Query("SELECT * FROM users ORDER BY exp DESC LIMIT 10;")
	defer rows.Close()
	for rows.Next() {
		rows.Scan(&u.user_id, &u.name, &u.exp, &u.mexp)
		text = text + u.name + ": " + strconv.Itoa(u.exp) + "\n"
	}

	mE := new(discordgo.MessageEmbed)
	mE.Color = 9693630
	mE.Title = "Leaderboards"

	f1 := new(discordgo.MessageEmbedField)
	f1.Inline = true
	f1.Name = "Text Chat"
	f1.Value = text
	mE.Fields = append(mE.Fields, f1)

	_, err := s.ChannelMessageSendEmbed(BotCommandsChannel, mE)
	if err != nil {
		fmt.Println(err.Error())
	}
}

func printMonthlyLeaderboard(s *discordgo.Session, m *discordgo.MessageCreate) {
	u := new(user)

	text := ""
	rows, _ := DB.Query("SELECT * FROM users ORDER BY mexp DESC LIMIT 10;")
	defer rows.Close()
	for rows.Next() {
		rows.Scan(&u.id, &u.name, &u.exp, &u.vexp, &u.mexp, &u.mvexp)
		text = text + u.name + ": " + strconv.Itoa(u.mexp) + "\n"
	}

	textVC := ""
	rowsVC, _ := DB.Query("SELECT * FROM users ORDER BY mvexp DESC LIMIT 10;")
	defer rowsVC.Close()
	for rowsVC.Next() {
		rowsVC.Scan(&u.id, &u.name, &u.exp, &u.vexp, &u.mexp, &u.mvexp)
		textVC = textVC + u.name + ": " + secsToHours(u.mvexp) + "\n"
	}

	mE := new(discordgo.MessageEmbed)
	mE.Color = 9693630
	mE.Title = "Monthly Leaderboards"

	f1 := new(discordgo.MessageEmbedField)
	f1.Inline = true
	f1.Name = "Text Chat"
	f1.Value = text
	mE.Fields = append(mE.Fields, f1)

	_, err := s.ChannelMessageSendEmbed(BotCommandsChannel, mE)
	if err != nil {
		fmt.Println(err.Error())
	}
}

func findExp(m *discordgo.MessageCreate) (int, int) {
	u := new(user)
	err := DB.QueryRow("SELECT * FROM users WHERE id = ?;", m.Author.ID).Scan(&u.id, &u.name, &u.exp, &u.mexp)
	if err != nil {
		fmt.Println(err.Error())
	}
	return u.exp, u.mexp
}

func findPos(m *discordgo.MessageCreate, exp int) int {
	var ranking int
	err := DB.QueryRow("SELECT COUNT (*) FROM users WHERE exp >= ?;", exp).Scan(&ranking)
	if err != nil {
		fmt.Println(err.Error())
	}
	return ranking
}

func clearWeeklyExp() {
	sqlStmt, err := DB.Prepare("UPDATE users SET wexp = 0;")
	if err != nil {
		fmt.Println(err.Error())
	}
	sqlStmt.Exec()
}

func clearMonthlyExp() {
	sqlStmt, err := DB.Prepare("UPDATE users SET mexp = 0;")
	if err != nil {
		fmt.Println(err.Error())
	}
	sqlStmt.Exec()
}

func getMonthlyExp(s *discordgo.Session) {
	u := new(user)
	message := "**```\nMost active users last month:\n"
	err := DB.QueryRow("SELECT * FROM users ORDER BY mexp DESC LIMIT 1;").Scan(&u.id, &u.name, &u.exp, &u.mexp)
	if err != nil {
		fmt.Println(err.Error())
	}
	message = message + "Text chat -> " + u.name + " with " + strconv.Itoa(u.mexp/10) + " messages sent!\n"
	_, _ = s.ChannelMessageSend(HallOfFameChannel, message)
}

func updateUserNames(s *discordgo.Session) {
	ml, err := s.GuildMembers("315176239008710656", "0", 1000)
	if err != nil {
		fmt.Println(err.Error())
	}
	for i := 0; i < len(ml); i++ {
		sqlStmt, err := DB.Prepare("UPDATE users SET name = ?, WHERE id = ?;")
		if err != nil {
			fmt.Println(err.Error())
		}
		sqlStmt.Exec(ml[i].User.Username, ml[i].User.ID)
	}
}

func findMonthlyPos(m *discordgo.MessageCreate, mexp int) int {
	var ranking int
	err := DB.QueryRow("SELECT COUNT (*) FROM users WHERE mexp >= ?;", mexp).Scan(&ranking)
	if err != nil {
		fmt.Println(err.Error())
	}
	return ranking
}
