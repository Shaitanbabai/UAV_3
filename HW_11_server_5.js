// npm init -y
// npm install express jsonwebtoken
// node название_сервер.js

const express = require('express');
const jwt = require('jsonwebtoken');

const app = express();
const port = 4000;
const SECRET_KEY = 'my_unique_secret';

app.use(express.json());

let globalToken = null;

// Создание уникального токена
app.post('/create-token', (req, res) => {
  globalToken = jwt.sign({ user: 'unique_user' }, SECRET_KEY);
  res.json({ token: globalToken });
});

// Middleware для проверки токена
function validateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (token === globalToken) {
    next();
  } else {
    res.sendStatus(403);
  }
}

// Уникальный маршрут
app.get('/welcome', validateToken, (req, res) => {
  res.send('Greetings from Unique API!');
});

// Уникальная команда
app.post('/command', validateToken, (req, res) => {
  const { instruction } = req.body;
  res.send(`Executed command: ${instruction}`);
});

app.listen(port, () => {
  console.log(`Unique API server running at http://localhost:${port}`);
});
