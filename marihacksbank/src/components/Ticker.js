import "../styles/Ticker.css"

function randomStock() {
  let value = Math.round((Math.random()*100 + 20) * 100);
  let valueStr = value.toString();

  let up = Math.random() > .5;
  return <div up={up ? "true" : ""}>{valueStr.substring(0, valueStr.length-2)}.{valueStr.substring(valueStr.length-2)} {up ? "▲" : "▼"}</div>
}

export default function RankingHistory() {
  return <div className="Ticker">
    <div className="TickerElementHolder">
      {[...Array(100)].map(randomStock)}
    </div>
  </div>;
}