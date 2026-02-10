import charities from '../data/charities_with_deprivation.json'

function App(){

  const micro = charities.filter(c => c['Charity Size Band'] === 'Micro').length;
  const small = charities.filter(c => c['Charity Size Band'] === "Small").length;
  const medium = charities.filter(c => c['Charity Size Band'] === "Medium").length;

  const validIMDScore = charities.filter(c => c['Index of Multiple Deprivation (IMD) Score'] !== null)
  const averageIMD = validIMDScore.reduce((sum, c) => sum + c.imdScore, 0)

  return(
    <div className='app-layout'>


      <header className='app_header'>
        <h1>Charity Watcher</h1>
      </header>

      {/* Stats Cards*/}
      <div className=''>
        <div className=''>
          <div className=''>Total Charities</div>
          <div className=''>{charities.length}</div>
          <div className=''>{micro} micro -- {small} small -- {medium} medium</div>
        </div>
      </div>

      <p>There are {charities.length} charities on record</p>

      <h2>Tower Hamlets Charities By size:</h2>
      <p>Micro: {micro}</p>
      <p>Small: {small}</p>
      <p>Medium: {medium}</p>

      <p>Average IMD Score in Tower Hamlets {averageIMD}</p>


    </div>
  )

}

export default App