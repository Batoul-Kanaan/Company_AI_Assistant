from backend.app.database.policies import (
    create_policy,
    get_policy,
    get_all_policies,
    search_policies,
    update_policy,
    delete_policy,
)


policy_data = {
    "policy_id": "POL-TEST-001",
    "title": "Remote Work Policy",
    "description": "Policy for employees working remotely",
    "category": "HR",
    "content": "Employees may work remotely according to company guidelines.",
    "status": "active",
}


print("=== CREATE ===")
policy = create_policy(policy_data)
print(policy)


print("\n=== GET ONE ===")
policy = get_policy("POL-TEST-001")
print(policy)


print("\n=== GET ALL ===")
policies = get_all_policies()
print(f"Total policies: {len(policies)}")


print("\n=== SEARCH ===")
policies = search_policies({
    "category": "HR"
})
print(f"HR policies: {len(policies)}")


print("\n=== UPDATE ===")
updated_policy = update_policy(
    "POL-TEST-001",
    {
        "status": "inactive",
    },
)
print(updated_policy)


print("\n=== DELETE ===")
deleted = delete_policy("POL-TEST-001")
print("Deleted:", deleted)