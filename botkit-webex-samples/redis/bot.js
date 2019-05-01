//
// Copyright (c) 2017 Cisco Systems
// Licensed under the MIT License 
//


// Load env variables 
var env = require('node-env-file');
env(__dirname + '/.env');


//
// BotKit initialization
//

var Botkit = require('botkit');

// Fetch token from environement
// [COMPAT] supports SPARK_TOKEN for backward compatibility
var accessToken = process.env.ACCESS_TOKEN || process.env.SPARK_TOKEN 
if (!accessToken) {
    console.log("Could not start as this bot requires a Webex Teams API access token.");
    console.log("Please invoke with an ACCESS_TOKEN environment variable");
    console.log("Example: ");
    console.log("> ACCESS_TOKEN=XXXXXXXXXXXX PUBLIC_URL=YYYYYYYYYYYYY node bot.js");
    process.exit(1);
}

if (!process.env.PUBLIC_URL) {
    console.log("Could not start as this bot must expose a public endpoint.");
    console.log("Please add env variable PUBLIC_URL on the command line");
    console.log("Example: ");
    console.log("> ACCESS_TOKEN=XXXXXXXXXXXX PUBLIC_URL=YYYYYYYYYYYYY node bot.js");
    process.exit(1);
}

var env = process.env.NODE_ENV || "development";

// Initialize Redis storage
var redisConfig = {
    // for local dev:  redis://127.0.0.1:6379
    // if on heroku :  redis://h:PASSWORD@ec2-54-86-77-126.compute-1.amazonaws.com:60109
    url: process.env.REDIS_URL

    // extra storage to store data for the 'activities' skill
    , methods: ['activities']           

    // uncomment to override default Redis namespace ('botkit:store')
    //, namespace: 'cisco:devnet'         
};
var redisStorage = require('botkit-storage-redis')(redisConfig);

var controller = Botkit.sparkbot({
    log: true,
    public_address: process.env.PUBLIC_URL,
    ciscospark_access_token: accessToken,
    secret: process.env.SECRET, // this is a RECOMMENDED security setting that checks if incoming payloads do originate from Webex
    webhook_name: process.env.WEBHOOK_NAME || ('built with BotKit (' + env + ')'),
    storage: redisStorage
});

var bot = controller.spawn({
});

bot.commons = {};
bot.commons["healthcheck"] = process.env.PUBLIC_URL + "/ping";
bot.commons["up-since"] = new Date(Date.now()).toGMTString();
bot.commons["owner"] = process.env.owner;
bot.commons["support"] = process.env.support;
bot.commons["platform"] = bot.type;
bot.commons["identity"] = "not available"; // the real identity will be available later 
bot.commons["code"] = process.env.code;
bot.commons["version"] = "v" + require("./package.json").version;

// Start Bot API
controller.setupWebserver(process.env.PORT || 3000, function (err, webserver) {
    controller.createWebhookEndpoints(webserver, bot, function () {
        console.log("webhooks setup successfully");
    });

    // installing Healthcheck
    webserver.get('/ping', function (req, res) {
        // The BotCommons metadata need to be built after the bot identity info has been fetched from Webex
        // As we don't have a Bot Initialization Complete event, we'll initialize this value when the bot commons data are fetched
        bot.commons.identity = bot.botkit.identity;
        
        res.json(bot.commons);
    });
    console.log("healthcheck available at: " + bot.commons.healthcheck);
});

// Load skills
var normalizedPath = require("path").join(__dirname, "skills");
require("fs").readdirSync(normalizedPath).forEach(function (file) {
    try {
        require("./skills/" + file)(controller);
        console.log("loaded skill: " + file);
    }
    catch (err) {
        if (err.code == "MODULE_NOT_FOUND") {
            if (file != "utils") {
                console.log("could not load skill: " + file);
            }
        }
    }
});

// Utility to add mentions if Bot is in a 'Group' space
bot.enrichCommand = function (message, command) {
    if ("group" == message.roomType) {
        var botName = bot.botkit.identity.displayName;
        return "`@" + botName + " " + command + "`";
    }
    if (message.original_message) {
        if ("group" == message.original_message.roomType) {
            var botName = bot.botkit.identity.displayName;            
            return "`@" + botName + " " + command + "`";
        }
    }

    return "`" + command + "`";
}
