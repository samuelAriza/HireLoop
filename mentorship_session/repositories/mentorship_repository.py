from typing import Optional, List
from ..models import MentorshipSession
from core.repositories import BaseRepository


class MentorshipRepository(BaseRepository):
    def create(self, **kwargs) -> MentorshipSession:
        return MentorshipSession.objects.create(**kwargs)

    def get_by_id(self, session_id: str) -> Optional[MentorshipSession]:
        return MentorshipSession.objects.filter(id=session_id).first()

    def update(self, session: MentorshipSession, **kwargs) -> MentorshipSession:
        for key, value in kwargs.items():
            setattr(session, key, value)
        session.save()
        return session

    def delete(self, session: MentorshipSession) -> None:
        deleted, _ = session.delete()
        return deleted > 0

    def list_by_mentor(self, mentor_id) -> List[MentorshipSession]:
        return MentorshipSession.objects.filter(mentor_id=mentor_id).all()

    def list_by_mentee(self, mentee_id) -> List[MentorshipSession]:
        return MentorshipSession.objects.filter(mentee_id=mentee_id).all()
