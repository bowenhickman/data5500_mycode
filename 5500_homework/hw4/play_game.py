from DeckOfCards import * # Import everything from DeckOfCards.py (Card, DeckOfCards, etc.)

def format_card(c):# helper function to format how a single card is displayed
    return c.face + " of " + c.suit

def hand_total(cards): # function to compute the total value of a hand with Ace handling
    total = 0 # Start the running total at zero
    aces_count = 0 # Set aces count to zero
    for c in cards:
        total += c.val# Add the card's base value to the total (Ace starts as 11)
        if c.face == "Ace":
            aces_count += 1
    while total > 21 and aces_count > 0:
        total -= 10                              
        aces_count -= 1 # minus 1 the count of Aces counted 11
    return total

def print_deck_block(label, deck): # function to print the whole deck with a label (before/after shuffle)
    print("\n" + label + ":\n")
    deck.print_deck() # Call the deck's built-in print function (prints "Face of Suit, ...") and a line end

def deal_initial(deck):# a function to deal the first two cards to player and dealer
    player = [deck.get_card(), deck.get_card()] # Get two cards from the top of the deck for the player
    dealer = [deck.get_card(), deck.get_card()]  # Get two cards from the top of the deck for the dealer
    return player, dealer

def show_initial_player_cards(player):  # show the player's first two cards
    print("Card number 1 is: " + format_card(player[0]))
    print("Card number 2 is: " + format_card(player[1]))

def player_turn(deck, player): # define the player's turn loop (hit until stop or bust)
    while True:# Start an infinite loop
        choice = input("Would you like a hit?(y/n) ")
        if choice != 'y':
            total = hand_total(player) # Compute the player's current total one last time
            return player, total, False # Return the hand, the total and a flag saying the player did NOT bust
        player.append(deck.get_card())# If they hit, take the next card from the deck and add it to the hand
        print("Card number " + str(len(player)) + " is: " + format_card(player[-1]))  # Show the new card
        total = hand_total(player) # Recompute the new total
        if player[-1].face == "Ace": #new card is an ace
            print("You got an Ace. Your total score is " + str(total)) 
        else:
            print("Your total score is: " + str(total))
        if total > 21:#the new total is over 21
            print("You busted, you lose!")# tell the player that they busted
            return player, total, True # showthe hand, total and a flag saying the player DID bust

def dealer_turn(deck, dealer): #the dealer's turn logic (dealer hits until total >= 17)
    print("\nDealer card number 1 is: " + format_card(dealer[0]))
    print("Dealer card number 2 is: " + format_card(dealer[1]))
    while True:#infinte loop
        total = hand_total(dealer) # Compute the dealer's current total
        if total >= 17:
            return dealer, total, total > 21 # Stop hitting, return hand, total, and busted
        dealer.append(deck.get_card()) # If dealer total is less than 17, take another card
        print("Dealer hits, card number " + str(len(dealer)) + " is: " + format_card(dealer[-1]))  # Show which card the dealer drew

def decide_and_print_result(player_total, dealer_total, dealer_busted): #function for printing outcomes
    if player_total > 21: #player busts
        print("You busted, you lose!")# Print the lose message
        return
    if dealer_busted:
        print("\nDealer score is: " + str(dealer_total))  # Show the dealer's final score
        print("\nDealer Busted, you win!!!")# Print the win message for a dealer bust
        return
    print("\nDealer score is: " + str(dealer_total))# If no one busted, print the dealer's final score
    if player_total > dealer_total:
        print("\nYour score is higher, you win!")# Print the win message for a higher player score
    else:
        print("\nDealer score is higher or equal, you lose!")  # Print the lose message

def main():#main fucntion to run game loop
    print("Welcome to Black Jack!")
    deck = DeckOfCards()# Create a new DeckOfCards object
    while True: #same deck of cards for multiple rounds                      
        print_deck_block("deck before shuffled", deck) # Print the entire deck before shuffling
        deck.shuffle_deck() # Shuffle the deck
        print_deck_block("deck after shuffled", deck) # Print the deck after shuffling
        player, dealer = deal_initial(deck) # Deal two cards to the player and two to the dealer
        show_initial_player_cards(player)# Show the player's first two cards
        initial_total = hand_total(player) # count the player's starting total with Ace adjustments
        print("Your total score is: " + str(initial_total))
        player, p_total, p_busted = player_turn(deck, player) #players turn until stand or bust
        if not p_busted:
            dealer, d_total, d_busted = dealer_turn(deck, dealer) # Run the dealer's turn (hit until >= 17)
            decide_and_print_result(p_total, d_total, d_busted) # Print who won and why
        again = input("\nanother game?(y/n): ").strip().lower() # Ask if the player wants to play another round
        if again != 'y':
            break

if __name__ == "__main__":
    main()