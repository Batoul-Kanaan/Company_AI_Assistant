from backend.app.models.policy import PolicyCreate


policy = PolicyCreate(
    policy_id="POL-TEST-001",
    title="Remote Work Policy",
    description="Policy for employees working remotely",
    category="HR",
    content="Employees may work remotely according to company guidelines.",
)

print(policy)
print("Policy model OK")