const express = require('express');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Configuração da porta serial
const port = new SerialPort({ path: '/dev/ttyACM0', baudRate: 9600 });  // Substitua '/dev/ttyUSB0' com o caminho correto da sua porta
const parser = port.pipe(new ReadlineParser({ delimiter: '\n' }));

// Rota para receber os valores dos sliders
app.post('/send-servo-values', (req, res) => {
  const { servoValues } = req.body;  // Receber array [0-100, 0-100, 0-100, 0-100, 0-100]
  
  if (servoValues && servoValues.length === 5) {
    const data = servoValues.join(',') + '\n';  // Formato: '0,50,100,75,25\n'
    port.write(data, (err) => {
      if (err) {
        return res.status(500).send('Erro ao enviar dados para o Arduino');
      }
      res.send('Valores enviados para o Arduino');
    });
  } else {
    res.status(400).send('Array inválido');
  }
});

// Evento quando a porta serial é aberta
port.on('open', () => {
  console.log('Conexão serial aberta');
});

// Evento de erro
port.on('error', (err) => {
  console.error('Erro na comunicação serial: ', err.message);
});

// Iniciar o servidor
app.listen(5000, () => {
  console.log('Servidor rodando na porta 5000');
});
