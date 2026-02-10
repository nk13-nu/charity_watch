import charities from '../data/charities_with_deprivation.json'

function App(){

  const micro = charities.filter(c => c['Charity Size Band'] === 'Micro').length;
  const small = charities.filter(c => c['Charity Size Band'] === "Small").length;
  const medium = charities.filter(c => c['Charity Size Band'] === "Medium").length;

  return(
    <div style={{ padding: '40px' }}>
      <h1>Charity Watcher</h1>
      <p>There are {charities.length} charities on record</p>

      <h2>Tower Hamlets Charities By size:</h2>
      <p>Micro: {micro}</p>
      <p>Small: {small}</p>
      <p>Medium: {medium}</p>
    </div>
  )

}

export default App