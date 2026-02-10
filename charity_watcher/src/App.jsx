import charities from '../data/charities_with_deprivation.json'

function App(){

  const micro = charities.filter(c => c['Charity Size Band'] === 'Micro').length;
  const small = charities.filter(c => c['Charity Size Band'] === "Small").length;
  const medium = charities.filter(c => c['Charity Size Band'] === "Medium").length;

  const validIMDScore = charities.filter(c => c['Index of Multiple Deprivation (IMD) Score'] !== null)
  const averageIMD = validIMDScore.reduce((sum, c) => sum + c.imdScore, 0)

  const uniqueLSOAs = new Set(charities.map(c => c['LSOA code (2021)'])).size

  return(
    <div className='app-layout'>

      <header className='app-header'>
        <h1>Charity Watcher</h1>
      </header>

      {/* Side Bar */}
      <aside className='app-sidebar'>
      </aside>

      <main className='app-main'>
        
        {/* Stats Cards*/}
        <div className='stats-row'>
          <div className='stats-card'>
            <div className='stats-card-title'>Total Charities</div>
            <div className='stats-card-value'>{charities.length}</div>
            <div className='stats-card-text'>{micro} micro -- {small} small -- {medium} medium</div>
          </div>

          <div className='stats-card'>
            <div className='stats-card-title'>Total Income</div>
            <div className='stats-card-value'>{charities.length}</div> 
            <div className='stats-card-text'>{micro} micro -- {small} small -- {medium} medium</div>
          </div>

          <div className='stats-card'>
            <div className='stats-card-title'>Average IMD Score</div>
            <div className='stats-card-value'>{averageIMD}</div>
            <div className='stats-card-text'>{micro} micro -- {small} small -- {medium} medium</div>
          </div>

          <div className='stats-card'>
            <div className='stats-card-title'>LSOA Coverage</div>
            <div className='stats-card-value'>{uniqueLSOAs} Lower Layer Output Areas</div>
            <div className='stats-card-text'>{micro} micro -- {small} small -- {medium} medium</div>
          </div>
        </div>

        {/*Map Card*/}
        <div className="map-content-row">
          <div className="map-card">Map here</div>
        </div>

        {/*Chart Cards*/}
        <div className="chart-content-row">
          <div className="chart-card">Bubble chart goes here</div>
          <div className="chart-card">IMD Chart here</div>
          <div className="chart-card">size band donun here</div>
        </div>


      </main>


    </div>
  )

}

export default App