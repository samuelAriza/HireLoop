from core.interfaces.cart_interface import PurchasableInterface

class MentorshipSessionAdapter(PurchasableInterface):
    def __init__(self, mentorship_session):
        self.mentorship_session = mentorship_session

    def get_price(self) -> float:
        return float(self.mentorship_session.duration_minutes) * 1.5 
    
    def get_title(self) -> str:
        return self.mentorship_session.topic

    def get_type(self) -> str:
        return "mentorship_session"