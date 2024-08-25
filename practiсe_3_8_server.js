const express = require('express');
const arDrone = require("ar-drone");

const app = express();

const drone1 = arDrone.createClient(); // 192.168.1.1
const drone2 = arDrone.createClient({ip: '192.168.1.2'});

drone1.on("navdata", (data) => {
    console.log('Данные от дрона 1:', data);
});

app.get('/time', (req, res) => {
    console.log("Клиент запросил время")
    const currentTime = new Date();
    res.json({time: currentTime});
});

app.get('/:droneId/takeoff', (req, res) => {
    console.log(`Запрос на взлет Дрон ${droneId} `)
    drone1.takeoff();
    const droneId = req.params.droneId;
    res.json({status: `Дрон ${droneId} взлетел`});

});

const PORT = 3000;

app.listen(PORT, () => {
    console.log("Сервер запущен!")
})