ROLE_PERMISSIONS = {
    "admin": {
        "finance": "full",
        "legal": "full",
        "hr": "full"
    },
    "manager": {
        "finance": "full",
        "legal": "summary",
        "hr": "full"
    },
    "employee": {
        "finance": "none",
        "legal": "none",
        "hr": "own"
    },
    "auditor": {
        "finance": "full",
        "legal": "full",
        "hr": "none"
    }
}


def get_permission(role, department):
    role = role.lower()
    department = department.lower()

    if role not in ROLE_PERMISSIONS:
        return "none"

    return ROLE_PERMISSIONS[role].get(department, "none")


def filter_chunks(chunks, role):
    allowed_chunks = []
    dropped_chunks = []

    for chunk in chunks:
        department = chunk["metadata"]["department"]

        permission = get_permission(role, department)

        if permission == "none":
            dropped_chunks.append(chunk)
            continue

        chunk["permission"] = permission
        allowed_chunks.append(chunk)

    return allowed_chunks, dropped_chunks
if __name__ == "__main__":
    test_chunks = [
        {"text": "Finance information", "metadata": {"department": "finance"}},
        {"text": "Legal information", "metadata": {"department": "legal"}},
        {"text": "HR information", "metadata": {"department": "hr"}}
    ]

    for role in ["admin", "manager", "employee", "auditor"]:
        allowed, dropped = filter_chunks(test_chunks, role)

        print("\nRole:", role)
        print("Allowed:", [c["metadata"]["department"] for c in allowed])
        print("Dropped:", [c["metadata"]["department"] for c in dropped])