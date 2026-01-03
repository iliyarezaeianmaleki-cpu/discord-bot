const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder } = require("discord.js");

const TOKEN = process.env.TOKEN; // توکن از Railway
const CLIENT_ID = process.env.CLIENT_ID; // آیدی اپلیکیشن

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

// تعریف دستور
const commands = [
  new SlashCommandBuilder()
    .setName("ping")
    .setDescription("تست آنلاین بودن ربات")
].map(cmd => cmd.toJSON());

// ثبت دستور
const rest = new REST({ version: "10" }).setToken(TOKEN);

(async () => {
  try {
    console.log("⏳ Registering commands...");
    await rest.put(
      Routes.applicationCommands(CLIENT_ID),
      { body: commands }
    );
    console.log("✅ Commands registered");
  } catch (err) {
    console.error(err);
  }
})();

// وقتی ربات روشن شد
client.once("ready", () => {
  console.log(`🤖 Logged in as ${client.user.tag}`);
});

// جواب دستور
client.on("interactionCreate", async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === "ping") {
    await interaction.reply("🏓 Pong! ربات آنلاینه");
  }
});

client.login(TOKEN);
