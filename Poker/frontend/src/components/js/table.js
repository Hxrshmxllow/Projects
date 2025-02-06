import React, {useState, useEffect} from "react";
import "../css/table.css";

function Table() {
    const [playerCard1, setPlayerCard1] = useState("");
    const [playerCard2, setPlayerCard2] = useState("");
    const [aiCard1, setAICard1] = useState("");
    const [aiCard2, setAICard2] = useState("");
    const [pot, setPot] = useState("");
    const [round, setRound] = useState("");
    const [communityCard1, setCommunityCard1] = useState("");
    const [communityCard2, setCommunityCard2] = useState("");
    const [communityCard3, setCommunityCard3] = useState("");
    const [playerMoney, setPlayerMoney] = useState("");
    const [aiMoney, setAIMoney] = useState("");
    const [gameStarted, setGameStarted] = useState(false);
    const [flipped, setFlipped] = useState(false);
    const [aiRaised, setAIRaised] = useState(false);
    const [playerMove, setPlayerMove] = useState("");
    const [amountRaised, setAmountRaised] = useState("");
    const [raised, setRaised] = useState("");
    const [winner, setWinner] = useState("");
    const [aiMove, setAIMove] = useState("");
    const initTable = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000", {
                method: "GET",
            });
            const data = await response.json();
            setPlayerCard1(data["player_card1"]);
            setPlayerCard2(data["player_card2"]);
            setAICard1(data["ai_card1"]);
            setAICard2(data["ai_card2"]);
            setPot(data["pot"]);
            setRound(data["round"]);
            setCommunityCard1(data["community_card1"]);
            setCommunityCard2(data["community_card2"]);
            setCommunityCard3(data["community_card3"]);
            setPlayerMoney(data["player_money"]);
            setAIMoney(data["ai_money"]);
        } catch (error) {
            alert("Error fetching initial game: ", error);
        }
    };
    
    useEffect(() => {
        initTable();
    }, []);

    const rounds = async () => {
        let url = "";
        try {
            let url = ""; 
            if (round === "Pre-Flop") {
                url = "http://127.0.0.1:5000/pre-flop";
            } else if (round === "Flop") {
                url = "http://127.0.0.1:5000/flop";
            } else if (round === "Turn") {
                url = "http://127.0.0.1:5000/turn";
            } else if (round === "River") {
                url = "http://127.0.0.1:5000/river";
            } 
            const response = await fetch(url, {
                method: "GET",
            });
            const data = await response.json();
            setWinner(data["winner"]);
            if (winner) {
                alert("Winner: " + winner);
            }
            setPlayerCard1(data["player_card1"]);
            setPlayerCard2(data["player_card2"]);
            setAICard1(data["ai_card1"]);
            setAICard2(data["ai_card2"]);
            setPot(data["pot"]);
            setRound(data["round"]);
            setCommunityCard1(data["community_card1"]);
            setCommunityCard2(data["community_card2"]);
            setCommunityCard3(data["community_card3"]);
            setPlayerMoney(data["player_money"]);
            setAIMoney(data["ai_money"]);
            setRaised(data["raised"]);
            setAmountRaised(data["amount_raised"]);
            setAIMove(data["aiMove"]);
        } catch (error) {
            alert("Error fetching pre-flop game: ", error);
        }
    };

    useEffect(() => {
        if (round) {
            rounds();
        }
    }, [round]);

    const player_move = async (move, amount) => {
        let url = "";
        try {
            let url = ""; 
            if (round === "Pre-Flop") {
                url = "http://127.0.0.1:5000/pre-flop";
            } else if (round === "Flop") {
                url = "http://127.0.0.1:5000/flop";
            } else if (round === "Turn") {
                url = "http://127.0.0.1:5000/turn";
            } else if (round === "River") {
                url = "http://127.0.0.1:5000/river";
            } 
            if (move === "call" && aiRaised === false){
                move = "check";
            }
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "move": move, "amount": amount }) 
            });
            const data = await response.json();
            setWinner(data["winner"]);
            if (winner && winner !== "null") {
                alert("Winner: " + winner);
            }
            setPlayerCard1(data["player_card1"]);
            setPlayerCard2(data["player_card2"]);
            setAICard1(data["ai_card1"]);
            setAICard2(data["ai_card2"]);
            setPot(data["pot"]);
            setRound(data["round"]);
            setCommunityCard1(data["community_card1"]);
            setCommunityCard2(data["community_card2"]);
            setCommunityCard3(data["community_card3"]);
            setPlayerMoney(data["player_money"]);
            setAIMoney(data["ai_money"]);
            setAIMove(data["aiMove"]);
            if(data["aiRaised"]){
                setAIRaised(true);
            }
        } catch (error) {
            console.error("Error calling API:", error);
            alert("Error calling API. Check console for details.");
        }
    };
    

    return (
        <div className="table-container" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/table.jpg)` }}>
            <div className="community-cards">
            {!gameStarted ? (
                <button className="start-game-button" onClick={() => setGameStarted(true)}>
                    Start Game
                </button>
            ) : (
                <div className="community-cards">
                    <div className="card" 
                        style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${communityCard1})` }}></div>
                    <div className="card" 
                        style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${communityCard2})` }}></div>
                    <div className="card" 
                        style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${communityCard3})` }}></div>
                </div>
            )}
            </div>
            <p className="pot">Pot: ${pot}</p>
            <div className="roundContainer">
                <h1>Round: {round}</h1>
            </div>
            <div className="playerContainer">
                <div className="optionsContainer">
                    <button className="callButton" onClick={() => player_move("call", amountRaised)}>
                        {raised ? "Call" : "Check"}
                    </button>
                    <button className="raiseButton" onClick={() => player_move("raise", 20)}>Raise</button>
                    <button className="foldButton" onClick={() => player_move("fold", 0)}>Fold</button>
                </div>
                <div className="playerCardContainer">
                    <div className="playerCard" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${playerCard1 || "card-back.png"})`}}></div>
                    <div className="playerCard" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${playerCard2 || "card-back.png"})`}}></div>
                </div>
                <p className="playerName">Harshit</p>
                <p className="playerMoney">${playerMoney}</p>
            </div>
            <div className="aiContainer">
                <div className="aiCardContainer">
                    <div className={`aiCard ${flipped ? "flipped" : ""}`} onClick={() => setFlipped(!flipped)}>
                        <div className="card-inner">
                            <div className="card-front" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${aiCard1})` }}></div>
                            <div className="card-back" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/card-back.png)` }}></div>
                        </div>
                    </div>
                    <div className={`aiCard ${flipped ? "flipped" : ""}`} onClick={() => setFlipped(!flipped)}>
                        <div className="card-inner">
                            <div className="card-front" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/${aiCard2})` }}></div>
                            <div className="card-back" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/img/cards/card-back.png)` }}></div>
                        </div>
                    </div>
                </div>
                <p className="aiName">AI</p>
                <p className="aiMoney">${aiMoney}</p>
                <p className="aiMove">{aiMove}</p>
            </div>
        </div>
    );
}

export default Table;

