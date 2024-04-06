import "../styles/Rankings.css"

const BROKER_NAME = {
    1: "Anonymous",
    2: "RBC Capital Markets",
    7: "TD Securities Inc.",
    9: "BMO Nesbitt Burns Inc.",
   14: "Virtu Canada Corp.",
   19: "Desjardins Securities Inc.",
   33: "Canaccord Genuity Corp.",
   39: "Merrill Lynch Canada Inc.",
   53: "Morgan Stanley Canada Ltd.",
   65: "Goldman Sachs Canada Inc.",
   70: "Manulife Securities Incorporated",
   72: "Credit Suisse Securities (Canada), Inc.",
   79: "CIBC World Markets Inc.",
   80: "National Bank Financial Inc.",
   84: "Independent Trading Group (ITG) Inc.",
   85: "Scotia Capital Inc.",
   88: "Aviso Financial Inc.",
  124: "Questrade Inc."
}

export default function Rankings() {
  return <div className="Rankings">
    <div className="Header">
      <h1>Rankings</h1>
      <select type="" id="RankingKey">
        <option selected>pineapple</option>
        <option>pizza</option>
      </select>
    </div>
    <div className="RankingHolder">
      {Ranking(79, 1.532)}
      {Ranking(85, 1.343)}
      {Ranking(124, 1.210)}
      {Ranking(2, 0.939)}
      {Ranking(7, -0.134)}
      {Ranking(9, -0.453)}
      {Ranking(14, -1.249)}
    </div>
  </div>;
}

function Ranking(brokerID, score) {
  return <div className="Ranking">
    <div className="Broker"><span className="BrokerID">({brokerID.toString().padStart(3, '0')})</span> {BROKER_NAME[brokerID]}</div>
    {score}
  </div>
}
