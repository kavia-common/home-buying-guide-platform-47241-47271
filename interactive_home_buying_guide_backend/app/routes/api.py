from flask import Blueprint, jsonify, request
from typing import List, Dict, Any, Optional
import copy

api_bp = Blueprint("api", __name__)

# Seed data representing a typical home buying journey
# In-memory store; could be swapped with file or DB later
_SEED_STEPS: List[Dict[str, Any]] = [
    {
        "id": "budgeting",
        "title": "Budgeting",
        "summary": "Assess your finances and set a realistic budget.",
        "order": 1,
        "description": "Calculate your monthly income, expenses, and determine how much you can afford for a home.",
        "checklist": [
            {"id": "analyze-income", "label": "Analyze monthly income", "completed": False},
            {"id": "track-expenses", "label": "Track monthly expenses", "completed": False},
            {"id": "set-budget", "label": "Set a home buying budget", "completed": False},
            {"id": "emergency-fund", "label": "Confirm emergency fund in place", "completed": False},
        ],
    },
    {
        "id": "preapproval",
        "title": "Pre-approval",
        "summary": "Get pre-approved for a mortgage.",
        "order": 2,
        "description": "Gather financial documents and obtain a mortgage pre-approval letter from a lender.",
        "checklist": [
            {"id": "check-credit", "label": "Check credit score", "completed": False},
            {"id": "gather-docs", "label": "Gather financial documents", "completed": False},
            {"id": "contact-lenders", "label": "Contact lenders for rates", "completed": False},
            {"id": "get-letter", "label": "Obtain pre-approval letter", "completed": False},
        ],
    },
    {
        "id": "search",
        "title": "Home Search",
        "summary": "Find properties that match your needs.",
        "order": 3,
        "description": "Work with an agent or browse listings to find potential homes within your budget.",
        "checklist": [
            {"id": "define-criteria", "label": "Define must-haves and nice-to-haves", "completed": False},
            {"id": "set-alerts", "label": "Set up listing alerts", "completed": False},
            {"id": "tour-homes", "label": "Tour shortlisted homes", "completed": False},
        ],
    },
    {
        "id": "offer",
        "title": "Make an Offer",
        "summary": "Submit a competitive offer for a home.",
        "order": 4,
        "description": "Work with your agent to craft an offer and negotiate terms.",
        "checklist": [
            {"id": "review-comps", "label": "Review comparable sales", "completed": False},
            {"id": "decide-terms", "label": "Decide offer terms and contingencies", "completed": False},
            {"id": "submit-offer", "label": "Submit offer", "completed": False},
        ],
    },
    {
        "id": "inspection",
        "title": "Inspection",
        "summary": "Inspect the property for issues.",
        "order": 5,
        "description": "Hire a professional to inspect the home and review the results.",
        "checklist": [
            {"id": "hire-inspector", "label": "Hire a licensed inspector", "completed": False},
            {"id": "attend-inspection", "label": "Attend inspection", "completed": False},
            {"id": "review-report", "label": "Review the inspection report", "completed": False},
        ],
    },
    {
        "id": "closing",
        "title": "Closing",
        "summary": "Finalize the purchase.",
        "order": 6,
        "description": "Complete final walkthrough, sign documents, and get the keys.",
        "checklist": [
            {"id": "final-walkthrough", "label": "Do final walkthrough", "completed": False},
            {"id": "review-closing", "label": "Review closing disclosure", "completed": False},
            {"id": "sign-docs", "label": "Sign closing documents", "completed": False},
        ],
    },
    {
        "id": "move-in",
        "title": "Move-In",
        "summary": "Plan your move.",
        "order": 7,
        "description": "Arrange movers, utilities, and settle into your new home.",
        "checklist": [
            {"id": "setup-utilities", "label": "Set up utilities and internet", "completed": False},
            {"id": "hire-movers", "label": "Hire movers or plan move", "completed": False},
            {"id": "address-change", "label": "Update address with services", "completed": False},
        ],
    },
]

_RESOURCES = [
    {"id": "calc", "title": "Mortgage Calculator", "url": "https://www.bankrate.com/calculators/mortgages/mortgage-calculator.aspx"},
    {"id": "cfpb", "title": "CFPB Home Buying Resources", "url": "https://www.consumerfinance.gov/owning-a-home/"},
    {"id": "va", "title": "VA Loan Info", "url": "https://www.va.gov/housing-assistance/home-loans/"},
    {"id": "hud", "title": "HUD Resources", "url": "https://www.hud.gov/topics/buying_a_home"},
]

# In-memory mutable store initialized from seed
_STORE: Dict[str, Dict[str, Any]] = {step["id"]: copy.deepcopy(step) for step in _SEED_STEPS}


def _compute_completion(step: Dict[str, Any]) -> float:
    items = step.get("checklist", [])
    if not items:
        return 0.0
    done = sum(1 for i in items if i.get("completed"))
    return round(100.0 * done / len(items), 2)


def _list_steps_summary() -> List[Dict[str, Any]]:
    steps = sorted(_STORE.values(), key=lambda s: s.get("order", 0))
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "summary": s["summary"],
            "order": s["order"],
            "completion": _compute_completion(s),
        }
        for s in steps
    ]


def _get_step_detail(step_id: str) -> Optional[Dict[str, Any]]:
    s = _STORE.get(step_id)
    if not s:
        return None
    detail = {
        "id": s["id"],
        "title": s["title"],
        "summary": s["summary"],
        "order": s["order"],
        "description": s.get("description", ""),
        "checklist": s.get("checklist", []),
        "completion": _compute_completion(s),
    }
    return detail


@api_bp.get("/steps")
def get_steps():
    """
    PUBLIC_INTERFACE
    summary: Get list of steps
    description: Returns a list of all guide steps with id, title, summary, order, and completion percent.
    responses:
        200: Successful response with JSON array of steps
    """
    return jsonify(_list_steps_summary())


@api_bp.get("/steps/<string:step_id>")
def get_step(step_id: str):
    """
    PUBLIC_INTERFACE
    summary: Get step detail
    description: Returns details for a specific step including description and checklist items.
    parameters:
        - name: step_id
          in: path
          required: true
          description: Identifier of the step
    responses:
        200: Step detail
        404: Step not found
    """
    detail = _get_step_detail(step_id)
    if not detail:
        return jsonify({"error": "Step not found"}), 404
    return jsonify(detail)


@api_bp.post("/steps/<string:step_id>/checklist/<string:item_id>/toggle")
def toggle_checklist(step_id: str, item_id: str):
    """
    PUBLIC_INTERFACE
    summary: Toggle checklist item
    description: Toggles the completion state of a checklist item for the specified step.
    parameters:
        - name: step_id
          in: path
          required: true
        - name: item_id
          in: path
          required: true
    responses:
        200: Updated step detail
        404: Step or checklist item not found
    """
    step = _STORE.get(step_id)
    if not step:
        return jsonify({"error": "Step not found"}), 404

    items = step.get("checklist", [])
    target = None
    for i in items:
        if i.get("id") == item_id:
            target = i
            break

    if target is None:
        return jsonify({"error": "Checklist item not found"}), 404

    target["completed"] = not bool(target.get("completed"))
    return jsonify(_get_step_detail(step_id))


@api_bp.get("/resources")
def get_resources():
    """
    PUBLIC_INTERFACE
    summary: Get general resources
    description: Returns a list of general resources for home buying.
    responses:
        200: List of resources
    """
    return jsonify(_RESOURCES)


@api_bp.get("/progress")
def get_progress():
    """
    PUBLIC_INTERFACE
    summary: Get overall progress
    description: Returns overall progress summary across all steps.
    responses:
        200: Progress summary
    """
    steps = list(_STORE.values())
    if not steps:
        return jsonify({"overallCompletion": 0.0, "completedSteps": 0, "totalSteps": 0})

    total = len(steps)
    completed_steps = sum(1 for s in steps if _compute_completion(s) >= 99.99)
    # Average completion across steps
    avg = round(sum(_compute_completion(s) for s in steps) / total, 2)
    return jsonify({"overallCompletion": avg, "completedSteps": completed_steps, "totalSteps": total})
