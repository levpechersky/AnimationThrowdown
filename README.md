# AnimationThrowdown helper

This is a command-line utility intended to help Animation Throwdown players

- discover powerful combos you may have missed out.

- see which siege island suits you best

- find out which cards of yours are the most powerful

- check which combos are the strongest: 
    - in general 
    - for each card alone
    - for some skill you like the most

Currently this utility only shows various useful statistics for your active deck and all your cards. 
In future I plan to make it able to generate decks based on requested criteria 
(for example, deck with the strongest Punch, deck with the most American Dad cards, the most Drunk trait, most Clash combos, and such)


##### What is special about this tool? 

- Works with your deck: takes into account cards levels, combo mastery, duplicate cards -
for both regular cards and combos. Health, Attack, Skills - everything will be exactly as you see in-game.

- Adjust the tool to your playing strategy: define how much each skill is worth to you,
and see how each card fits with your game style

### Requirements

Requires Python 3

For windows, download from https://www.python.org/downloads/windows/

### Usage

#### Describe your cards

Edit [deck.cards](deck.cards) and write down which cards do you have in your current deck.


Edit [sidedeck.cards](sidedeck.cards) and put there the rest of your cards (not including the active deck).

Both files are regular text files, you can use Notepad or something similar. Cards format is pretty simple:
```
L 6** Buck's Stud
```
- Rarity, only the first letter (C - Common, R - Rare, E - Epic, and so on)
- Level, as shown in game (e.g. 1*, 4, 6**)
- Name (exactly as in game, case-sensitive)

Empty and whitespace lines are ignored, comment lines start with `# `.

Order of cards doesn't matter.

If you have, say, 2 copies of a card - write it down twice.

#### Describe which combos you have mastered

Edit [combo.mastery](combo.mastery) and write down which mastery levels and combo names, as following:
```
2 Burgerboss Bob
```
- Mastery level
- Combo name (case-sensitive)

Empty and whitespace lines are ignored, comment lines start with `# `.

#### Weights setting - for more advanced customization (optional)
This is the point, where you can adjust this tool to your game strategy.
Everyone says Crazed is the best, but you prefer Punch, or maybe Gas?

I use 'weights' - a symbolic cost for each skill, Health and Attack, to indicate the importance of that skill.
It looks like this:
```
W_HP = 28
W_ATTACK = 100
W_SKILL = {
	'Cripple All': 185,
	'Shield All': 180,
	'Heal All': 171,
	'Motivate': 150,
	'Cheer All': 140,
	'Bomb': 135,
	'Punch': 125,
	'Crazed': 120,
	'Heal': 108,
	'Gas': 73,
	'Burn': 70,
	'Enlarge': 70,
	'Bodyguard': 66,
	'Boost': 66,
	'Sturdy': 64,
	'Cripple': 61,
	'Recover': 60,
	'Payback': 58,
	'Shield': 57,
	'Hijack': 50,
	'Cheer': 44,
	'Leech': 40,
	'Jab': 39,
	'Give': 37,
}
```
The Higher - the better.
Numerical values don't matter much, what's more important is the ratios between them.


##### Semi-automatic interactive way
This is very boring, but usually gives the best results.

Run `weights_gen.py` and follow instructions.
The script will ask you several question, like in following example.

1. How much a particular skill is worth to you, compared to Attack? In the example I say that 13 Attack points are
probably worth 16 Boost points.
2. After your answer, the script gives you kind of a preview of 2 cards (the numbers are Attack/HP),
 to check your answer, and let you change it if necessary. In the example I noticed, that the card with Attack bonus looks stronger.
3. If you choose 1 or 2 (one of proposed cards looks stronger) - you can enter a new cost, and get an updated preview.
I changed my answer to 18.
4. When you think that both cards are nearly equal in strength - choose 0, and the script will proceed to the next skill.

```
For how much Boost(+ attack on combo) would you trade Attack(13)?
Enter 0 to try with new random Attack value.
> 16
Let's check. Which is stronger?
 0: both are equal, proceed to next skill
 1: 21/27 card
 2:  8/27 card with Boost(16) (+ attack on combo)
> 1
Increase value, try 25
For how much Boost(+ attack on combo) would you trade Attack(13)?
Enter 0 to try with new random Attack value.
> 18
Let's check. Which is stronger?
 0: both are equal, proceed to next skill
 1: 27/24 card
 2: 14/24 card with Boost(18) (+ attack on combo)
> 0
Set weight Boost=72
==================================================
For how much Give would you trade Attack(1)?
Enter 0 to try with new random Attack value.

```

In the end, the script will generate a new Python file `weights_user.py` with resulting weights, based on your answers.

You may want to adjust the resulting weights a bit - you can edit `weights_user.py` afterwards.
You may also delete it to use the default weights.

##### Manual way
This way is faster, but also need some thought, and requires some Python knowledge (very basic).

Edit Skill Weights in [weights.py](weights.py)

#### The report

When weights are ready (or if you skipped weights setting), run `main.py` - it will read your cards and mastery data,
and generate `report.txt` with your cards statistics.

##### Report format
Example: Legendary Brian with 7 Attack and 33 HP, and computed power (based on weights, see above) of 2491

```Legendary   7/33[ 2491] Brian```


##### Examples

Traits and animated series - choose your siege Island:
```
>> Cards count by series:
 Bobs Burgers    : 21
 Family Guy      : 18
 American Dad    : 15
 Futurama        : 14
 King Of The Hill: 8
Detailed:
	Bobs Burgers
		Epic        9/24[ 2688] Bob                          HERO   Bobs Burgers     Heal(7) Crazed(3)
		Epic        9/24[ 2688] Bob                          HERO   Bobs Burgers     Heal(7) Crazed(3)
		Epic        5/26[ 2408] Louise                       HERO   Bobs Burgers     Punch(4) Leech(5) Crazed(4)
		Epic        5/26[ 2408] Louise                       HERO   Bobs Burgers     Punch(4) Leech(5) Crazed(4)
		Legendary   8/27[ 2060] Tina                         HERO   Bobs Burgers     Boost(4) Leech(6)
		Legendary  11/33[ 2920] Tina                         HERO   Bobs Burgers     Boost(6) Leech(8) Shield All(2-Bobs Burgers)
```

```
>> Cards count by trait:
 none            : 14
 animal          : 10
 athletic        : 9
 fighter         : 8
 disguised       : 7
 addicted        : 5
 musical         : 5
 artistic        : 5
 educated        : 4
 armed           : 4
 drunk           : 3
 rich            : 2
Detailed:
	animal
		Legendary   7/33[ 2491] Brian                        HERO   Family Guy       Bodyguard(2) Boost(5) Bomb(3)
		Legendary   2/36[ 1847] Klaus Heisler                HERO   American Dad     Recover(4) Shield All(2-American Dad) Gas(3)
		Legendary  15/46[ 4592] Buck's Stud                  OBJECT King Of The Hill Heal(13) Hijack(8)
		Legendary  16/27[ 3652] Iraq Lobster                 OBJECT Family Guy       Motivate(4) Sturdy(6) Jab(8)
		Legendary  14/21[ 2889] Iraq Lobster                 OBJECT Family Guy       Motivate(3) Sturdy(4) Jab(5)
```

___

Individual card score (only cards HP, Attack and skills - not considering combos).

1st column - combo potential score (see below)
```
>> Individual card score:
 118578 Legendary  15/46[ 4592] Buck's Stud                  OBJECT King Of The Hill Heal(13) Hijack(8)
  75045 Legendary  13/47[ 4303] Pantry Guns                  OBJECT American Dad     Bodyguard(8) Jab(11) Gas(10)
 362287 Legendary  11/45[ 4097] Peter                        HERO   Family Guy       Sturdy(8) Bomb(7) Cheer All(4-Family Guy)
 105320 Legendary  10/47[ 3806] Jacked on Bots               OBJECT Futurama         Bodyguard(5) Sturdy(5) Crazed(7)
  78439 Legendary  10/45[ 3797] Big Boy Karate               OBJECT Futurama         Motivate(5) Shield All(4-fighter) Cripple(7)
 285818 Legendary  14/38[ 3680] Bender                       HERO   Futurama         Sturdy(8) Payback(8) Leech(6)
  97198 Legendary  16/27[ 3652] Iraq Lobster                 OBJECT Family Guy       Motivate(4) Sturdy(6) Jab(8)
 109666 Legendary  13/38[ 3584] K Pop Video                  OBJECT Family Guy       Cheer(10-musical) Motivate(8-musical) Leech(10)
  88294 Legendary  13/25[ 3440] Quahog Martial Arts Academy  OBJECT Family Guy       Motivate(6) Bodyguard(5) Cheer All(3-Family Guy)
```

___

Combo potential score - sum of individual scores of all possible combos with that card.

Only combos with cards you have are taken into account.

1st column - combo potential score, in brackets - individual score.
```
>> Combo potential score:
 362287 Legendary  11/45[ 4097] Peter                        HERO   Family Guy       Sturdy(8) Bomb(7) Cheer All(4-Family Guy)
 321209 Legendary  11/33[ 2920] Tina                         HERO   Bobs Burgers     Boost(6) Leech(8) Shield All(2-Bobs Burgers)
 317535 Legendary   8/38[ 2784] Stewie                       HERO   Family Guy       Shield All(1) Punch(4) Leech(6)
 311656 Legendary   9/34[ 2751] Peggy                        HERO   King Of The Hill Payback(5) Heal All(1) Gas(6)
 285818 Legendary  14/38[ 3680] Bender                       HERO   Futurama         Sturdy(8) Payback(8) Leech(6)
 281424 Legendary   8/36[ 3266] Bobby                        HERO   King Of The Hill Payback(6) Punch(6) Crazed(3)
```

___

Combined score (1st column): weighted average of individual and combo potential score.

Top 13 heroes plus top 13 objects from this list would make a strong deck.

You can adjust those weights in [weights.py](weights.py): see `SINGLE_CARD_SCORE_WEIGHT` and `COMBOS_SCORE_WEIGHT`
```
>> Combined score:
  12119 Legendary  11/45[ 4097] Peter                        HERO   Family Guy       Sturdy(8) Bomb(7) Cheer All(4-Family Guy)
  10317 Legendary  11/33[ 2920] Tina                         HERO   Bobs Burgers     Boost(6) Leech(8) Shield All(2-Bobs Burgers)
  10138 Legendary   8/38[ 2784] Stewie                       HERO   Family Guy       Shield All(1) Punch(4) Leech(6)
   9961 Legendary   9/34[ 2751] Peggy                        HERO   King Of The Hill Payback(5) Heal All(1) Gas(6)
   9829 Legendary  14/38[ 3680] Bender                       HERO   Futurama         Sturdy(8) Payback(8) Leech(6)
   9464 Legendary   8/36[ 3266] Bobby                        HERO   King Of The Hill Payback(6) Punch(6) Crazed(3)
   9074 Legendary  13/38[ 3249] Dr. Amy Wong                 HERO   Futurama         Cripple All(3) Bodyguard(5)
```

___

Strongest combos. Maybe there's a top-grade combo you have not researched yet?

```
>> Strongest combos:
Chicken Fight                17/63[ 9774] Motivate(11) Punch(20) Bomb(16)                                                Legendary 6** Peter + Legendary 6* Big Boy Karate
Pointillism                  13/65[ 9204] Punch(18) Bomb(14) Heal(18)                                                    Legendary 6 Stewie + Legendary 6** Napkin Art
Chicken Fight                20/49[ 9137] Motivate(10) Punch(19) Bomb(14)                                                Legendary 6** Peter + Legendary 6* Quahog Martial Arts Academy
Chicken Fight                17/53[ 8824] Motivate(10) Punch(18) Bomb(14)                                                Legendary 6** Peter + Legendary 6 Fashion Wrestling
Chicken Fight                16/56[ 8808] Motivate(10) Punch(18) Bomb(14)                                                Legendary 6** Peter + Legendary 6 Goth Dance Fighting
Line Dancer Amy              20/58[ 8646] Jab(18) Motivate(18) Bomb(12)                                                  Legendary 6* Dr. Amy Wong + Legendary 6** K Pop Video
Pointillism                  12/61[ 8624] Punch(17) Bomb(13) Heal(17)                                                    Legendary 6 Brian + Legendary 6** Napkin Art
```

Strongest combos for each card. Nice to check in the middle of a fight, to decide on your next move.

```
>> Strongest combos per card:
Legendary 6** Peter:
	   9774 with Legendary 6* Big Boy Karate             : Chicken Fight                17/63[ 9774] Motivate(11) Punch(20) Bomb(16)
	   9137 with Legendary 6* Quahog Martial Arts Academy: Chicken Fight                20/49[ 9137] Motivate(10) Punch(19) Bomb(14)
	   8824 with Legendary 6 Fashion Wrestling           : Chicken Fight                17/53[ 8824] Motivate(10) Punch(18) Bomb(14)
	   7803 with Legendary 6 Mr. Fischoeder              : Lord Griffin                 16/55[ 7803] Crazed(12) Heal(17) Gas(19)
	   7791 with Legendary 6** K Pop Video               : K Pop Peter                  19/62[ 7791] Shield All(10-musical) Punch(19) Leech(22)
	   7239 with Legendary 6 Sacred Daggers              : Pirate Cannon Peter          17/53[ 7239] Crazed(11) Cheer All(7) Bomb(13)
Legendary 6* Big Boy Karate:
	   9774 with Legendary 6** Peter                     : Chicken Fight                17/63[ 9774] Motivate(11) Punch(20) Bomb(16)
	   7440 with Legendary 6 Stewie                      : Karate Stewie                13/63[ 7440] Crazed(11) Punch(16) Boost(16)
	   6974 with Legendary 6 Peggy                       : Class Spanker                14/60[ 6974] Hijack(12) Punch(18) Payback(18)
	   6747 with Legendary 6 Klaus Heisler               : Smoke Bomb                    9/63[ 6747] Gas(16) Bomb(12) Cripple All(7)
```

Combos with the strongest skills. Make a deck with the strongest Punch!
```
>> Strongest combos for each skill:
	[Motivate]
		Bender's Ducklings           22/66[ 8317] Heal(26-animal) Motivate(19-animal) Crazed(12)             | Legendary 6** Bender + Legendary 6** Buck's Stud
		Line Dancer Amy              20/58[ 8646] Jab(18) Motivate(18) Bomb(12)                              | Legendary 6* Dr. Amy Wong + Legendary 6** K Pop Video
		Line Dancer Amy              16/62[ 8034] Jab(17) Motivate(17) Bomb(11)                              | Legendary 6* Dr. Amy Wong + Legendary 6 4 Skore
		Line Dancer Amy              18/48[ 7653] Jab(16) Motivate(16) Bomb(11)                              | Legendary 6* Dr. Amy Wong + Legendary 6 K Pop Video
		Bender's Ducklings           20/55[ 7128] Heal(22-animal) Motivate(16-animal) Crazed(10)             | Legendary 6** Bender + Legendary 6* Mr. Business
		Electric Love                19/57[ 5977] Motivate(16-musical) Cripple(21)                           | Legendary 6* Tina + Legendary 6** K Pop Video
	[Punch]
		Gun Safety Peter             18/70[ 6970] Punch(21) Jab(15)                                          | Legendary 6** Peter + Legendary 6** Pantry Guns
		Chicken Fight                17/63[ 9774] Motivate(11) Punch(20) Bomb(16)                            | Legendary 6** Peter + Legendary 6* Big Boy Karate
		Death Metal                  18/49[ 7320] Punch(20) Recover(12) Payback(16)                          | Legendary 6 Chris Griffin + Legendary 6** K Pop Video
		Red Rodriguez 2 Real         22/58[ 6808] Cheer(22-musical) Punch(20)                                | Legendary 6** Bender + Legendary 6** K Pop Video
		Chicken Fight                20/49[ 9137] Motivate(10) Punch(19) Bomb(14)                            | Legendary 6** Peter + Legendary 6* Quahog Martial Arts Academy
```
