from backend.kb_search import semantic_search
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from backend.llm_utils import query_llm
import json 
import re
import os

SALES_FILE = "sales_leads.json"

analyzer = SentimentIntensityAnalyzer()

conversation_state = {
    "initial_query": None,
    "company": None,
    "no_of_team_members": None,
    "additional_info": "",
    "active_intent": None 
    }

def handle_unmatched_tech_issue(query: str):
    prompt = f"What department should handle this technical support query: '{query}'? Respond with only the department name."
    dept = query_llm(prompt)
    return (f"Thanks for your query. I couldn't find an immediate answer, but I've routed your request to our {dept} team. They will get back to you shortly.",dept)

def extract_feature_request(query: str):
    prompt = f"Extract the specific product or feature being requested in this sentence: '{query}'. Respond with only the name."
    feature = query_llm(prompt)
    return (f"Thank you for your suggestion! We've logged your feature request for {feature} for our product team to review.",feature)

def is_negative_sentiment(text):
    return analyzer.polarity_scores(text)['compound'] < -0.5

def is_complex_sales(message):
    keywords = ["bulk", "large", "reseller", "RFP", "deal"]
    return any(k in message.lower() for k in keywords)

def load_sales_leads():
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, "r") as f:
            return json.load(f)
    return []

def save_sales_leads(leads):
    with open(SALES_FILE, "w") as f:
        json.dump(leads, f, indent=2)

def extract_company_name(text):
    prompt = f"Extract the company name from this message: '{text}'. If not found, say 'None'."
    result = query_llm(prompt)
    match = re.search(r"(?i)company\s*[:\-]?\s*(.+)", result)
    return match.group(1).strip() if match else (None if "None" in result else result.strip())

def extract_team_size(text):
    prompt = f"Extract number of team members from this message: '{text}'. If not found, say 'None'."
    result = query_llm(prompt)
    match = re.search(r"(\d+)", result)
    return int(match.group(1)) if match else None

def process_sales_lead(conversation_state: dict, user_input: str,user_email: str) -> tuple[str, dict]:
    #conversation_state.setdefault("additional_info", "")
    if  conversation_state["active_intent"] is not None:
        conversation_state["additional_info"] += " " + user_input.strip()

    if not conversation_state.get("company"):
        company = extract_company_name(user_input)
        if company:
            conversation_state["company"] = company
            return (
                "Thanks for your interest! Our sales team will be in touch soon. "
                "In the meantime, could you tell us more about your needs? "
                "How many team members do you have?",
                conversation_state
            )
        else:
            return "Could you please provide your company name?", conversation_state

    if not conversation_state.get("no_of_team_members"):
        team_size = extract_team_size(user_input)
        if team_size:
            conversation_state["no_of_team_members"] = team_size

            leads = load_sales_leads()
            leads.append({
                "company": conversation_state["company"],
                "email" : user_email,
                "query": conversation_state.get("initial_query", ""),
                "no_of_team_members": conversation_state["no_of_team_members"],
                "additional_info": conversation_state["additional_info"].strip()
            })
            save_sales_leads(leads)

            return (
                "Thank you! Your information has been recorded. "
                "Our sales team will be in touch shortly.",
                conversation_state
            )
        else:
            return "Kindly provide the number of team members in your organization.", conversation_state

    return "All required information received.", conversation_state


def generate_response(message: str, email : str, intent :str = None):
    escalate = False
    if is_negative_sentiment(message):
        with open('negative_sentiment.json', 'a') as f:
            json.dump({"Email": email,"message": message}, f)
            f.write("\n")
        return ("Extremely sorry if we have caused you any inconvenience. We've forwarded your concern to the appropriate team.", conversation_state)

    if intent == "Technical Support":
        topic = semantic_search(message)['topic']
        answer = semantic_search(message)['response']
        if not semantic_search(message)['escalate']:
            escalate= False
            return (f"Thanks for reaching out! Regarding your {topic}, here's some information: {answer}. Does this resolve your issue?", conversation_state)
        else:
            response,dept  = handle_unmatched_tech_issue(message)
            with open('tech_issues.json',"a") as f:
                json.dump({"Email": email, "Department": dept, "query": message}, f)
                f.write("\n")
            return (response, conversation_state)

    elif intent == "Product Feature Request":
        response, feature = extract_feature_request(message)
        with open("feature_requests.json", "a") as f:
            json.dump({"Email": email, "Feature_requested": feature,"Request": message}, f)
            f.write("\n")
        return (response, conversation_state)

    elif intent == "Sales Lead":
        conversation_state.setdefault("initial_query", message)
        response, conversation_state = process_sales_lead(conversation_state, message,email)

        if conversation_state["no_of_team_members"] is None or conversation_state["additional_info"] == "":
            conversation_state["active_intent"] = "Sales Lead"
        else:
            conversation_state["active_intent"] = None
            conversation_state["additional_info"]=""
            
        if is_complex_sales(message):
            with open('complex_sales.json', 'a') as f:
                json.dump({"Email": email,"message": message}, f)
                f.write("\n")
        return (response, conversation_state)

    return (..., conversation_state)
