"""Types for usage in the rest of the scripts."""
from typing import Literal, TypedDict


ALL_DONE = "ALL_DONE"


AssistantRole = Literal["assistant"]
UserRole = Literal["user"]
SystemRole = Literal["system"]
Role = AssistantRole | UserRole | SystemRole

Summary = str

# Explicitly typing each complaint agent name is kind of overkill.
# Feel free to discard.
ChiefComplaintAgent = Literal["ChiefComplaintAgent"]
ChiefComplaintAgentADHD = Literal["ChiefComplaintAgent:ADHD"]
ChiefComplaintAgentAbPain = Literal["ChiefComplaintAgent:Abdominal Pain"]
ChiefComplaintAgentAnxiety = Literal["ChiefComplaintAgent:Anxiety"]
ChiefComplaintAgentAsthma = Literal["ChiefComplaintAgent:Asthma"]
ChiefComplaintAgentBackPain = Literal["ChiefComplaintAgent:Back pain"]
ChiefComplaintAgentChestPain = Literal["ChiefComplaintAgent:Chest Pain"]
ChiefComplaintAgentConstipation = Literal["ChiefComplaintAgent:Constipation"]
ChiefComplaintAgentCough = Literal["ChiefComplaintAgent:Cough"]
ChiefComplaintAgentDepression = Literal["ChiefComplaintAgent:Depression"]
ChiefComplaintAgentDiarrhea = Literal["ChiefComplaintAgent:Diarrhea"]
ChiefComplaintAgentFever = Literal["ChiefComplaintAgent:Fever"]
ChiefComplaintAgentFlankPain = Literal["ChiefComplaintAgent:Flank pain"]
ChiefComplaintAgentHeadache = Literal["ChiefComplaintAgent:Headache"]
ChiefComplaintAgentHighBp = Literal["ChiefComplaintAgent:High blood pressure"]
ChiefComplaintAgentIrregularHb = Literal[
    "ChiefComplaintAgent:Irregular heartbeats or palpitations"
]
ChiefComplaintAgentMoodIssues = Literal["ChiefComplaintAgent:Mood issues"]
ChiefComplaintAgentNoseBleed = Literal["ChiefComplaintAgent:Nose bleeding"]
ChiefComplaintAgentOcd = Literal["ChiefComplaintAgent:OCD"]
ChiefComplaintAgentPanicAttacks = Literal["ChiefComplaintAgent:Panic attacks"]
ChiefComplaintAgentPelvicPain = Literal["ChiefComplaintAgent:Pelvic pain"]
ChiefComplaintAgentPenile = Literal["ChiefComplaintAgent:Penile concerns"]
ChiefComplaintAgentRash = Literal["ChiefComplaintAgent:Rash"]
ChiefComplaintAgentShortOfBreath = Literal["ChiefComplaintAgent:Shortness of breath"]
ChiefComplaintAgentSickVisit = Literal["ChiefComplaintAgent:Sick visit"]
ChiefComplaintAgentSoreThroat = Literal["ChiefComplaintAgent:Sore throat"]
ChiefComplaintAgentSwelling = Literal["ChiefComplaintAgent:Swelling"]
FamilyHistoryAgent = Literal["FamilyHistoryAgent"]
FeedbackAgent = Literal["FeedbackAgent"]
MedicalHistoryAgent = Literal["MedicalHistoryAgent"]
OnboardingAgent = Literal["OnboardingAgent"]
PatientProxy = Literal["PatientProxy"]
ReviewOfSystemsAgent = Literal["ReviewOfSystemsAgent"]
SocialHistoryAgent = Literal["SocialHistoryAgent"]
DefaultAgent = Literal["default"]
UserAgent = Literal["user"]


AgentName = (
    ChiefComplaintAgent
    | ChiefComplaintAgentADHD
    | ChiefComplaintAgentAbPain
    | ChiefComplaintAgentAnxiety
    | ChiefComplaintAgentAsthma
    | ChiefComplaintAgentBackPain
    | ChiefComplaintAgentChestPain
    | ChiefComplaintAgentConstipation
    | ChiefComplaintAgentCough
    | ChiefComplaintAgentDepression
    | ChiefComplaintAgentDiarrhea
    | ChiefComplaintAgentFever
    | ChiefComplaintAgentFlankPain
    | ChiefComplaintAgentHeadache
    | ChiefComplaintAgentHighBp
    | ChiefComplaintAgentIrregularHb
    | ChiefComplaintAgentMoodIssues
    | ChiefComplaintAgentNoseBleed
    | ChiefComplaintAgentOcd
    | ChiefComplaintAgentPanicAttacks
    | ChiefComplaintAgentPelvicPain
    | ChiefComplaintAgentPenile
    | ChiefComplaintAgentRash
    | ChiefComplaintAgentShortOfBreath
    | ChiefComplaintAgentSickVisit
    | ChiefComplaintAgentSoreThroat
    | ChiefComplaintAgentSwelling
    | FamilyHistoryAgent
    | FeedbackAgent
    | MedicalHistoryAgent
    | OnboardingAgent
    | PatientProxy
    | ReviewOfSystemsAgent
    | SocialHistoryAgent
    | DefaultAgent
    | UserAgent
)


class RawMessage(TypedDict):
    """A message in the raw transcripts"""

    role: Role
    content: str
    agent_name: AgentName
    interaction_type: str
    timestamp: str
    time_taken_in_ms: int
    section: str
    attributes: dict[str, str]
    md5: str


class PatientProfile(TypedDict):
    """A patient profile from the raw transcripts"""

    first_name: str
    last_name: str
    gender: str
    age_in_years: str
    chief_complaint: str
    profile: str
    profile_id: str
    patient_id: str


class SimContext(TypedDict):
    """A sim context from the raw transcripts"""

    task_index: int
    agent_type: str
    working_dir: str
    start_time: str
    patient_profile: PatientProfile
    request_sleep_delay_seconds: float
    max_conversation_length: int
    wait_for_summary: bool
    end_time: str
    duration: str


class FullRawTranscript(TypedDict):
    """The full raw transcript in each source json file."""

    session_id: str
    messages: list[RawMessage]
    summary: None | Summary
    profile_id: str
    profile_chief_complaint: str
    profile_gender: str
    error: str | None
    sim_context: SimContext


class SimpleTurn(TypedDict):
    """Minimal representation of a chat turn."""

    role: Role
    content: str


class ConversationTurn(TypedDict):
    """A row in final output jsonl."""

    session_id: str
    message_index: int
    is_hidden: bool
    role: Role
    agent_name: AgentName
    prior_turns: list[SimpleTurn]
    rendered_prior_turns: str
    content: str
    task_prompt: str | None
    chief_complaint: str
    patient_age_in_years: str
    patient_first_name: str
    patient_last_name: str
    patient_gender: str


class SimpleTranscript(TypedDict):
    messages: list[SimpleTurn]
    session_id: str
    patient_first_name: str
    patient_last_name: str
    patient_gender: str
    patient_age_in_years: str
    task_prompt: str
