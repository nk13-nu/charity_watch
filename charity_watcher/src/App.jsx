import charities from '../data/charities_with_deprivation.json'

function App(){

  const micro = charities.filter(c => c['Size Band'] === 'Micro').length;
  const small;
  const medium;
}

export default App