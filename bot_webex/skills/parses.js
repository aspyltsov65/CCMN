var axios = require('axios');
var fs = require("fs");
const { createCanvas, loadImage } = require('canvas')
const canvas = createCanvas(1550, 770)
const ctx = canvas.getContext('2d')

module.exports = function (controller) {

    controller.hears(['find'], 'direct_message,direct_mention', function (bot, message) {

        bot.startConversation(message, function (err, convo) {
            convo.ask('Enter xlogin or device MAC that you want to find(MAC format: 00:ab:cd:ef:11:22)', function (response, convo)
            {
                process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
                let answer = response.text;
                axios.get('https://cisco-cmx.unit.ua/api/location/v2/clients', {
                                        auth: {
                                            username: 'RO',
                                            password: 'just4reading'}})
                    .then(function (response) {
                        let i = 0;
                        while (response.data[i])
                        {
                            let v = Object.values(response.data[i]);
                            if (v[12] && (v[0] == answer || v[13] == answer))
                            {
                                var img = '../Perks/e1.png';
                                let image_sw = Object.values(v[1]);
                                switch (image_sw[0]){
                                    case 'System Campus>UNIT.Factory>2nd_Floor>Coverage Area_2nd_Floor':
                                        img = '../Perks/e2.png';
                                        break;
                                    case 'System Campus>UNIT.Factory>3rd_Floor>Coverage Area-3rd_Floor':
                                        img = '../Perks/e3.png';
                                        break;
                                }
                                loadImage(img).then((image) => {
                                    ctx.drawImage(image, 0, 0, 1550, 770);
                                    ctx.fillStyle = "#ff0000";
                                    ctx.beginPath();
                                    ctx.arc(v[2].x, v[2].y, 10, 0, 2 * Math.PI);
                                    ctx.fill();
                                    var buf = canvas.toBuffer();
                                    fs.writeFileSync("location.png", buf);
                                    bot.reply(message, {
                                        text: 'Here is the map with red dot, where ' + answer + ' located.',
                                        files: [fs.createReadStream('./location.png')]
                                    })
                                });
                                break
                            }
                            i++;
                        }
                        if (!response.data[i])
                            convo.say(answer + " not connected(")
                        // var rs = Object.values(response.data)
                        // rs = Object.values(rs[2][0])
                        // while (response.data[i])
                        // {
                        //
                        // }
                        // loadImage('../../Perks/e1.png').then((image) => {
                        //     ctx.drawImage(image, 0, 0, 1550, 770);
                        //     ctx.fillStyle = "#ff0000";
                        //     ctx.beginPath();
                        //     ctx.arc(rs[2].x, rs[2].y, 10, 0, 2 * Math.PI);
                        //     ctx.fill();
                        //     var buf = canvas.toBuffer();
                        //     fs.writeFileSync("location.png", buf);
                        //     bot.reply(message, {text: 'Here is the map with red dot, where ' + rs[0] + ' located.' ,files:[fs.createReadStream('./location.png')]})
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                convo.next();
            });
        });
    });
};