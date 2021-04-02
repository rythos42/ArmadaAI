# ArmadaAI
Attempts at a computer-based AI for table-top wargame Star Wars Armada.

# Project Goals
- "Good enough". Only needs to automate some decisions, not all. Enough that I can convince myself I'm not playing a solitaire game.- 
- Only needs to manage *movement* at this time, other decisions are beyond what I think is needed.
- Minimal maintenance - better if all data can be loaded from VASSAL file format vmod or vsav

# Todo
- How to connect to VASSAL?
	- What is the VASSAL file format? How does it describe ship positions?
	- Load a vassal file
	- Read the ship positions
	- Place those positions onto the table
	- (make the table virtual)
	- Make a move decision
	- Write the move decision back to the VASSAL file
	- Is there a way to get VASSAL to load files when they change?
- move ships to start at a "post-opening book" position?
	- currently will take ~33 days to analyze first move, which isn't useful.
	- But at least it *does it*!
- interface to allow player to turn
- change evaluation to prefer moves that give a double arc
- initial positioning of AI ships
	- random?
	- hard flank?
	- grouped?
- update win conditions:
    - better if you can double-arc
    - good if you can get to the range the ship wants to be at
    - good if you can stay beyond the ranges the opponent wants to be at
- ensure it can go beyond the beginning moves (ie, past a ship)
- enable ships to go speed 4
- "opening book" to automate early moves based on fleet characteristics
- "finishing book" to automate turn in/turn out decision
- add more ships and stats
 - add metadata around what kind of types want what range
	- update evaluation to use that
	- prefer if we don't have to maintain ship metadata in future - can this information be read from ship image cards?

# Tech Debt / Far Future
- arcs and ship scaling may not be the same as map because it's scaled seperately
- pylint disabled because it's a minor pain to appease
- allow AI to turn out?
- allow AI to do inside turns?
- Can't currently go speed 0, is this valuable/important?

# Useful Code and Links
- Draw polygons associated with a mask

        olist = first_player_ship.black_mask.outline()
        pygame.draw.polygon(screen, (200, 150, 150), olist, 0)
        
- Armada Robot        https://boardgamegeek.com/filepage/188857/eds-armada-robot-player
 - Pygame Tutorial     https://realpython.com/pygame-a-primer/#sprites
 - Minmax+ABpruning    https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/


# Game Measurements
Map files from VASSAL are 4320x2160px
Small base ships 43 mm x 71 mm.
Medium base ships 63* mm x 102 mm, 149px x 243px in VASSAL
Large base ships 77.5 mm x 129 mm.

## Distances
1. 3" (77mm)
2. 4 15/16" (125mm)
3. 7 5/16" (185mm)
4. 9 7/16" (245mm)
5. 1 foot

## Ranges
- Close: 4 7/8" (124mm)
- Medium: 7 3/8" (188mm)
- Long: 1 foot

# Notable Milestones 
## v0.2
- Added graphics, Munificent ships, arcs
- Added ships able to move straight line distances equivalent to table top
- Updated game rules to win if you start your turn within black range of opponent

## v0.1
- Ships start at points on number line, 1-10
- Each ship can move 1, 2 or 3
- AI takes first turn
- Game ends if ships are touching or overlapping
- Game is won if you start your turn touching the opponent