import "../styles/Trades.css"

export default function Trades() {
  return <div className="Trades">
    <h1>Recent Trades</h1>
    {Trade("069", "420", 200, 24900000, true)}
    {Trade("069", "420", 1900, 24910000, false)}
    {Trade("069", "420", 4000, 24950000, true)}
  </div>;
}

function splitPrice(price) {
  let priceStr = price.toString();
  return [priceStr.substring(0, priceStr.length-6), priceStr.substring(priceStr.length-6)];
}

function Trade(broker, contraBroker, shareCount, pricePerShare, isBuy) {
  let [totalFull, totalDecimal] = splitPrice(shareCount * pricePerShare);
  let [perShareFull, perShareDecimal] = splitPrice(pricePerShare)

  return <article className="Trade" buy={isBuy ? "true" : ""}>
    <div className="price">
      <span className="primaryPrice">${totalFull}.<span className="currencyDecimal">{totalDecimal}</span></span>
      <span className="secondaryPrice">({isBuy ? "bought" : "sold"} {shareCount} @ ${perShareFull}.<span className="currencyDecimal">{perShareDecimal}</span>)</span>
    </div>
    <div>{broker} {isBuy ? "→" : "←"} {contraBroker}</div>
  </article>
}
