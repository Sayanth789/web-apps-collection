let firstCard = getRandomCard()
let secondCard = getRandomCard()
let cards = [firstCard, secondCard]
let hasBlackjack = false
let sum = firstCard + secondCard;

let isAlive = true
let message = '';

let messageEl = document.getElementById("message-el");
let sumEl = document.getElementById("sum-el");
let cardsEl = document.getElementById("card-el");
let player = {

     Name: "Sayath", 
     Chips: 123

}



let playerEl = document.getElementById("player-el")
playerEl.textContent = player.Name + ": $" + player.Chips

console.log(message)
console.log(sumEl)

function getRandomCard() {
    let randomCard = Math.floor(Math.random() * 13) + 1;
    if (randomCard > 10 ) {
        return 10
    }
    else if (randomCard === 1) {
        return 11
    } else {
        return randomCard
    }
}

function startGame() {
    renderGame();
    // This will call the renderGame thus we not need to change the name of the functions 
}

function renderGame() {
    cardsEl.textContent = "Cards: "
    for (let i = 0; i < cards.length; i++) {
        cardsEl.textContent += cards[i] + " "
    }
    sumEl.textContent = "Sum: " + sum
    // cardsEl.textContent = "Card: " + cards[0] + " " + cards[1]
    // cardEl.textContent = "Card " + `${firstCard} ` + ` ${secondCard}`
    if (sum < 21) {
        message = "Do you want to draw a new card "
    } else if (sum === 21) {
        message = "Whoooo!!! You have got Blackjack!"
        hasBlackjack = true;

    }
    else  {
        message = "You're out of the game.."
        isAlive = false
    }    
    messageEl.textContent = message;
}

if (hasBlackjack === false && isAlive === true ) {
    newCard()
}
function newCard() {
    if (isAlive && !hasBlackjack) {
        let card = getRandomCard();
        sum += card;
        cards.push(card)
        renderGame()
    }
}
