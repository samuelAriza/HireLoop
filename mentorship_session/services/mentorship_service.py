from typing import List
from ..models import MentorshipSession
from ..repositories.mentorship_repository import MentorshipRepository


class MentorshipService:
    def __init__(self, repository: MentorshipRepository):
        self.repository = repository

    def create_session(
        self, topic, start_time, duration_minutes, mentor_id
    ) -> MentorshipSession:
        return self.repository.create(
            topic=topic,
            start_time=start_time,
            duration_minutes=duration_minutes,
            mentor_id=mentor_id,
        )

    def get_session(self, session_id) -> MentorshipSession:
        session = self.repository.get_by_id(session_id)
        if not session:
            raise ValueError("Mentorship session not found")
        return session

    def update_session(self, session_id, **kwargs) -> MentorshipSession:
        session = self.get_session(session_id)
        return self.repository.update(session, **kwargs)

    def delete_session(self, session_id) -> bool:
        session = self.get_session(session_id)
        return self.repository.delete(session)

    def list_mentor_sessions(self, mentor_id) -> List[MentorshipSession]:
        return self.repository.list_by_mentor(mentor_id)

    def list_mentee_sessions(self, mentee_id) -> List[MentorshipSession]:
        return self.repository.list_by_mentee(mentee_id)
