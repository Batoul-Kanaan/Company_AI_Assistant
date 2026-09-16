from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth import verify_credentials

from backend.app.database.policies import (
    create_policy,
    get_policy,
    get_all_policies,
    search_policies,
    update_policy,
    delete_policy,
)

from backend.app.models.policy import (
    PolicyCreate,
    PolicyUpdate,
)


router = APIRouter(
    prefix="/policies",
    tags=["Policies"],
    dependencies=[Depends(verify_credentials)],
)


def serialize_policy(policy: dict):
    if policy:
        policy["_id"] = str(policy["_id"])

    return policy


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_policy_route(policy: PolicyCreate):
    existing_policy = get_policy(policy.policy_id)

    if existing_policy:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Policy already exists",
        )

    result = create_policy(
        policy.model_dump()
    )

    return serialize_policy(result)


@router.get("/")
def get_policies():
    policies = get_all_policies()

    return [
        serialize_policy(policy)
        for policy in policies
    ]


@router.get("/search")
def search_policies_route(
    category: str | None = None,
    status: str | None = None,
):
    query = {}

    if category:
        query["category"] = category

    if status:
        query["status"] = status

    policies = search_policies(query)

    return [
        serialize_policy(policy)
        for policy in policies
    ]


@router.get("/{policy_id}")
def get_policy_route(policy_id: str):
    policy = get_policy(policy_id)

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    return serialize_policy(policy)


@router.put("/{policy_id}")
def update_policy_route(
    policy_id: str,
    policy: PolicyUpdate,
):
    existing_policy = get_policy(policy_id)

    if not existing_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    updated_policy = update_policy(
        policy_id,
        policy.model_dump(exclude_unset=True),
    )

    return serialize_policy(updated_policy)


@router.delete("/{policy_id}")
def delete_policy_route(policy_id: str):
    deleted = delete_policy(policy_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

    return {
        "message": "Policy deleted successfully"
    }