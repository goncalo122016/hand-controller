import './App.css'
import { useState, useEffect } from 'react'
import { Slider } from './components/ui/slider'
import b1 from './img/fundo1.jpg'
import b2 from './img/fundo2.jpg'
import b3 from './img/fundo3.jpg'
import b4 from './img/fundo4.jpg'
import b5 from './img/fundo5.jpg'

function App() {
  const [sliderValues, setSliderValues] = useState([0, 0, 0, 0, 0])
  const [backgroundImage, setBackgroundImage] = useState(b1)
  const [toggleStates, setToggleStates] = useState([false, false, false, false, false])

  // Atualiza os valores do slider
  const handleSliderChange = (index: number, newValue: number) => {
    const newValues = [...sliderValues]
    newValues[index] = newValue
    setSliderValues(newValues)
  }

  // Alterna os botões entre 0 e 100
  const handleToggleChange = (index: number) => {
    const newToggleStates = [...toggleStates]
    newToggleStates[index] = !newToggleStates[index]
    setToggleStates(newToggleStates)

    const newSliderValue = newToggleStates[index] ? 100 : 0
    handleSliderChange(index, newSliderValue)
  }

  // Altera o fundo da tela
  const handleBackgroundChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedBackground = event.target.value
    switch (selectedBackground) {
      case 'b1': setBackgroundImage(b1); break
      case 'b2': setBackgroundImage(b2); break
      case 'b3': setBackgroundImage(b3); break
      case 'b4': setBackgroundImage(b4); break
      case 'b5': setBackgroundImage(b5); break
      default: setBackgroundImage(b1)
    }
  }

  // Função para enviar os valores dos sliders para o Arduino via backend
  const sendServoValues = async (values: number[]) => {
    try {
      const response = await fetch('http://localhost:5000/send-servo-values', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ servoValues: values }),
      })
      const data = await response.text()
    } catch (error) {
      console.error('Erro ao enviar os dados:', error)
    }
  }

  // Atualiza os valores a cada 1 segundo
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('Enviando valores:', sliderValues)
      sendServoValues(sliderValues)
    }, 1000)

    return () => clearInterval(interval) // Limpa o intervalo ao desmontar
  }, [sliderValues]) // Executa sempre que `sliderValues` mudar

  return (
    <div 
      className="w-full h-screen bg-cover bg-center flex flex-col items-center justify-center relative overflow-hidden"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <div className="absolute top-10 right-10 z-20">
        <select className="p-2 bg-gray rounded-lg" onChange={handleBackgroundChange}>
          <option value="b1">Background 1</option>
          <option value="b2">Background 2</option>
          <option value="b3">Background 3</option>
          <option value="b4">Background 4</option>
          <option value="b5">Background 5</option>
        </select>
      </div>

      <div className="absolute w-1/2 p-10 bg-gunmetal rounded-lg z-10 items-center flex flex-col justify-center">
        <div className="text-4xl font-bold text-gray mb-10 z-10">Bionic Hand Control</div>

        <div className="flex gap-24">
          {sliderValues.map((value, index) => (
            <div key={index} className="flex flex-col items-center">
              <Slider
                value={[value]}
                onValueChange={(newValue) => handleSliderChange(index, newValue[0])}
                orientation="vertical"
                className="h-64 w-4 bg-red rounded-lg shadow-xl transition-all duration-300 hover:bg-red-light"
                max={100}
              />
              <div className="text-white mt-4 text-lg">{value}%</div>

              <button
                onClick={() => handleToggleChange(index)}
                className={`mt-4 px-4 py-2 rounded-full transition-all duration-300 ${
                  toggleStates[index] ? 'bg-red text-white' : 'bg-darkgray text-gunmetal'
                }`}
              >
                {toggleStates[index] ? 'Close' : 'Open'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
