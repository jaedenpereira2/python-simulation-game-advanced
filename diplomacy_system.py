import random
from typing import Dict, List, Tuple, Optional

class DiplomacySystem:
    def __init__(self, civilization_names: List[str]):
        # Relationship states: 'allied', 'neutral', 'war'
        self.relationships: Dict[Tuple[str, str], str] = {}
        self._initialize_relationships(civilization_names)
        self.trade_offers: List[Dict] = []  # List of pending trade offers

    def _initialize_relationships(self, civilization_names: List[str]):
        for i, civ1 in enumerate(civilization_names):
            for civ2 in civilization_names[i+1:]:
                self.relationships[(civ1, civ2)] = 'neutral'
                self.relationships[(civ2, civ1)] = 'neutral'

    def get_relationship(self, civ1: str, civ2: str) -> str:
        return self.relationships.get((civ1, civ2), 'neutral')

    def set_relationship(self, civ1: str, civ2: str, state: str):
        self.relationships[(civ1, civ2)] = state
        self.relationships[(civ2, civ1)] = state

    def declare_war(self, civ1: str, civ2: str):
        self.set_relationship(civ1, civ2, 'war')

    def propose_alliance(self, civ1: str, civ2: str):
        # For now, instantly accept
        self.set_relationship(civ1, civ2, 'allied')

    def make_peace(self, civ1: str, civ2: str):
        self.set_relationship(civ1, civ2, 'neutral')

    def propose_trade(self, from_civ: str, to_civ: str, offer: Dict[str, float], request: Dict[str, float]):
        self.trade_offers.append({
            'from': from_civ,
            'to': to_civ,
            'offer': offer,
            'request': request,
            'status': 'pending'
        })

    def resolve_trade(self, offer_index: int, accept: bool):
        if 0 <= offer_index < len(self.trade_offers):
            self.trade_offers[offer_index]['status'] = 'accepted' if accept else 'rejected'

    def get_active_trades(self) -> List[Dict]:
        return [offer for offer in self.trade_offers if offer['status'] == 'pending']

    def draw(self, screen, font, x, y, civilizations):
        # Draw relationship matrix
        civ_names = [civ.name for civ in civilizations]
        for i, civ1 in enumerate(civ_names):
            for j, civ2 in enumerate(civ_names):
                if i == j:
                    continue
                rel = self.get_relationship(civ1, civ2)
                color = (200, 200, 200)
                if rel == 'allied':
                    color = (0, 200, 255)
                elif rel == 'war':
                    color = (255, 50, 50)
                text = f"{civ1[:3]}-{civ2[:3]}: {rel}"
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (x, y + 20 * (i * len(civ_names) + j)))
        # Draw pending trades
        trade_y = y + 25 * len(civ_names) * len(civ_names)
        for offer in self.get_active_trades():
            text = f"Trade: {offer['from']}→{offer['to']} Offer: {offer['offer']} Request: {offer['request']}"
            text_surface = font.render(text, True, (255, 255, 0))
            screen.blit(text_surface, (x, trade_y))
            trade_y += 20 