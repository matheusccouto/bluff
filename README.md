# bluff
Bluff is a pythonic poker framework.

[![PyPi Version](https://img.shields.io/pypi/v/bluff.svg)](https://pypi.python.org/pypi/bluff/)
[![MIT License](https://img.shields.io/github/license/matheusccouto/bluff)](https://github.com/matheusccouto/bluff/blob/master/LICENSE)

Currently, bluff covers the following poker variants:
* Texas Hold'em
* Chinese Poker

## Getting Started
### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Bluff.
```bash
pip install bluff
```
### Usage
#### Evaluating hands
```python
import bluff

# Hands can be created by passing Card instances as arguments.
hand1 = bluff.Hand(
    bluff.Card("5d"),
    bluff.Card("4s"),
    bluff.Card("5s"),
    bluff.Card("4c"),
    bluff.Card("5h"),
)

hand1.name
>>> "full_house"
```
#### Comparing hands values
```python
import bluff

# Hands can also be created by passing their string representations.
hand1 = bluff.Hand("5d", "4s", "5s", "4c", "5h")
# Concatenated strings are also accepted.
hand2 = bluff.Hand("Jh", "Td", "Js", "5s", "8d")

hand1.value > hand2.value
>>> True
```

#### Drawing a card for a player
```python
import bluff

player = bluff.Player(name="Chris Moneymaker", chips=10000)
deck = bluff.Deck()
card = deck.draw()
player.hand.add(card)
```
#### Evaluating equity with Monte Carlo
```python
from bluff.holdem import equity

equity.equity(("QQ", "AKo"), times=10000)
```
#### Evaluating a hand equity against several ranges
```python
from bluff.holdem import equity

# Ranges descriptions.
equity.eval_ranges("JTs", ("KQs ATo 99", "AKs QQ"), times=10000)
# Ranges percentages.
equity.eval_ranges("JTs", (10, 30), times=10000)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Author

* **Matheus Couto** - [Linkedin](https://www.linkedin.com/in/matheusccouto/)

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.