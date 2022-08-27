const Page = ({page}) => (
    <li>
        <a href={"https://fr.wikipedia.org/wiki/" + page.title} target="_blank">
            {page.title}
        </a> {page.count !== undefined && <span className="is-size-7">({page.count} vues hier)</span>}
    </li>
)
const App = () => {
    const [data, setData] = React.useState()
    const [showAnswer, setShowAnswer] = React.useState(false)
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
    const refresh = () => {
        setShowAnswer(false)
        let url = "/api/easy"
        if (params.hard)
            url = "/api/hard"
        fetch(url).then(e => e.json()).then(e => {
            console.log(e)
            setData(e)
        })
    }
    React.useEffect(refresh, [])
    return (
        <div className="main">
            <section className="section">
                <div className="container">
                    <h1 className="title">
                        Wiki Guess
                    </h1>

                    <div className="columns">
                        <div className="column">
                            <h2 className="subtitle">
                                Pages contenant un lien vers la page
                            </h2>
                            <ul>
                                {data && data.backlinks.map(page => <Page key={page.title} page={page} />)}
                            </ul>
                        </div>

                        <div className="column">
                            <h2 className="subtitle">
                                Choix
                            </h2>
                            <ol>
                                {data && data.randomPages.map(page => <Page key={page.title} page={page} />)}
                            </ol>

                        </div>
                        <div className="column">
                            {!showAnswer
                                ?
                                <button className="button is-info" onClick={e => setShowAnswer(true)}>
                                    Montrer la réponse
                                </button>
                                :
                                <div>
                                    <h2 className="subtitle">
                                        Réponse
                                    </h2>
                                    <ul><Page page={data.randomPage} /></ul>
                                    <button className="button mt-5 is-primary" onClick={e => refresh()}>
                                        Recommencer
                                    </button>
                                </div>
                            }
                        </div>
                    </div>

                </div>
            </section>

            <footer class="footer">
              <div class="content has-text-centered">
                <p>
                  <a href="/">Mode normal</a> - <a href="/?hard=true">Mode difficile</a>
                </p>
              </div>
            </footer>
        </div>
    )
}

const domContainer = document.getElementById('root');
ReactDOM.render(<App />, domContainer);
