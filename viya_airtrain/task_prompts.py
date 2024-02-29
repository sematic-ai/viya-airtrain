from itertools import cycle


TASK_PROMPT_BY_AGENT_NAME = {
    "FamilyHistoryAgent": cycle(
        [
            (
                "Gather information about the patient's immediate family medical history "
                "including those living as well as deceased. Don't ask about each "
                "family member separately."
            ),
            (
                "Get details about the patient's immediate family medical history "
                "including BOTH living AND deceased family members. Be careful not "
                "to inquire regarding each family member individually."
            ),
            (
                "Ask about the medical history of the patient. You should ask about "
                "siblings/parents only, regardless of whether or not they're "
                "currently alive. To avoid tedium, don't ask about the family members "
                "as individuals if possible, but rather as a group."
            ),
            (
                "Retrieve medical history data on the patient's family. Asking about "
                "each family member individually should be avoided, but it's ok to ask "
                "about people who are no longer living, provided that they're still "
                "immediate family (immediate family members are the only ones you should "
                "ask questions about)."
            ),
            (
                "Inquire as to the nature of the medical history of the patient's "
                "family (immediate members only). You shouldn't discriminate individual "
                "family members, including their status as alive/dead."
            ),
            (
                "Collect intel on the medical history of the patient's FAMILY. "
                "You shouldn't: (a) ask about individual members of said family nor "
                "(b) care whether the family members are alive nor "
                "(c) care about family members who aren't the patients siblings/parents."
            ),
            (
                "Kindly interrogate the patient to determine the medical history "
                "of their family. Be concise by asking about the family as a group "
                "rather than as individuals. Siblings and parents should be considered, "
                "but other more distant family members should not."
            ),
            (
                "Determine the family medical history of the patient by asking "
                "questions. Asking about family members should be avoided if they are "
                "non-immediate. The fact that the family members are living or dead is "
                "irrelevant to your task."
            ),
            (
                "Clarify relevant details about the medical history of the family of the "
                "patient with your questions. The alive/dead nature of those family "
                "members doesn't matter, but whether they are close or distant relatives "
                "does (focus on parents and siblings)."
            ),
            (
                "Compile data on the patient's immediate family's medical history. "
                "DON'T: care whether the family members are alive or dead. DON'T "
                "ask about the family members one-by-one."
            ),
        ]
    ),
    "MedicalHistoryAgent": cycle(
        [
            (
                "Gather information about the history of patient's medical "
                "conditions, surgeries, allergies to food, medicines and environmental "
                "allergens along with current list of medications and supplements that "
                "the patient is taking along with dosage and frequency."
            ),
            (
                "Obtain intel about the medical history of the patient. "
                "Some things to ask about: "
                "(a) past/current medical conditions "
                "(b) surgeries they've had "
                "(c) food alergies "
                "(d) medicinal allergies "
                "(e) environmental allergies "
                "(f) current medicines "
                "(g) dosages of those medicines "
                "(e) frequency of taking those medicines."
            ),
            (
                "Be inquisitve regarding the medical history of the patient themselves. "
                "You should want to know about any medicines they're on, as well as "
                "how often they're taking them and what dosages they're using. "
                "Allergies are also important, including environmental ones, "
                "food ones, and any allergies to medications. Most importantly, "
                "ask about any medical conditions they have/have had and any surgeries "
                "they've had (especially recent ones)."
            ),
            (
                "Determine the patient's history, medically speaking. Regarding "
                "allergies, ask about all kinds: medicine allergies, food allergies, "
                "environmental allergies... When it comes to their medications, you'll "
                "do well to find out which ones they're on, as well as how often & in "
                "what dosages. DON'T FORGET to ask about any medical conditions, "
                "past or present, and any surgeries they've undergone."
            ),
            (
                "Figure out what you can about the medical history of the patient. "
                "Recent surgeries are of particular importance, as are any medical "
                "conditions. The medications (kind, frequency, dosage) are also "
                "important to know about. Allergies? Ask about those too, whether they "
                "be allergies to things in the environment, medications, or foods."
            ),
            (
                "Learn about the medical facts of the patient, past or present. "
                "Surgeries and medical conditions are definitely things you "
                "should ask about. Please get to know about the dosages and "
                "frequencies of any medications. Don't neglect allergies either."
            ),
            (
                "Take a proactive approach in understanding the patient's medical "
                "background. It's essential to inquire about the medications they "
                "are currently using, including the frequency and dosages. Don't forget "
                "to explore any allergies they may have, whether to the environment, "
                "food, or drugs. Above all, it's crucial to gather information "
                "on any existing or past medical conditions and surgeries, "
                "particularly those that are recent."
            ),
            (
                "Assess the patient's medical history thoroughly. "
                "Inquire about any allergies—medicinal, food-related, "
                "or environmental. Ensure to learn about their current "
                "medications, including the frequency and dosages. Crucially, "
                "gather details on any past or present medical conditions and surgeries "
                "they have undergone."
            ),
            (
                "Collect details on the patient's medical history, emphasizing: "
                "(a) current medications, including (b) dosages and "
                "(c) frequency of administration, (d) any allergies to food, "
                "(e) drugs, or (f) environmental factors, (g) past or present medical "
                "conditions, and (h) surgical history."
            ),
            (
                "Procure comprehensive data regarding the patient’s medical antecedents, "
                "necessitating an exhaustive inquiry into: (a) the pharmacological "
                "agents presently being administered, alongside (b) "
                "their respective quantifications and "
                "(c) the temporal regularity of their consumption, "
                "(d) hypersensitivity reactions to alimentary substances, "
                "(e) pharmaceutical compounds, or (f) environmental stimuli, "
                "(g) historical and concurrent pathophysiological states, and "
                "(h) any operative interventions previously or recently undertaken."
            ),
        ]
    ),
    "SocialHistoryAgent": cycle(
        [
            (
                "Gather information about the patient's lifestyle like if they're "
                "married, if they work anywhere, if they smoke, drink, or use drugs, "
                "and if they've traveled outside of the country in the last 6 months. "
                "Get more details about each of these where applicable."
            ),
        ]
    ),
}


def get_task_prompt(agent_name: str):
    return next(TASK_PROMPT_BY_AGENT_NAME[agent_name])
